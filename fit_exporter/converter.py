from __future__ import annotations

import datetime
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import fitdecode


def _get_field(fields: Dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in fields:
            return fields[name]
    return None


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _format_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value.isoformat()
    return str(value)


def _normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value.isoformat()
    if hasattr(value, "name") and hasattr(value, "value"):
        return _normalize_value(value.value)
    if isinstance(value, dict):
        return {k: _normalize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_value(v) for v in value]
    return value


def _fields_to_dict(fields: Any) -> Dict[str, Any]:
    if isinstance(fields, dict):
        return {k: _normalize_value(v) for k, v in fields.items()}
    if isinstance(fields, list):
        converted: Dict[str, Any] = {}
        for item in fields:
            if hasattr(item, "name") and hasattr(item, "value"):
                converted[item.name] = _normalize_value(item.value)
            elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
                converted[item[0]] = _normalize_value(item[1])
        return converted
    try:
        return {k: _normalize_value(v) for k, v in dict(fields).items()}
    except Exception:
        return {}


def _pace_from_speed(speed: Optional[float]) -> Optional[float]:
    if speed is None or speed <= 0:
        return None
    return 1000.0 / speed


def _record_from_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    speed = _to_float(_get_field(fields, "speed", "enhanced_speed"))
    distance = _to_float(_get_field(fields, "distance", "enhanced_distance"))
    elevation = _to_float(_get_field(fields, "altitude", "enhanced_altitude"))

    return {
        "timestamp": _format_timestamp(_get_field(fields, "timestamp")),
        "distance_m": distance,
        "speed_mps": speed,
        "pace_min_per_km": _pace_from_speed(speed),
        "heart_rate": _to_int(_get_field(fields, "heart_rate", "enhanced_heart_rate")),
        "cadence_spm": _to_int(_get_field(fields, "cadence", "cadence_left", "cadence_right")),
        "power": _to_int(_get_field(fields, "power", "enhanced_power")),
        "latitude": _to_float(_get_field(fields, "position_lat", "enhanced_altitude"))
        if "position_lat" in fields
        else None,
        "longitude": _to_float(_get_field(fields, "position_long", "enhanced_altitude"))
        if "position_long" in fields
        else None,
        "elevation_m": elevation,
    }


def _lap_from_fields(fields: Dict[str, Any], lap_number: int) -> Dict[str, Any]:
    speed = _to_float(_get_field(fields, "avg_speed", "avg_speed"))
    avg_hr = _to_int(_get_field(fields, "avg_heart_rate", "avg_heart_rate"))
    avg_cadence = _to_int(_get_field(fields, "avg_cadence", "avg_running_cadence"))
    avg_power = _to_int(_get_field(fields, "avg_power", "avg_power"))

    return {
        "lap_number": lap_number,
        "type": _get_field(fields, "lap_trigger", "event", "sport", "sub_sport") or "lap",
        "distance_m": _to_float(_get_field(fields, "total_distance", "distance")),
        "duration_s": _to_float(_get_field(fields, "total_elapsed_time", "total_timer_time", "timestamp")),
        "average_pace_min_per_km": _pace_from_speed(speed),
        "average_hr": avg_hr,
        "max_hr": _to_int(_get_field(fields, "max_heart_rate", "max_heart_rate")),
        "average_cadence": avg_cadence,
        "average_power": avg_power,
    }


def _build_workout(name: Optional[str], steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not name and not steps:
        return {}
    return {
        "name": name or "",
        "steps": steps,
    }


def _normalize_fields(fields: Any) -> Dict[str, Any]:
    if isinstance(fields, dict):
        return fields
    if isinstance(fields, list):
        try:
            return dict(fields)
        except (TypeError, ValueError):
            pass
    return {str(i): value for i, value in enumerate(fields)}


def _parse_workout_step(fields: Any) -> Dict[str, Any]:
    fields = _fields_to_dict(fields)
    duration = _to_float(_get_field(fields, "duration", "duration_type"))
    target_pace = _to_float(_get_field(fields, "target_value", "target_speed"))
    return {
        "type": _get_field(fields, "wkt_step_name", "workout_step_name", "step_name") or "step",
        "duration_s": duration,
        "target_pace_min_per_km": target_pace,
        "raw_fields": {
            k: v for k, v in fields.items() if k not in {"timestamp", "type"}
        },
    }


def _safe_average(values: List[Optional[float]]) -> Optional[float]:
    valid = [v for v in values if v is not None]
    if not valid:
        return None
    return sum(valid) / len(valid)


def _hms_to_seconds(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _timestamp_span(records: List[Dict[str, Any]]) -> Optional[float]:
    timestamps = [r["timestamp"] for r in records if r.get("timestamp")]
    if not timestamps:
        return None
    parsed = [datetime.datetime.fromisoformat(ts) for ts in timestamps]
    if not parsed:
        return None
    elapsed = max(parsed) - min(parsed)
    return elapsed.total_seconds()


def parse_fit_file(fit_path: str) -> Dict[str, Any]:
    fit_path_obj = Path(fit_path)
    if not fit_path_obj.exists():
        raise FileNotFoundError(f"Input path does not exist: {fit_path}")

    metadata: Dict[str, Any] = {
        "schema_version": "1.0",
        "device": None,
        "software_version": None,
        "activity_date": None,
        "sport": None,
        "sub_sport": None,
        "timezone": None,
    }
    session_fields: Dict[str, Any] = {}
    file_id_fields: Dict[str, Any] = {}
    device_info_fields: Dict[str, Any] = {}
    workout_name: Optional[str] = None
    workout_steps: List[Dict[str, Any]] = []
    records: List[Dict[str, Any]] = []
    laps: List[Dict[str, Any]] = []

    with fitdecode.FitReader(str(fit_path_obj), check_crc=True) as reader:
        lap_count = 0
        for frame in reader:
            if not hasattr(frame, "name") or not hasattr(frame, "fields"):
                continue
            frame_fields = _fields_to_dict(frame.fields)
            if frame.name == "file_id":
                file_id_fields = frame_fields
            elif frame.name == "device_info":
                device_info_fields = frame_fields
            elif frame.name == "session":
                session_fields = frame_fields
            elif frame.name == "lap":
                lap_count += 1
                laps.append(_lap_from_fields(frame_fields, lap_count))
            elif frame.name == "record":
                records.append(_record_from_fields(frame_fields))
            elif frame.name == "workout":
                workout_name = _get_field(frame_fields, "wkt_name", "name")
            elif frame.name == "workout_step":
                workout_steps.append(_parse_workout_step(frame_fields))

    metadata["device"] = _get_field(device_info_fields, "product_name", "product")
    metadata["software_version"] = _get_field(device_info_fields, "software_version")
    metadata["activity_date"] = _format_timestamp(_get_field(file_id_fields, "timestamp", "time_created"))
    metadata["sport"] = _get_field(session_fields, "sport") or "running"
    metadata["sub_sport"] = _get_field(session_fields, "sub_sport")
    if metadata["activity_date"] is not None:
        try:
            parsed_date = datetime.datetime.fromisoformat(metadata["activity_date"])
            metadata["timezone"] = parsed_date.tzname() or "UTC"
        except ValueError:
            metadata["timezone"] = "UTC"

    total_distance = _to_float(_get_field(session_fields, "total_distance", "total_distance"))
    moving_time = _to_float(_get_field(session_fields, "total_timer_time", "total_timer_time"))
    elapsed_time = _to_float(_get_field(session_fields, "total_elapsed_time", "total_elapsed_time"))
    avg_speed = _to_float(_get_field(session_fields, "avg_speed", "avg_speed"))
    max_speed = _to_float(_get_field(session_fields, "max_speed", "max_speed"))
    avg_hr = _to_int(_get_field(session_fields, "avg_heart_rate", "avg_heart_rate"))
    max_hr = _to_int(_get_field(session_fields, "max_heart_rate", "max_heart_rate"))
    avg_cadence = _to_int(_get_field(session_fields, "avg_running_cadence", "avg_cadence"))
    max_cadence = _to_int(_get_field(session_fields, "max_running_cadence", "max_cadence"))
    avg_power = _to_int(_get_field(session_fields, "avg_power", "avg_power"))
    max_power = _to_int(_get_field(session_fields, "max_power", "max_power"))
    total_ascent = _to_float(_get_field(session_fields, "total_ascent", "total_ascent"))
    total_descent = _to_float(_get_field(session_fields, "total_descent", "total_descent"))
    calories = _to_int(_get_field(session_fields, "total_calories", "total_calories"))

    if not total_distance and records:
        last_distance = next((r["distance_m"] for r in reversed(records) if r.get("distance_m") is not None), None)
        total_distance = last_distance
    if not elapsed_time and records:
        elapsed_time = _timestamp_span(records)
    if not moving_time:
        moving_time = elapsed_time
    if not avg_speed and total_distance and moving_time:
        avg_speed = total_distance / moving_time if moving_time > 0 else None
    if not avg_hr and records:
        avg_hr = _safe_average([r["heart_rate"] for r in records if r.get("heart_rate") is not None])
    if not max_hr and records:
        max_hr = max((r["heart_rate"] for r in records if r.get("heart_rate") is not None), default=None)
    if not avg_cadence and records:
        avg_cadence = _safe_average([r["cadence_spm"] for r in records if r.get("cadence_spm") is not None])
    if not max_cadence and records:
        max_cadence = max((r["cadence_spm"] for r in records if r.get("cadence_spm") is not None), default=None)
    if not avg_power and records:
        avg_power = _safe_average([r["power"] for r in records if r.get("power") is not None])
    if not max_power and records:
        max_power = max((r["power"] for r in records if r.get("power") is not None), default=None)
    if not total_ascent and records:
        asc = 0.0
        elevations = [r["elevation_m"] for r in records if r.get("elevation_m") is not None]
        for prev, curr in zip(elevations, elevations[1:]):
            if curr > prev:
                asc += curr - prev
        total_ascent = asc or None
    if not total_descent and records:
        desc = 0.0
        elevations = [r["elevation_m"] for r in records if r.get("elevation_m") is not None]
        for prev, curr in zip(elevations, elevations[1:]):
            if curr < prev:
                desc += prev - curr
        total_descent = desc or None

    summary: Dict[str, Any] = {
        "distance_m": total_distance,
        "moving_time_s": moving_time,
        "elapsed_time_s": elapsed_time,
        "avg_speed_mps": avg_speed,
        "max_speed_mps": max_speed,
        "avg_pace_min_per_km": _pace_from_speed(avg_speed),
        "calories": calories,
        "avg_hr": _to_int(avg_hr) if avg_hr is not None else None,
        "max_hr": max_hr,
        "avg_cadence_spm": _to_int(avg_cadence) if avg_cadence is not None else None,
        "max_cadence_spm": max_cadence,
        "avg_power": _to_int(avg_power) if avg_power is not None else None,
        "max_power": max_power,
        "total_ascent": total_ascent,
        "total_descent": total_descent,
    }

    workout = _build_workout(workout_name, workout_steps)

    return {
        "metadata": metadata,
        "summary": summary,
        "workout": workout,
        "splits": laps,
        "records": records,
        "derived": {},
        "notes": {},
    }

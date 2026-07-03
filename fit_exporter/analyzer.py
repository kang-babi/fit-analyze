from __future__ import annotations

import math
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fit_exporter.validator import validate_activity_schema


def _safe_average(values: List[float]) -> Optional[float]:
    values = [value for value in values if value is not None]
    if not values:
        return None
    return sum(values) / len(values)


def _safe_standard_deviation(values: List[float]) -> Optional[float]:
    values = [value for value in values if value is not None]
    if len(values) < 2:
        return None
    return statistics.stdev(values)


def _as_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [record for record in records if isinstance(record, dict)]


def _slice_segment(records: List[Dict[str, Any]], start: float, end: float) -> List[Dict[str, Any]]:
    if not records:
        return []
    start_index = int(len(records) * start)
    end_index = int(len(records) * end)
    return records[start_index:end_index] if start_index < end_index else []


def _extract_field(records: List[Dict[str, Any]], field_name: str) -> List[float]:
    values: List[float] = []
    for record in records:
        value = record.get(field_name)
        if value is None:
            continue
        try:
            values.append(float(value))
        except (TypeError, ValueError):
            continue
    return values


def _percentage_change(before: Optional[float], after: Optional[float]) -> Optional[float]:
    if before is None or after is None or before == 0:
        return None
    return ((after - before) / abs(before)) * 100.0


def _confidence_from_missing(activity: Dict[str, Any]) -> str:
    metadata = activity.get("metadata", {})
    summary = activity.get("summary", {})
    records = activity.get("records", [])
    required_metadata = ["schema_version", "activity_date", "sport"]
    required_summary = [
        "distance_m",
        "moving_time_s",
        "elapsed_time_s",
        "avg_speed_mps",
        "avg_pace_min_per_km",
        "calories",
    ]
    if any(metadata.get(field) is None for field in required_metadata):
        return "low"
    if any(summary.get(field) is None for field in required_summary):
        return "medium"
    if len(records) < 10:
        return "medium"
    return "high"


def classify_workout(activity: Dict[str, Any]) -> str:
    workout = activity.get("workout") or {}
    summary = activity.get("summary") or {}
    distance = _as_float(summary.get("distance_m"))
    avg_pace = _as_float(summary.get("avg_pace_min_per_km"))
    if workout.get("steps"):
        return "Structured Workout"
    if distance is not None and distance >= 24000:
        return "Long Run"
    if avg_pace is not None and avg_pace >= 7.5:
        return "Recovery Run"
    if avg_pace is not None and avg_pace <= 5.5:
        return "Threshold Run"
    if avg_pace is not None and avg_pace <= 6.5:
        return "Easy Run"
    return "Unknown"


def _generate_workout_compliance(activity: Dict[str, Any], summary: Dict[str, Any]) -> Optional[float]:
    workout = activity.get("workout") or {}
    steps = workout.get("steps") or []
    if not steps:
        return None
    target_paces = [step.get("target_pace_min_per_km") for step in steps if step.get("target_pace_min_per_km")]
    if not target_paces:
        return None
    average_target = _safe_average([float(p) for p in target_paces if p is not None])
    actual_pace = _as_float(summary.get("avg_pace_min_per_km"))
    if average_target is None or actual_pace is None or average_target == 0:
        return None
    deviation = abs(actual_pace - average_target) / average_target
    compliance = max(0.0, 100.0 - deviation * 100.0)
    return round(min(compliance, 100.0), 1)


def analyze_activity(activity: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(activity, dict):
        raise ValueError("Activity must be a JSON object.")

    issues = validate_activity_schema(activity)
    records = _normalize_records(activity.get("records", []))
    summary = activity.get("summary", {}) or {}

    workout_type = classify_workout(activity)
    pace_values = _extract_field(records, "pace_min_per_km")
    heart_rate_values = _extract_field(records, "heart_rate")
    cadence_values = _extract_field(records, "cadence_spm")
    power_values = _extract_field(records, "power")

    first_segment = _slice_segment(records, 0.0, 0.2)
    last_segment = _slice_segment(records, 0.8, 1.0)

    first_pace = _safe_average(_extract_field(first_segment, "pace_min_per_km"))
    last_pace = _safe_average(_extract_field(last_segment, "pace_min_per_km"))
    first_hr = _safe_average(_extract_field(first_segment, "heart_rate"))
    last_hr = _safe_average(_extract_field(last_segment, "heart_rate"))
    first_cadence = _safe_average(_extract_field(first_segment, "cadence_spm"))
    last_cadence = _safe_average(_extract_field(last_segment, "cadence_spm"))

    negative_split = None
    if first_pace is not None and last_pace is not None:
        negative_split = last_pace < first_pace

    fatigue_index = None
    if first_pace is not None and first_pace > 0 and last_pace is not None:
        fatigue_index = round((last_pace / first_pace) * 100.0, 1)

    hr_drift = None
    if first_hr is not None and last_hr is not None:
        hr_drift = round(last_hr - first_hr, 1)

    pace_variability = None
    if pace_values and len(pace_values) > 1:
        pace_mean = _safe_average(pace_values)
        pace_stdev = _safe_standard_deviation(pace_values)
        if pace_mean and pace_stdev is not None:
            pace_variability = round((pace_stdev / pace_mean) * 100.0, 1)

    cadence_stability = None
    if cadence_values and len(cadence_values) > 1:
        cadence_mean = _safe_average(cadence_values)
        cadence_stdev = _safe_standard_deviation(cadence_values)
        if cadence_mean and cadence_stdev is not None:
            cadence_stability = round(100.0 - (cadence_stdev / cadence_mean) * 100.0, 1)

    execution_score = _generate_workout_compliance(activity, summary)
    confidence = _confidence_from_missing(activity)

    strengths: List[str] = []
    improvements: List[str] = []
    recommendations: List[str] = []

    if workout_type == "Recovery Run":
        if summary.get("avg_pace_mpn_per_km") is None and summary.get("avg_speed_mps"):
            strengths.append("Maintained easy pace for recovery.")
    if negative_split is True:
        strengths.append("Negative split pacing shows strong finish.")
    elif negative_split is False:
        improvements.append("Pace drifted slightly later in the activity.")
    if hr_drift is not None and hr_drift <= 5:
        strengths.append("Heart rate remained stable through the session.")
    elif hr_drift is not None and hr_drift > 5:
        improvements.append("Heart rate drift suggests growing fatigue.")
    if cadence_stability is not None and cadence_stability >= 90:
        strengths.append("Running cadence remained consistent.")
    elif cadence_stability is not None and cadence_stability < 90:
        improvements.append("Cadence varied more than ideal; focus on rhythm.")

    if fatigue_index is not None and fatigue_index > 105:
        recommendations.append("Allow additional recovery after this session due to late-race fatigue.")
    if hr_drift is not None and hr_drift > 7:
        recommendations.append("Monitor aerobic effort and reduce pace if heart rate climbs excessively.")
    if cadence_stability is not None and cadence_stability < 90:
        recommendations.append("Aim for steadier cadence through the second half of the workout.")
    if execution_score is not None and execution_score < 90:
        recommendations.append("Review workout pacing to improve compliance with planned targets.")
    if not recommendations:
        recommendations.append("Continue the current training progression and maintain consistent pacing.")

    overall_assessment = (
        "The activity delivered steady execution with a balanced pacing profile." if not improvements else
        "The activity showed useful effort but could benefit from more consistent pacing and fatigue management." 
    )

    analysis: Dict[str, Any] = {
        "metadata": {
            "workout_type": workout_type,
            "confidence": confidence,
            "issues": issues,
        },
        "activity_summary": {
            "distance_m": summary.get("distance_m"),
            "moving_time_s": summary.get("moving_time_s"),
            "avg_pace_min_per_km": summary.get("avg_pace_min_per_km"),
            "avg_hr": summary.get("avg_hr"),
            "avg_cadence_spm": summary.get("avg_cadence_spm"),
            "avg_power": summary.get("avg_power"),
        },
        "workout_execution": {
            "workout_type": workout_type,
            "negative_split": negative_split,
            "workout_compliance": execution_score,
            "summary": {
                "target_pace_min_per_km": _safe_average([step.get("target_pace_min_per_km") for step in (activity.get("workout", {}).get("steps") or []) if step.get("target_pace_min_per_km")]),
                "actual_avg_pace_min_per_km": summary.get("avg_pace_min_per_km"),
            },
        },
        "physiological_response": {
            "hr_drift": hr_drift,
            "first_segment_hr": first_hr,
            "last_segment_hr": last_hr,
            "avg_power": _safe_average(power_values),
        },
        "running_mechanics": {
            "cadence_stability": cadence_stability,
            "first_segment_cadence": first_cadence,
            "last_segment_cadence": last_cadence,
        },
        "pacing": {
            "negative_split": negative_split,
            "fatigue_index": fatigue_index,
            "pace_variability_percent": pace_variability,
            "average_pace_min_per_km": summary.get("avg_pace_min_per_km"),
        },
        "historical_comparison": {
            "note": "Historical comparison requires a training history database. No history was provided.",
        },
        "trend_analysis": {
            "note": "Trend analysis could not be computed without additional activities.",
        },
        "strengths": strengths,
        "areas_for_improvement": improvements,
        "recommendations": recommendations,
        "overall_assessment": overall_assessment,
    }

    return analysis


def analyze_activity_file(activity_path: str) -> Dict[str, Any]:
    path = Path(activity_path)
    if not path.exists():
        raise FileNotFoundError(f"Activity file not found: {activity_path}")
    import json

    with path.open("r", encoding="utf-8") as handle:
        activity = json.load(handle)

    return analyze_activity(activity)

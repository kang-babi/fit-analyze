from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_METADATA_FIELDS = ["schema_version", "activity_date", "sport"]
REQUIRED_SUMMARY_FIELDS = [
    "distance_m",
    "moving_time_s",
    "elapsed_time_s",
    "avg_speed_mps",
    "max_speed_mps",
    "avg_pace_min_per_km",
    "calories",
    "avg_hr",
    "max_hr",
    "avg_cadence_spm",
    "max_cadence_spm",
    "avg_power",
    "max_power",
    "total_ascent",
    "total_descent",
]
REQUIRED_RECORD_FIELDS = [
    "timestamp",
    "distance_m",
    "speed_mps",
    "pace_min_per_km",
    "heart_rate",
    "cadence_spm",
    "power",
    "latitude",
    "longitude",
    "elevation_m",
]


def validate_activity_schema(activity: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if not isinstance(activity, dict):
        return ["Activity payload is not a JSON object."]

    metadata = activity.get("metadata")
    if not isinstance(metadata, dict):
        issues.append("Missing or invalid metadata section.")
    else:
        for field in REQUIRED_METADATA_FIELDS:
            if metadata.get(field) is None:
                issues.append(f"Missing metadata field: {field}")

    summary = activity.get("summary")
    if not isinstance(summary, dict):
        issues.append("Missing or invalid summary section.")
    else:
        for field in REQUIRED_SUMMARY_FIELDS:
            if summary.get(field) is None:
                issues.append(f"Missing summary field: {field}")

    records = activity.get("records")
    if not isinstance(records, list):
        issues.append("Missing or invalid records section.")
    else:
        if not records:
            issues.append("Records section is empty.")
        else:
            first_record = records[0]
            if isinstance(first_record, dict):
                for field in REQUIRED_RECORD_FIELDS:
                    if field not in first_record:
                        issues.append(f"Record missing field: {field}")
            else:
                issues.append("Records are not objects.")

    return issues

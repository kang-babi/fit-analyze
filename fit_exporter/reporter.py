from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def _render_list(title: str, items: List[str]) -> str:
    if not items:
        return f"{title}: None\n"
    return "\n".join([f"{title}:" ] + [f"- {item}" for item in items]) + "\n"


def format_analysis_text(analysis: Dict[str, Any]) -> str:
    metadata = analysis.get("metadata", {})
    summary = analysis.get("activity_summary", {})
    workout_execution = analysis.get("workout_execution", {})
    physiological = analysis.get("physiological_response", {})
    mechanics = analysis.get("running_mechanics", {})
    pacing = analysis.get("pacing", {})
    hist = analysis.get("historical_comparison", {})
    trend = analysis.get("trend_analysis", {})
    strengths = analysis.get("strengths", [])
    improvements = analysis.get("areas_for_improvement", [])
    recommendations = analysis.get("recommendations", [])
    assessment = analysis.get("overall_assessment", "")

    lines = [
        "# Running Activity Analysis Report",
        "",
        f"**Workout Type:** {metadata.get('workout_type', 'Unknown')}",
        f"**Confidence:** {metadata.get('confidence', 'unknown')}",
        "",
        "## Activity Summary",
        "",
        f"- **Distance:** {summary.get('distance_m', 'unknown')} m",
        f"- **Moving Time:** {summary.get('moving_time_s', 'unknown')} s",
        f"- **Average Pace:** {summary.get('avg_pace_min_per_km', 'unknown')} min/km",
        f"- **Average HR:** {summary.get('avg_hr', 'unknown')} bpm",
        f"- **Average Cadence:** {summary.get('avg_cadence_spm', 'unknown')} spm",
        "",
        "## Workout Execution",
        "",
        f"- **Negative Split:** {workout_execution.get('negative_split', 'unknown')}",
        f"- **Workout Compliance:** {workout_execution.get('workout_compliance', 'unknown')}",
        f"- **Planned Target Pace:** {workout_execution.get('summary', {}).get('target_pace_min_per_km', 'unknown')} min/km",
        "",
        "## Physiological Response",
        "",
        f"- **HR Drift:** {physiological.get('hr_drift', 'unknown')} bpm",
        f"- **Average Power:** {physiological.get('avg_power', 'unknown')} W",
        "",
        "## Running Mechanics",
        "",
        f"- **Cadence Stability:** {mechanics.get('cadence_stability', 'unknown')}%",
        f"- **First Segment Cadence:** {mechanics.get('first_segment_cadence', 'unknown')} spm",
        f"- **Last Segment Cadence:** {mechanics.get('last_segment_cadence', 'unknown')} spm",
        "",
        "## Pacing",
        "",
        f"- **Fatigue Index:** {pacing.get('fatigue_index', 'unknown')}%",
        f"- **Pace Variability:** {pacing.get('pace_variability_percent', 'unknown')}%",
        "",
        "## Historical Comparison",
        "",
        hist.get("note", "No historical data provided."),
        "",
        "## Trend Analysis",
        "",
        trend.get("note", "No trend data provided."),
        "",
        "## Strengths",
    ]
    if strengths:
        for item in strengths:
            lines.append(f"- {item}")
    else:
        lines.append("- No clear strengths identified.")
    lines.extend([
        "",
        "## Areas for Improvement",
    ])
    if improvements:
        for item in improvements:
            lines.append(f"- {item}")
    else:
        lines.append("- No major improvement areas identified.")
    lines.extend([
        "",
        "## Recommendations",
    ])
    if recommendations:
        for item in recommendations:
            lines.append(f"- {item}")
    else:
        lines.append("- Maintain current training load.")
    lines.extend([
        "",
        "## Overall Assessment",
        "",
        assessment or "No assessment available.",
        "",
    ])
    return "\n".join(lines)


def write_report(text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")

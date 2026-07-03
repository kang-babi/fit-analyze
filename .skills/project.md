# Running Activity Analysis Specification

**Version:** 1.0.0

## Purpose

This document defines the JSON schema expected by ChatGPT to perform
meaningful activity analysis and long-term trend analysis on running
activities.

The goal is not to mirror Garmin FIT files exactly, but to normalize
activity data into a platform-independent format suitable for analysis.

---

# Design Principles

The generated JSON should:

- be human-readable
- avoid Garmin-specific field names where possible
- normalize units
- preserve sufficient raw data for future analyses
- be extensible without breaking compatibility

---

# Top-Level Structure

```json
{
    "metadata": {},
    "summary": {},
    "workout": {},
    "splits": [],
    "records": [],
    "derived": {},
    "notes": {}
}
```

---

# metadata

Describes the activity itself.

## Required

| Field | Type | Description |
|--------|------|-------------|
| schema_version | string | JSON schema version |
| device | string | Watch model |
| software_version | string | Watch firmware |
| activity_date | ISO8601 | Activity start |
| sport | string | running |
| sub_sport | string/null | Garmin sub sport |
| timezone | string | Activity timezone |

Example

```json
{
    "schema_version": "1.0",
    "device": "Forerunner 165",
    "software_version": "28.05",
    "activity_date": "2026-07-03T06:18:00+08:00",
    "sport": "running"
}
```

---

# summary

Overall session statistics.

## Required

| Field | Unit |
|--------|------|
| distance_m | meters |
| moving_time_s | seconds |
| elapsed_time_s | seconds |
| avg_speed_mps | m/s |
| max_speed_mps | m/s |
| avg_pace_min_per_km | min/km |
| calories | kcal |
| avg_hr | bpm |
| max_hr | bpm |
| avg_cadence_spm | steps/min |
| max_cadence_spm | steps/min |
| avg_power | watts |
| max_power | watts |
| total_ascent | meters |
| total_descent | meters |

## Optional

Training Effect

VO2 benefit

Sweat Loss

Ground Contact Time

Stride Length

Vertical Oscillation

Temperature

---

# workout

Workout definition.

Example

```json
{
    "name": "Threshold",

    "steps": [
        {
            "type": "Warmup",
            "duration_s": 600,
            "target_pace_min_per_km": 7.67
        },
        {
            "type": "Interval",
            "duration_s": 360,
            "target_pace_min_per_km": 6.33
        },
        {
            "type": "Recovery",
            "duration_s": 120,
            "target_pace_min_per_km": 9.50
        }
    ]
}
```

This allows workout compliance analysis.

---

# splits

One object per Garmin lap.

Required

- lap number
- type
- distance
- duration
- average pace
- average HR
- max HR
- average cadence
- average power

Optional

- stride length
- vertical ratio
- GCT

---

# records

Most important section.

One object per FIT record.

Required

```json
{
    "timestamp": "...",
    "distance_m": 0,
    "speed_mps": 2.54,
    "pace_min_per_km": 6.55,
    "heart_rate": 154,
    "cadence_spm": 162,
    "power": 285,
    "latitude": 0,
    "longitude": 0,
    "elevation_m": 23.4
}
```

The more complete this section is, the better the analysis.

---

# derived

Values already calculated by the exporter.

Examples

```json
{
    "negative_split": true,

    "average_stride_length_cm": 94,

    "average_ground_contact_time_ms": 291,

    "average_vertical_ratio": 9.2
}
```

Derived values reduce repeated computation.

---

# notes

Human-entered values.

These cannot be extracted from the FIT file.

```json
{
    "rpe": 7,

    "sleep_hours": 7.5,

    "weight_kg": 71.8,

    "shoes": "Adizero SL",

    "weather": "Cloudy",

    "comments": "Second interval became difficult."
}
```

---

# Unit Conventions

Distance

meters

Time

seconds

Heart Rate

beats per minute

Cadence

steps per minute

**NOT Garmin's per-leg cadence.**

Power

watts

Pace

minutes per kilometer

Coordinates

decimal degrees

Altitude

meters

---

# Data Quality

Missing values should be

```json
null
```

Never

```json
0
```

unless zero is a legitimate measurement.

---

# Required Analyses

This schema should enable ChatGPT to compute:

- Pace consistency
- Heart rate drift
- Cadence stability
- Running economy trends
- Recovery quality
- Threshold execution
- Interval compliance
- Long run progression
- Weekly mileage
- Monthly mileage
- Training load progression
- Aerobic efficiency
- Pace vs HR improvements
- Negative/positive splits
- Segment comparisons
- Fatigue onset
- Progress toward long-term goals

without requiring access to the original FIT file.

---

# Long-Term Goal

The JSON generated from every activity should be sufficiently complete
that future analyses never require re-reading the original FIT file.
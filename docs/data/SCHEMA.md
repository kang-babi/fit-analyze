# SCHEMA.md

# Garmin FIT Exporter Data Dictionary

**Schema Version:** 1.0.0

---

# Purpose

This document defines every field that may appear in the exported JSON.

Unlike `SPECIFICATION.md`, which defines the overall structure of the
JSON document, this file documents every property individually.

Each field includes:

- Type
- Unit
- Source
- Required status
- Nullable status
- Category
- Importance
- Analysis dependencies
- Description
- Example

This document is considered the authoritative data dictionary for the
project.

---

# Field Categories

Every exported value belongs to one of four categories.

| Category    | Description                    |
| ----------- | ------------------------------ |
| Observation | Directly measured by the watch |
| Derived     | Deterministically calculated   |
| User        | Manually entered               |
| External    | Added from another source      |

---

# Importance Levels

★★★★★

Critical

Required for almost every analysis.

★★★★☆

Important

Frequently used.

★★★☆☆

Useful

Occasionally used.

★★☆☆☆

Optional

Only used by specialized analyses.

★☆☆☆☆

Low Priority

Retained for completeness.

---

# Metadata

---

## metadata.schema_version

| Property   | Value       |
| ---------- | ----------- |
| Type       | string      |
| Required   | Yes         |
| Nullable   | No          |
| Category   | Observation |
| Importance | ★★★★★       |
| Source     | Exporter    |
| Example    | `"1.0.0"`   |

### Description

Version of the exported JSON schema.

### Used By

- Validation
- Backwards compatibility

---

## metadata.activity_date

| Property   | Value       |
| ---------- | ----------- |
| Type       | ISO8601     |
| Required   | Yes         |
| Nullable   | No          |
| Category   | Observation |
| Importance | ★★★★★       |
| Source     | FIT Session |

### Description

Timestamp representing the beginning of the activity.

### Used By

- Monthly analysis
- Weekly analysis
- Trend analysis

---

## metadata.device

| Property   | Value       |
| ---------- | ----------- |
| Type       | string      |
| Required   | Recommended |
| Nullable   | Yes         |
| Category   | Observation |
| Importance | ★★★☆☆       |
| Source     | Device Info |

### Description

Running watch model.

Example

```
Forerunner 165
```

---

# Summary

---

## summary.distance_m

| Property   | Value       |
| ---------- | ----------- |
| Type       | float       |
| Unit       | meters      |
| Required   | Yes         |
| Nullable   | No          |
| Category   | Observation |
| Importance | ★★★★★       |
| Source     | Session     |

### Description

Total moving distance.

### Used By

- Weekly mileage
- Monthly mileage
- Pace
- Long run progression

---

## summary.avg_hr

| Property   | Value       |
| ---------- | ----------- |
| Type       | integer     |
| Unit       | bpm         |
| Required   | Yes         |
| Nullable   | Yes         |
| Category   | Observation |
| Importance | ★★★★★       |
| Source     | Session     |

### Description

Average heart rate.

### Used By

- HR Drift

- Aerobic Efficiency

- Threshold Analysis

- Recovery Analysis

---

## summary.avg_cadence_spm

| Property   | Value       |
| ---------- | ----------- |
| Type       | integer     |
| Unit       | steps/min   |
| Required   | Yes         |
| Nullable   | Yes         |
| Category   | Observation |
| Importance | ★★★★★       |
| Source     | Session     |

### Description

Average running cadence.

Garmin cadence must be converted to total steps/minute.

### Used By

- Cadence Stability

- Running Economy

---

## summary.avg_power

| Property   | Value       |
| ---------- | ----------- |
| Type       | integer     |
| Unit       | watts       |
| Required   | Recommended |
| Nullable   | Yes         |
| Category   | Observation |
| Importance | ★★★★☆       |

### Used By

- Running Economy

- Threshold Analysis

---

# Workout

---

## workout.steps

Array

One object per planned workout step.

Required Fields

```
type

duration_s

target_pace

target_hr

target_power
```

---

# Splits

---

## splits[]

One object per Garmin lap.

Each split should contain

- lap number

- distance

- duration

- pace

- HR

- cadence

- power

- running dynamics

---

# Records

---

## records[]

One object per FIT Record message.

This is the highest resolution data available.

The exporter should preserve every record.

Required

```
timestamp

distance_m

speed_mps

pace_min_per_km

heart_rate

cadence_spm

power

latitude

longitude

elevation_m
```

Optional

```
temperature

vertical_ratio

ground_contact_time

stride_length
```

---

# Metrics

Metrics represent calculated indicators.

Unlike Summary, Metrics describe the quality or characteristics of the
activity rather than simple observations.

---

## metrics.hr_drift

| Property   | Value   |
| ---------- | ------- |
| Type       | float   |
| Unit       | bpm     |
| Category   | Derived |
| Importance | ★★★★★   |

### Description

Difference between average HR during the second half and first half of
the activity.

### Used By

- Easy Runs

- Long Runs

---

## metrics.negative_split

| Property   | Value   |
| ---------- | ------- |
| Type       | boolean |
| Category   | Derived |
| Importance | ★★★★☆   |

### Description

True if the second half of the run is faster than the first.

---

## metrics.cadence_stability

| Property   | Value   |
| ---------- | ------- |
| Type       | float   |
| Category   | Derived |
| Importance | ★★★★☆   |

### Description

Standard deviation of cadence.

Lower indicates more consistent running mechanics.

---

## metrics.pacing_variability

| Property   | Value   |
| ---------- | ------- |
| Type       | float   |
| Unit       | %       |
| Category   | Derived |
| Importance | ★★★★★   |

### Description

Quantifies pacing consistency.

---

## metrics.workout_compliance

| Property   | Value      |
| ---------- | ---------- |
| Type       | percentage |
| Category   | Derived    |
| Importance | ★★★★★      |

### Description

Measures how closely the activity matched the planned workout.

---

# Notes

User-entered values.

Examples

```
rpe

sleep_hours

weight_kg

shoes

weather

comments
```

Category

User

These values never originate from the FIT file.

---

# Validation Rules

Every exported activity should satisfy:

✓ Schema version exists

✓ Metadata exists

✓ Summary exists

✓ Records exist

✓ Distances never decrease

✓ Timestamps remain chronological

✓ Pace is min/km

✓ Speed is m/s

✓ Cadence is total steps/minute

✓ Coordinates are decimal degrees

---

# Source Priority

When multiple values exist for the same metric, precedence is:

1. FIT File

2. Derived Calculation

3. User Override

4. External Enrichment

---

# Future Expansion

Future schema versions may introduce:

- Weather

- Air Quality

- Shoe Lifetime

- Terrain Classification

- Heart Rate Zones

- Pace Zones

- Critical Power

- Running Stress Score

without modifying existing fields.

---

# Guiding Principle

Every field should justify its existence by improving one or more of the
following:

- Coaching

- Visualization

- Trend Analysis

- Statistical Processing

- Future Extensibility

Otherwise, the field should not be exported.

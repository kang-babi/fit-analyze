# SPECIFICATION.md

# Garmin FIT Exporter JSON Specification

**Version:** 1.0.0

---

# Purpose

This document defines the canonical JSON format produced by the Garmin
FIT Exporter.

The purpose of this specification is to establish a stable,
platform-independent representation of a running activity suitable for:

- coaching
- activity analysis
- trend analysis
- visualization
- machine learning
- long-term archival

Consumers of this JSON should never require access to the original FIT
file.

---

# Guiding Principles

The exported JSON should be:

- Human readable
- Self descriptive
- Versioned
- Stable
- Platform independent
- Analysis focused

The exporter should prioritize preserving information useful for
analysis rather than reproducing every field contained within the FIT
specification.

---

# Root Object

Every exported activity consists of a single JSON object.

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

Every top-level object has a specific purpose.

---

# metadata

Describes the activity.

This object contains identifying information that remains constant for
the entire activity.

## Required

| Field          | Type    |
| -------------- | ------- |
| schema_version | string  |
| activity_date  | ISO8601 |
| sport          | string  |

## Recommended

| Field            |
| ---------------- |
| device           |
| software_version |
| timezone         |
| manufacturer     |
| sub_sport        |

Example

```json
{
  "schema_version": "1.0",

  "device": "Garmin Forerunner 165",

  "software_version": "28.05",

  "activity_date": "2026-07-03T06:12:44+08:00",

  "timezone": "Asia/Manila",

  "sport": "running",

  "sub_sport": "generic"
}
```

---

# summary

Represents aggregate statistics for the activity.

This object contains overall values rather than time-series data.

Required fields

```text
distance_m

moving_time_s

elapsed_time_s

avg_speed_mps

max_speed_mps

avg_pace_min_per_km

calories

avg_hr

max_hr

avg_cadence_spm

max_cadence_spm

avg_power

max_power

total_ascent

total_descent
```

Recommended

```text
avg_temperature

max_temperature

estimated_sweat_loss_ml

training_effect

anaerobic_training_effect

primary_benefit

avg_step_length_cm

avg_vertical_ratio

avg_vertical_oscillation_cm

avg_ground_contact_time_ms
```

Example

```json
{
  "distance_m": 6125.8,

  "moving_time_s": 2520,

  "elapsed_time_s": 2550,

  "avg_speed_mps": 2.43,

  "max_speed_mps": 4.62,

  "avg_pace_min_per_km": 6.86,

  "calories": 452,

  "avg_hr": 164,

  "max_hr": 184
}
```

---

# workout

Represents the planned workout.

If the activity was not a structured workout, this object may be empty.

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

      "target_pace_min_per_km": 9.5
    }
  ]
}
```

Workout steps should remain in chronological order.

---

# splits

Contains lap-level summaries.

One object per Garmin lap.

Required

```text
index

type

distance_m

duration_s

avg_pace_min_per_km

avg_hr

max_hr

avg_cadence_spm

avg_power
```

Recommended

```text
avg_stride_length_cm

avg_vertical_ratio

avg_ground_contact_time_ms
```

Example

```json
{
  "index": 2,

  "type": "Interval",

  "distance_m": 950,

  "duration_s": 360,

  "avg_pace_min_per_km": 6.31,

  "avg_hr": 174,

  "max_hr": 183
}
```

---

# records

The records section is the most important part of the export.

It contains one object for every FIT Record message.

Consumers should perform nearly all detailed analyses using this section.

Required fields

```text
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

Recommended

```text
temperature

vertical_ratio

ground_contact_time

stride_length
```

Example

```json
{
  "timestamp": "2026-07-03T06:17:32",

  "distance_m": 2540.2,

  "speed_mps": 2.68,

  "pace_min_per_km": 6.22,

  "heart_rate": 171,

  "cadence_spm": 168,

  "power": 297,

  "latitude": 13.1457,

  "longitude": 123.7234,

  "elevation_m": 18.3
}
```

The exporter should preserve every available record.

Do not downsample.

---

# derived

Contains deterministic values computed by the exporter.

These values reduce repeated calculations by downstream consumers.

Possible fields

```text
negative_split

positive_split

average_stride_length_cm

average_ground_contact_time_ms

average_vertical_ratio

average_running_power

average_grade

moving_percentage
```

Derived metrics should always be reproducible from the raw data.

Never include subjective values.

---

# notes

This section is intentionally user-editable.

These values cannot be extracted from the FIT file.

Example

```json
{
  "rpe": 7,

  "sleep_hours": 7.5,

  "weight_kg": 72.3,

  "shoes": "Adizero SL",

  "weather": "Cloudy",

  "comments": "Second threshold interval felt difficult."
}
```

The exporter may create this object with null values.

---

# Units

Distance

meters

---

Time

seconds

---

Speed

meters per second

---

Pace

minutes per kilometer

---

Heart Rate

beats per minute

---

Cadence

steps per minute

Never Garmin's per-leg cadence.

---

Power

watts

---

Temperature

degrees Celsius

---

Coordinates

decimal degrees

---

Elevation

meters

---

# Missing Values

Unavailable values must be represented as

```json
null
```

Never

```json
0
```

unless zero is a legitimate measurement.

---

# Ordering

Top-level objects should always appear in this order.

```text
metadata

summary

workout

splits

records

derived

notes
```

Likewise, records and splits should always be chronological.

---

# Validation Rules

An exported activity is considered valid if:

- metadata exists
- summary exists
- records contains at least one record
- timestamps are chronological
- distance is non-decreasing
- cadence is expressed in steps/minute
- pace is expressed in min/km
- coordinates are decimal degrees

---

# Compatibility

Consumers should ignore unknown fields.

Future schema versions may introduce new objects.

Existing fields should never change meaning.

Breaking changes require a major version increment.

---

# Data Retention

The exported JSON should contain sufficient information that future
analysis never requires:

- Garmin Connect

- Garmin FIT SDK

- Original FIT file

The JSON becomes the canonical representation of the activity.

---

# Summary

This specification intentionally prioritizes analytical usefulness over
perfect fidelity to the FIT protocol.

Every exported field should satisfy at least one of the following:

- improves coaching
- improves visualization
- improves statistical analysis
- improves future extensibility

Otherwise, it should not be exported.

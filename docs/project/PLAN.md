# PLAN.md

# Garmin FIT Exporter

> A platform-independent running activity exporter designed for long-term coaching, performance analysis, and trend analysis.

---

# Vision

Modern GPS watches generate an enormous amount of training data. While FIT
files contain rich information, they are:

- proprietary
- difficult to inspect manually
- tightly coupled to Garmin's internal schema
- inconvenient for downstream analysis

This project exists to bridge that gap.

Its goal is to convert Garmin FIT activity files into a normalized JSON
representation that contains everything necessary for meaningful running
analysis without requiring access to the original FIT file.

The exported JSON should remain stable even if Garmin changes the FIT
format or if activities originate from another platform in the future.

---

# Mission

Transform a proprietary binary activity file into an open,
human-readable representation suitable for:

- activity analysis
- coaching
- long-term trend analysis
- visualization
- machine learning
- statistical processing

while remaining independent of Garmin-specific implementations.

---

# Philosophy

The exporter is **not** another Garmin Connect.

It is an activity normalization engine.

The emphasis is preserving analytical value rather than reproducing every
field contained within the FIT specification.

Whenever a decision must be made, the guiding question should be:

> "Will this information improve future analysis?"

If the answer is no, the information should probably not be exported.

---

# Core Principles

## 1. Platform Independence

The exported JSON should not depend on Garmin-specific terminology.

Future exporters for Coros, Polar, Suunto, Apple Watch, or Wahoo should
be capable of generating the exact same JSON schema.

---

## 2. Human Readability

Developers should be capable of opening the JSON in any editor and
immediately understanding its contents.

Avoid:

- cryptic identifiers
- undocumented enums
- proprietary naming

Prefer:

```json
{
  "avg_hr": 152
}
```

instead of

```json
{
  "avg_heart_rate": 152
}
```

or

```json
{
  "field_103": 152
}
```

---

## 3. Stable Schema

The exported JSON is considered a public contract.

Future versions should extend the schema without breaking existing
consumers.

Versioning should follow Semantic Versioning.

---

## 4. Preserve Analytical Value

Not every FIT field deserves to be exported.

Examples:

Useful

- Heart Rate
- Cadence
- Power
- GPS Position
- Pace
- Temperature
- Running Dynamics

Probably unnecessary

- Manufacturer IDs
- Serial Numbers
- Unknown Garmin fields
- Internal developer messages

---

## 5. Derived Metrics

If a metric is deterministic and expensive to repeatedly calculate,
consider exporting it.

Examples

- pace
- cadence (steps/min)
- stride length
- HR drift
- negative split detection

This minimizes duplicated calculations during downstream analysis.

---

# Project Goals

Version 1 aims to produce sufficient information to perform meaningful
analysis without needing the original FIT file.

Specifically:

✓ Activity summary

✓ GPS records

✓ Workout structure

✓ Splits

✓ Running dynamics

✓ Heart rate

✓ Cadence

✓ Power

✓ Elevation

✓ Temperature

✓ Derived metrics

---

# Success Criteria

A successful export allows ChatGPT (or any analysis software) to answer
questions such as:

- Was this easy run executed correctly?

- Did heart rate drift during the long run?

- Was cadence consistent?

- Was pacing even?

- When did fatigue begin?

- How does this compare to previous threshold workouts?

without requiring the original FIT file.

---

# Scope

Included

- Running activities

- Garmin FIT files

- Workout definitions

- Session statistics

- Splits

- GPS records

- Running dynamics

- Derived metrics

Excluded

- Cycling

- Swimming

- Multisport

- Strength training

- Sleep

- Daily activity tracking

These may be considered future enhancements.

---

# Non-Goals

This project will NOT become:

- Garmin Connect

- Strava

- TrainingPeaks

- Golden Cheetah

- FIT SDK replacement

- Visualization software

Its responsibility ends after producing the normalized JSON.

---

# Design Decisions

The exporter intentionally separates responsibilities.

FIT File

↓

Reader

↓

Parser

↓

Activity Model

↓

Derived Metrics

↓

JSON Writer

Each layer performs exactly one responsibility.

---

# Code Quality Goals

The project should adhere to modern Python practices.

- Python 3.12+

- Type hints everywhere

- Dataclasses

- Small functions

- Single Responsibility Principle

- Minimal dependencies

- Black formatting

- Ruff linting

---

# Performance Goals

The exporter should process a typical running activity
(~10,000 records) in well under one second on modern hardware.

Memory usage should remain modest.

The exporter should stream records whenever possible.

---

# Reliability Goals

The exporter should never fail because:

- cadence is missing

- temperature is absent

- GPS temporarily drops

Missing values should become

```json
null
```

rather than causing exceptions.

---

# Extensibility

The architecture should support additional exporters.

Examples

Garmin FIT

↓

Normalized Activity

Coros FIT

↓

Normalized Activity

Apple Workout

↓

Normalized Activity

Analysis software should never know which watch created the activity.

---

# Long-Term Vision

Eventually the exporter should become a reusable library capable of
supporting multiple ecosystems.

Potential future features include:

- CSV export

- YAML export

- SQLite export

- PostgreSQL ingestion

- REST API

- CLI

- Batch processing

- Shoe tracking

- Weather enrichment

- Elevation correction

- Automatic activity classification

---

# Milestones

## Version 0.1

Project skeleton

Reader

Parser

Models

JSON writer

---

## Version 0.2

Workout parsing

Running dynamics

Derived metrics

---

## Version 0.3

Validation

Unit tests

Schema versioning

---

## Version 1.0

Stable JSON contract

Documentation

Complete CLI

Ready for long-term activity analysis.

---

# Intended Consumer

The primary consumer of the generated JSON is an analysis engine.

The analysis engine should never require access to:

- Garmin Connect

- FIT SDK

- Original FIT file

Everything necessary for meaningful coaching should already exist within
the exported JSON.

---

# Guiding Principle

> Every exported field should justify its existence by improving future
> analysis.

If a field does not contribute to analysis, visualization, or future
extensions, it should not be included.

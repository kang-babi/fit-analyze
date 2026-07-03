# CONVERTER.md

# Garmin FIT to JSON Converter Specification

Version: 1.0.0

---

# Purpose

This document defines the conversion pipeline that transforms a Garmin
FIT activity into the normalized JSON format defined by
SPECIFICATION.md.

The converter is responsible only for data extraction,
normalization, validation, and serialization.

It does not perform coaching, activity analysis, or report generation.

---

# Objectives

The converter should:

- preserve all useful running data
- normalize Garmin-specific values
- produce deterministic output
- produce human-readable JSON
- require no internet connection
- preserve chronological ordering
- support future schema versions

---

# Scope

The converter is responsible for:

- reading FIT files
- decoding FIT messages
- validating extracted data
- normalizing units
- constructing the JSON document
- exporting formatted JSON

The converter is not responsible for:

- coaching
- visualization
- report generation
- trend analysis
- recommendations

---

# Input

Accepted Input

Garmin FIT Activity

Requirements

- valid FIT file
- complete activity
- readable by the FIT SDK or compatible parser

Unsupported Inputs

- GPX
- TCX
- CSV
- JSON

Support for additional formats may be introduced in future versions.

---

# Output

Output Format

UTF-8 JSON

Encoding

UTF-8

Formatting

Pretty Printed

Indentation

4 spaces

Line Endings

LF

The generated JSON becomes the canonical representation of the activity.

---

# Conversion Pipeline

The conversion process consists of the following stages.

```
FIT File

↓

Read Binary

↓

Decode Messages

↓

Extract Data

↓

Normalize Values

↓

Validate

↓

Construct Objects

↓

Serialize JSON

↓

Write File
```

Each stage should complete successfully before continuing.

---

# Stage 1

Read FIT File

Responsibilities

Open the FIT file.

Verify readability.

Verify file integrity.

Handle read errors gracefully.

---

# Stage 2

Decode FIT Messages

Decode all available FIT message types.

Examples

File ID

Device Info

Session

Lap

Record

Event

Workout

Workout Step

Developer Fields

Unknown messages should be ignored unless they affect data integrity.

---

# Stage 3

Extract Observations

Extract all supported observations.

Examples

timestamps

distance

speed

pace

heart rate

cadence

power

GPS

elevation

temperature

running dynamics

The converter should preserve every available observation.

---

# Stage 4

Normalize Values

Convert Garmin-specific values into canonical units.

Examples

Distance

meters

Speed

meters per second

Pace

minutes per kilometer

Cadence

steps per minute

Coordinates

decimal degrees

Temperature

degrees Celsius

Elevation

meters

No Garmin-specific representations should appear in the exported JSON.

---

# Stage 5

Validation

Verify

timestamps increase chronologically

distance never decreases

required fields exist

units are normalized

records are internally consistent

Validation failures should be reported clearly.

Recoverable errors should not terminate conversion.

---

# Stage 6

Construct Objects

Populate objects in the following order.

metadata

summary

workout

splits

records

metrics

notes

Each object should conform to SPECIFICATION.md.

---

# Stage 7

Serialize JSON

Serialize using

UTF-8

Pretty Print

Deterministic ordering

No unnecessary whitespace

Output should be stable between executions.

---

# File Naming

Recommended Output

```
YYYY-MM-DD_HH-MM-SS_activity.json
```

Example

```
2026-07-03_06-14-28_threshold.json
```

Alternative naming conventions may be configured.

---

# Error Handling

Errors should be classified.

Fatal

Cannot continue conversion.

Examples

Unreadable FIT

Corrupted binary

Unsupported format

Recoverable

Conversion continues.

Examples

Missing temperature

Missing running dynamics

Unknown developer fields

Warnings should be reported.

---

# Logging

The converter should report:

file loaded

messages decoded

records extracted

warnings

errors

conversion duration

output path

Logging should assist debugging without exposing unnecessary details.

---

# Performance

The converter should:

process activities efficiently

avoid unnecessary memory allocation

stream data where practical

remain deterministic

Performance is secondary to correctness.

---

# Compatibility

The converter should tolerate:

future FIT message types

unknown developer fields

additional Garmin devices

Older FIT files should remain supported whenever practical.

---

# Determinism

The same FIT file should always produce identical JSON output.

Conversion should never depend on:

system locale

internet connectivity

system time

random values

---

# Data Preservation

The converter should preserve all observations relevant to future
analysis.

Unknown fields should be ignored unless they provide meaningful running
information.

Information should never be discarded solely because it is not currently
used by the analysis engine.

---

# Missing Values

Unavailable values should be exported as

```
null
```

Never substitute estimated values.

Never silently replace missing values with zero.

---

# Extensibility

Future schema versions may introduce:

new observations

new metrics

additional workout types

developer-specific fields

The converter should be designed to accommodate these additions with
minimal architectural changes.

---

# Testing

The converter should be verified using activities representing:

Easy Run

Recovery Run

Threshold

Interval

Long Run

Race

Structured Workout

Manual Activity

Each exported JSON should pass schema validation.

---

# Success Criteria

The converter is considered successful when:

the FIT file is fully decoded

the JSON conforms to SPECIFICATION.md

all supported observations are preserved

validation passes

output is deterministic

analysis can proceed without the original FIT file

---

# Guiding Principle

The converter exists to transform proprietary Garmin activity data into
an open, stable, analysis-focused format.

After conversion, every downstream process should rely exclusively on
the normalized JSON rather than the original FIT file.

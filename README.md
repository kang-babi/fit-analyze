# Garmin FIT Analysis

An analysis-first Garmin FIT processing pipeline for long-term running
development.

The project converts proprietary Garmin FIT activities into a stable,
human-readable JSON format and performs deterministic analysis to
produce evidence-based coaching insights.

Unlike Garmin Connect, this project focuses on long-term training
progression rather than individual activity summaries.

---

# Vision

The objective of this project is to build a complete running analysis
system capable of supporting years of endurance training.

The project is designed around four principles.

- Open data
- Deterministic analysis
- Long-term trend evaluation
- Documentation-first architecture

Every activity becomes part of a growing historical dataset that can be
analyzed consistently over time.

---

# Project Goals

- Convert Garmin FIT activities into a normalized JSON format.
- Preserve observations useful for future analysis.
- Generate reproducible activity reports.
- Support structured workout evaluation.
- Analyze long-term performance trends.
- Provide conservative, evidence-based coaching recommendations.
- Remain independent of Garmin Connect after conversion.

---

# Project Architecture

```
Garmin FIT Activity
          │
          ▼
     Converter
          │
          ▼
 Normalized JSON
          │
          ▼
 Analysis Engine
          │
          ▼
 Report Generator
          │
          ▼
 Coaching Layer
```

Each layer has a single responsibility.

The converter extracts data.

The analysis engine interprets the activity.

The report generator presents findings.

The coaching layer provides recommendations.

---

# Repository Structure

```
project/

├── docs/
│   ├── PLAN.md
│   ├── SPECIFICATION.md
│   ├── SCHEMA.md
│   ├── ANALYSIS.md
│   ├── METRICS.md
│   ├── REPORT.md
│   ├── PROMPTING.md
│   ├── ATHLETE_PROFILE.md
│   ├── COACHING.md
│   ├── CONVERTER.md
│   ├── ROADMAP.md
│   ├── CONTRIBUTING.md
│   └── CHANGELOG.md
│
├── examples/
│
├── output/
│
├── src/
│
├── tests/
│
├── README.md
└── LICENSE
```

---

# Documentation

The project is documentation-driven.

Every major architectural decision is described before implementation.

| Document           | Purpose                 |
| ------------------ | ----------------------- |
| PLAN.md            | Project vision          |
| SPECIFICATION.md   | JSON specification      |
| SCHEMA.md          | Data dictionary         |
| ANALYSIS.md        | Analysis methodology    |
| METRICS.md         | Derived metrics         |
| REPORT.md          | Report specification    |
| PROMPTING.md       | Analysis workflow       |
| ATHLETE_PROFILE.md | Athlete context         |
| COACHING.md        | Coaching philosophy     |
| CONVERTER.md       | FIT conversion pipeline |
| ROADMAP.md         | Development milestones  |
| CONTRIBUTING.md    | Development standards   |
| CHANGELOG.md       | Project history         |

---

# Analysis Philosophy

Every activity is evaluated using the same methodology.

The analysis emphasizes:

- workout execution
- physiological response
- pacing
- running mechanics
- historical comparison
- long-term trends

Individual activities are interpreted within the context of the athlete's
training history.

---

# Design Principles

The project follows several architectural principles.

## Documentation Before Code

Architecture is defined before implementation.

---

## Deterministic Output

The same activity should always produce identical results.

---

## Explainable Analysis

Every conclusion should be supported by measurable evidence.

---

## Long-Term Perspective

Training trends are more meaningful than isolated workouts.

---

## Separation of Responsibilities

Conversion, analysis, reporting, and coaching remain independent.

---

# Current Status

Documentation

Complete

Converter

Planned

Analysis Engine

Planned

Report Generator

Planned

Automation

Planned

See `ROADMAP.md` for implementation milestones.

---

# Technology

Planned implementation

Python

Primary input

Garmin FIT

Primary output

Normalized JSON

Primary use case

Running activity analysis

---

# Usage

## Export a FIT file

If you provide a filename, the command uses that file directly:

```bash
python export_fit.py export input/my_run.fit
```

If you omit the input file, the CLI prompts you to select one from `input/`:

```bash
python export_fit.py export
```

Output is written to:

```text
output/[filename]/activity.json
```

## Analyze an activity

You can analyze a FIT file or exported JSON directly:

```bash
python export_fit.py analyze input/my_run.fit
python export_fit.py analyze output/my_run/ activity.json
```

If no input is provided, the CLI prompts for a file from `input/`.

Default analysis output is written to:

```text
output/[filename]/analysis.json
```

To generate a report together with analysis:

```bash
python export_fit.py analyze input/my_run.fit --report
```

This writes the report to:

```text
output/[filename]/report.md
```

To generate a report from existing analysis or activity JSON:

```bash
python export_fit.py report output/my_run/analysis.json
```

Default report output is written to:

```text
output/[filename]/report.md
```

---

# Future Development

Planned capabilities include:

- Automatic FIT conversion
- Structured workout analysis
- Monthly summaries
- Historical trend analysis
- Visualization
- Performance metrics
- Training load analysis

---

# Contributing

Development standards are documented in `CONTRIBUTING.md`.

Meaningful architectural changes should be accompanied by corresponding
documentation updates.

---

# License

This project is released under the MIT License.

See `LICENSE` for details.

---

# Acknowledgements

This project exists because of a simple question:

_"Can running activities be analyzed independently of Garmin Connect
while producing more transparent, explainable, and long-term coaching
insights?"_

This repository is the answer to that question.

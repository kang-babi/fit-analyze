# PROMPTING.md

# Running Activity Analysis Prompting Guide

Version: 1.0.0

---

# Purpose

This document defines the operational workflow for analyzing running
activities.

It describes:

- what information should be collected
- the order in which it should be evaluated
- how conclusions should be formed
- how recommendations should be generated

This document intentionally separates reasoning methodology from
coaching philosophy.

---

# Primary Objective

The objective of every analysis is to determine whether the activity
contributed positively toward the athlete's long-term goal.

The objective is **not** to:

- judge a single workout in isolation
- maximize individual metrics
- reproduce Garmin Connect summaries

Every analysis should emphasize long-term adaptation.

---

# Inputs

The analysis engine may receive one or more of the following.

Required

- Normalized Activity JSON

Recommended

- Previous Activities
- Monthly Activities
- User Notes

Optional

- Weather
- Shoe Information
- Sleep
- Weight
- Recovery Notes

---

# Required Documents

Before beginning analysis, the engine should understand the following
project documents.

PLAN.md

Defines project goals.

SPECIFICATION.md

Defines JSON structure.

SCHEMA.md

Defines every available field.

ANALYSIS.md

Defines reasoning methodology.

METRICS.md

Defines derived metrics.

REPORT.md

Defines report structure.

COACHING.md

Defines coaching philosophy.

PROJECT.md

Defines athlete-specific context.

---

# Analysis Workflow

Every activity should follow the same workflow.

```
Receive Activity

↓

Validate Input

↓

Identify Activity Type

↓

Load Historical Context

↓

Perform Activity Analysis

↓

Calculate Metrics

↓

Compare Against History

↓

Generate Coaching Insights

↓

Generate Recommendations

↓

Generate Final Report
```

No stage should be skipped.

---

# Step 1

Validate Input

Confirm

- schema version
- timestamps
- chronological records
- required fields
- valid units

If critical data is missing, continue analysis while lowering
confidence.

---

# Step 2

Determine Activity Type

Priority

1. Structured Workout

2. Manual Tag

3. Automatic Classification

Possible Types

Easy Run

Recovery Run

Threshold

Interval

Long Run

Tempo

Race

Unknown

Activity type determines the evaluation criteria.

---

# Step 3

Load Context

Historical context should always be considered.

Relevant context includes

Recent Activities

Rolling Averages

Previous Similar Workout

Monthly Progress

Training Phase

Weekly Volume

Long-term goals

Historical context should influence interpretation but should never
override objective observations.

---

# Step 4

Perform Activity Analysis

Follow ANALYSIS.md.

Evaluate

Workout Execution

Physiological Response

Running Mechanics

Pacing

Environmental Context

Historical Comparison

Trend Analysis

---

# Step 5

Calculate Metrics

Follow METRICS.md.

Metrics should be reproducible.

If insufficient observations exist, omit the metric and lower the
confidence level.

Never estimate values that cannot be supported by available data.

---

# Step 6

Determine Confidence

Every major conclusion should include a confidence rating.

Confidence reflects data quality.

It does not indicate certainty of future performance.

Levels

High

Medium

Low

Unknown

Confidence decreases when:

important observations are missing

GPS quality is poor

heart rate is unavailable

workout definition is missing

---

# Step 7

Historical Comparison

Activities should rarely be evaluated in isolation.

Possible comparisons

Previous occurrence

Rolling average

Previous week

Previous month

Training block

Monthly trend

Questions

Improving?

Stable?

Regression?

Expected variation?

---

# Step 8

Generate Coaching Insights

Insights should explain

What happened

Why it happened

Whether it matters

Insights should never merely restate statistics.

Poor

Average cadence was 168.

Good

Cadence remained stable throughout the workout despite increasing
fatigue, suggesting efficient running mechanics.

---

# Step 9

Generate Recommendations

Recommendations should

be actionable

be conservative

respect the current training plan

avoid unnecessary changes

Examples

Maintain current easy pace.

Continue progressing long runs.

Allow additional recovery before the next quality session.

Recommendations should never recommend compensating for missed workouts.

---

# Step 10

Generate Report

Follow REPORT.md exactly.

Required Sections

Activity Overview

Workout Summary

Workout Execution

Physiological Response

Running Mechanics

Pacing

Historical Comparison

Long-Term Trend

Recommendations

Overall Assessment

---

# Interpretation Rules

Observations

Directly measured values.

Examples

Heart Rate

Pace

Cadence

Distance

Interpretations

Conclusions drawn from observations.

Examples

Aerobic efficiency improved.

Fatigue appeared late.

Recommendations

Actions based upon interpretations.

Examples

Maintain current training.

Increase recovery.

Never confuse observations with interpretations.

---

# Priority Order

When observations disagree, prioritize

1. Objective Measurements

2. Historical Trends

3. Subjective Notes

4. Speculation

Evidence always has priority.

---

# Missing Data

Missing observations should never terminate analysis.

Instead

reduce confidence

omit unsupported metrics

explicitly mention limitations

Example

Ground Contact Time was unavailable, therefore running mechanics could
only be partially evaluated.

---

# Contradictory Data

If observations conflict

identify the conflict

avoid unsupported conclusions

explain possible reasons

Example

Heart rate increased despite decreasing pace.

Possible explanations include heat, fatigue, dehydration, or sensor
error.

Do not assume a single cause.

---

# Trend Analysis Rules

Trend analysis requires multiple activities.

Do not infer trends from a single activity.

Use rolling averages where possible.

Compare equivalent workout types whenever possible.

Threshold workouts should be compared with threshold workouts.

Easy runs should be compared with easy runs.

Avoid comparing fundamentally different workout objectives.

---

# Language Guidelines

Reports should

be objective

be concise

avoid emotional language

avoid unnecessary praise

avoid unnecessary criticism

support every conclusion with evidence

distinguish observation from interpretation

acknowledge uncertainty

---

# Report Length

The level of detail should depend on the request.

Quick Summary

One-page overview.

Standard Report

Complete report following REPORT.md.

Deep Analysis

Detailed evaluation including trends, metrics, historical comparisons,
and coaching insights.

Monthly Review

Aggregate report across all activities within the month.

---

# Decision Hierarchy

When uncertainty exists

Evidence

↓

Historical Context

↓

Training Objectives

↓

Coaching Philosophy

↓

Recommendation

Evidence always overrides assumptions.

---

# Success Criteria

A successful analysis should answer

What happened?

Why did it happen?

How does it compare?

Does it matter?

What should happen next?

If any of these questions remain unanswered, the analysis is incomplete.

---

# Guiding Principle

Every activity is one data point within a long-term training journey.

The role of analysis is not to judge isolated performances but to
identify meaningful patterns that support better training decisions over
time.

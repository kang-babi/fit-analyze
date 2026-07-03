# ANALYSIS.md

# Running Activity Analysis Methodology

Version: 1.0.0

---

# Purpose

This document defines how an activity should be analyzed once it has
been converted into the normalized JSON schema.

It does not describe:

- Garmin FIT parsing
- JSON generation
- Data collection

Instead, it describes the reasoning process used to evaluate a running
activity.

The primary objective is to evaluate execution quality, identify trends,
and provide actionable coaching insights.

---

# Guiding Principles

Every analysis should:

- prioritize long-term trends over isolated activities
- distinguish observations from interpretations
- quantify uncertainty when data is incomplete
- avoid overreacting to single poor sessions
- compare against historical activities whenever possible

The goal is coaching rather than reporting.

---

# Analysis Pipeline

Every activity should be processed using the following stages.

```

Load Activity

↓

Validate Schema

↓

Identify Workout Type

↓

Evaluate Workout Execution

↓

Evaluate Physiological Response

↓

Evaluate Running Mechanics

↓

Evaluate Pacing

↓

Compare Against Historical Activities

↓

Generate Coaching Insights

↓

Generate Recommendations

```

Each stage builds upon the previous one.

---

# Workout Classification

Before analysis begins, the activity should be classified.

Possible workout types include:

- Easy Run
- Recovery Run
- Long Run
- Threshold Run
- Tempo Run
- Interval Session
- Progression Run
- Race
- Unknown

Workout classification may originate from:

1. Structured workout
2. Manual tag
3. Automatic detection

---

# General Evaluation Framework

Every workout should answer five questions.

## 1.

Did the athlete execute the planned workout?

---

## 2.

How did the athlete respond physiologically?

---

## 3.

How consistent was the execution?

---

## 4.

Were there signs of excessive fatigue?

---

## 5.

How does this compare with previous activities?

---

# Easy Run Analysis

Purpose

Develop aerobic capacity while minimizing fatigue.

Primary Evaluation

- pace discipline
- HR stability
- cadence consistency
- aerobic efficiency

Questions

Was the pace comfortably controlled?

Did heart rate remain aerobic?

Did HR drift significantly?

Was cadence stable?

Was running form maintained?

Outputs

- Easy Run Score
- HR Drift
- Aerobic Efficiency
- Pacing Consistency
- Cadence Stability

---

# Recovery Run Analysis

Purpose

Promote recovery while maintaining movement.

Priority

Heart rate is more important than pace.

Indicators

- low HR
- relaxed pace
- smooth cadence

Warnings

- elevated HR
- excessive pace
- high power output

---

# Long Run Analysis

Purpose

Develop endurance.

Primary Metrics

- pacing
- fatigue
- HR drift
- cadence degradation

Questions

Did pace deteriorate?

Did cadence fall?

Did HR continue climbing?

Where did fatigue begin?

Outputs

- Fatigue Index
- Aerobic Decoupling
- HR Drift
- Negative Split Detection

---

# Threshold Analysis

Purpose

Increase sustainable pace.

Primary Metrics

- workout compliance
- pace consistency
- HR response
- recovery quality

Questions

Was target pace achieved?

Was recovery sufficient?

Did pace fade?

Did HR rise excessively?

Outputs

- Threshold Execution
- Interval Consistency
- Recovery Quality
- Fatigue Onset

---

# Interval Analysis

Purpose

Improve speed and VO₂max.

Evaluate

- interval consistency
- recovery quality
- power repeatability

Questions

Were intervals completed?

Did pace decrease?

Did HR recover?

Did cadence remain stable?

Outputs

- Compliance Score
- Interval Degradation
- Recovery Score

---

# Race Analysis

Priority

Performance.

Questions

Did pacing match strategy?

Where was the fastest segment?

Where was fatigue observed?

Were splits negative?

Outputs

- Race Execution
- Pacing Score
- Finish Strength

---

# Physiological Analysis

Evaluate

- average HR
- maximum HR
- HR drift
- aerobic decoupling
- recovery rate

Interpretation

Higher HR is not inherently good or bad.

Heart rate should always be interpreted relative to:

- pace
- workout objective
- historical data

---

# Running Mechanics

Evaluate

- cadence
- stride length
- vertical ratio
- vertical oscillation
- ground contact time

Questions

Did mechanics deteriorate?

Were mechanics consistent?

Did fatigue alter running form?

---

# Pacing Analysis

Evaluate

- average pace
- pace variability
- pace distribution
- split consistency

Questions

Was pacing controlled?

Were there surges?

Was execution even?

---

# Workout Compliance

Applicable only when a structured workout exists.

Each workout step should be evaluated individually.

Example

Warmup

Target

7:40/km

Actual

7:42/km

Compliance

98%

Interval

Target

6:20/km

Actual

6:18/km

Compliance

99%

Recovery

Target

9:30/km

Actual

9:10/km

Compliance

84%

Overall workout compliance should be reported.

---

# Historical Comparison

Activities should never be analyzed in isolation.

Compare against:

Previous occurrence

Previous week

Previous month

Same workout type

Rolling averages

Trend analysis has higher priority than isolated performance.

---

# Trend Analysis

Monitor changes in:

- easy pace
- threshold pace
- cadence
- aerobic efficiency
- HR drift
- long run duration
- weekly mileage
- monthly mileage

Identify:

Improvement

Plateau

Regression

---

# Confidence

Every conclusion should include a confidence level.

High

Complete data.

Medium

Minor missing values.

Low

Important measurements unavailable.

Unknown

Unable to determine.

---

# Recommendations

Recommendations should always prioritize:

1. Safety

2. Recovery

3. Long-term consistency

Recommendations should never encourage compensating for missed workouts.

Recommendations should avoid drastic training changes based on a single activity.

---

# Analysis Output Structure

Every activity analysis should contain:

Activity Summary

Workout Execution

Physiological Response

Running Mechanics

Pacing

Historical Comparison

Trend Analysis

Strengths

Areas for Improvement

Recommendations

Overall Assessment

---

# Guiding Philosophy

Every analysis should answer one question:

"Did this activity move the athlete closer to their long-term goal?"

The purpose of analysis is not to judge individual workouts but to
understand how each activity contributes to long-term adaptation.

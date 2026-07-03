# METRICS.md

# Running Activity Metrics Reference

Version: 1.0.0

---

# Purpose

This document defines every derived metric used during activity
analysis.

Unlike observations directly recorded by the watch, metrics are
calculated from one or more observations.

Every metric should be:

- deterministic
- reproducible
- explainable
- independent of Garmin proprietary algorithms

---

# Metric Classification

Metrics are grouped into the following domains.

## Execution

Measures how well the planned workout was performed.

Examples

- Workout Compliance
- Interval Consistency
- Recovery Compliance

---

## Physiological

Measures the body's response.

Examples

- Heart Rate Drift
- Aerobic Decoupling
- Recovery Rate

---

## Mechanical

Measures running form.

Examples

- Cadence Stability
- Ground Contact Consistency
- Vertical Oscillation

---

## Pacing

Measures speed control.

Examples

- Pace Variability
- Negative Split
- Even Pace Score

---

## Training Load

Measures accumulated stress.

Examples

- Weekly Mileage
- Longest Run
- Intensity Distribution

---

# Metric Definition Template

Every metric should contain:

- Purpose
- Formula
- Inputs
- Unit
- Range
- Interpretation
- Confidence
- Dependencies

---

# Workout Compliance

Category

Execution

Purpose

Measures how closely the athlete followed the planned workout.

Inputs

- workout.steps
- records

Formula

Average compliance of every workout segment.

Range

0–100%

Interpretation

100%

Perfect execution.

90–99%

Excellent.

80–89%

Acceptable.

Below 80%

Poor execution.

Dependencies

Workout definition required.

---

# Pace Variability

Category

Pacing

Purpose

Measure pacing consistency.

Inputs

- records.speed
- records.pace

Formula

Coefficient of variation of pace.

Interpretation

Lower values indicate smoother pacing.

High values suggest surging or inconsistent effort.

---

# Negative Split

Category

Pacing

Purpose

Determine whether the second half of the run was faster.

Inputs

- records

Formula

Average pace (second half)

compared against

Average pace (first half)

Output

Boolean

Additional Output

Percentage improvement.

Interpretation

True

Finished stronger.

False

Finished slower.

---

# Heart Rate Drift

Category

Physiological

Purpose

Estimate aerobic fatigue.

Inputs

- heart rate
- elapsed time

Formula

Average HR (second half)

minus

Average HR (first half)

Unit

bpm

Interpretation

Small drift

Excellent aerobic endurance.

Large drift

Possible fatigue or excessive intensity.

Confidence

High if complete HR data exists.

---

# Aerobic Decoupling

Category

Physiological

Purpose

Measure relationship between pace and heart rate.

Inputs

- pace
- HR

Output

Percentage

Interpretation

Smaller values indicate stronger aerobic efficiency.

---

# Recovery Rate

Category

Physiological

Purpose

Evaluate heart rate recovery.

Inputs

- recovery intervals

Formula

Peak HR

minus

HR after recovery interval

Interpretation

Larger decreases generally indicate better recovery.

---

# Fatigue Onset

Category

Physiological

Purpose

Estimate when fatigue first became observable.

Indicators

- HR drift
- cadence decrease
- pace decrease
- power decrease

Output

Timestamp

Distance

Confidence

Low

Medium

High

---

# Cadence Stability

Category

Mechanical

Purpose

Measure cadence consistency.

Inputs

Cadence records.

Formula

Standard deviation.

Interpretation

Lower values indicate smoother mechanics.

---

# Stride Stability

Category

Mechanical

Purpose

Measure consistency of stride length.

Inputs

Stride Length

Interpretation

Lower variability generally indicates stable mechanics.

---

# Vertical Oscillation Consistency

Category

Mechanical

Purpose

Evaluate upper body stability.

Inputs

Vertical Oscillation

Interpretation

Large variation may indicate fatigue.

---

# Ground Contact Stability

Category

Mechanical

Purpose

Evaluate consistency of ground contact.

Interpretation

Increasing contact time often accompanies fatigue.

---

# Easy Run Score

Composite Metric

Purpose

Summarize execution quality of an easy run.

Components

- HR Drift
- Pace Stability
- Cadence Stability
- Aerobic Efficiency

Output

0–100

---

# Threshold Score

Composite Metric

Purpose

Evaluate threshold workout quality.

Components

Workout Compliance

Recovery Quality

Pace Consistency

HR Response

Fatigue

Output

0–100

---

# Interval Score

Composite Metric

Purpose

Evaluate interval session quality.

Components

Compliance

Recovery

Consistency

Execution

Output

0–100

---

# Long Run Score

Composite Metric

Purpose

Evaluate endurance sessions.

Components

HR Drift

Fatigue

Cadence

Pacing

Negative Split

Output

0–100

---

# Weekly Metrics

Calculated from multiple activities.

Examples

Weekly Mileage

Average Easy Pace

Average Threshold Pace

Average Cadence

Longest Run

Training Load

Intensity Distribution

---

# Monthly Metrics

Calculated from an entire month.

Examples

Total Mileage

Training Frequency

Longest Run

Average Recovery Days

Training Distribution

Workout Type Distribution

---

# Trend Metrics

Require historical activities.

Examples

Easy Pace Trend

Threshold Pace Trend

Cadence Trend

Power Trend

Heart Rate Trend

Running Economy Trend

---

# Confidence Levels

Every metric should include a confidence value.

High

All required observations available.

Medium

Minor observations missing.

Low

Important observations missing.

Unknown

Cannot be calculated.

---

# Composite Metrics

Composite metrics should always expose:

Overall Score

Individual Component Scores

Weighting

Confidence

No composite metric should hide its calculation.

---

# Design Principles

Metrics should never:

- depend on Garmin proprietary scores
- require cloud services
- require internet access
- require machine learning

Metrics should always be reproducible from the exported JSON.

---

# Future Metrics

Potential additions include:

- Running Economy Index
- Efficiency Factor
- Training Monotony
- Acute:Chronic Workload Ratio
- Critical Speed
- Pace Reserve
- Heat Adjustment
- Humidity Adjustment
- Terrain Difficulty Index
- Recovery Readiness
- Race Prediction

These additions should not require changes to the existing schema.

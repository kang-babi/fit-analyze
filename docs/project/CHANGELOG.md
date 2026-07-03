# CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

This project follows the principles of
[Keep a Changelog](https://keepachangelog.com/)
and
[Semantic Versioning](https://semver.org/).

The changelog records meaningful architectural, functional, and
documentation changes.

Minor formatting changes, refactoring without behavioral impact, and
other trivial modifications should generally not appear here.

---

# [Unreleased]

## Planned

### Converter

- Implement Garmin FIT parser.
- Normalize activity observations.
- Export canonical JSON.

### Analysis Engine

- Calculate derived metrics.
- Analyze structured workouts.
- Generate standardized reports.

### Testing

- Add unit tests.
- Add regression tests.
- Validate schema compliance.

---

# [1.0.0] - Initial Release

## Added

### Project Documentation

- Added project vision (`PLAN.md`).
- Added JSON specification (`SPECIFICATION.md`).
- Added schema reference (`SCHEMA.md`).
- Added activity analysis methodology (`ANALYSIS.md`).
- Added metrics reference (`METRICS.md`).
- Added report specification (`REPORT.md`).
- Added prompting workflow (`PROMPTING.md`).
- Added athlete profile (`ATHLETE_PROFILE.md`).
- Added coaching philosophy (`COACHING.md`).
- Added converter specification (`CONVERTER.md`).
- Added project roadmap (`ROADMAP.md`).
- Added contribution guide (`CONTRIBUTING.md`).

### Architecture

- Defined documentation-first development workflow.
- Defined normalized JSON format.
- Separated conversion, analysis, reporting, and coaching into distinct layers.
- Established deterministic conversion pipeline.
- Established standardized reporting structure.

### Standards

- Adopted Semantic Versioning.
- Adopted deterministic JSON output.
- Established documentation as the primary source of truth.

---

# Changelog Categories

The following categories should be used where appropriate.

## Added

New functionality.

---

## Changed

Behavioral changes.

---

## Deprecated

Features scheduled for removal.

---

## Removed

Deleted functionality.

---

## Fixed

Bug fixes.

---

## Security

Security improvements.

---

## Documentation

Meaningful documentation changes.

---

## Performance

Performance improvements that affect observable behavior.

---

## Refactoring

Architectural improvements without changing behavior.

Use sparingly.

---

# Versioning Policy

The project follows Semantic Versioning.

Major

Breaking architectural or behavioral changes.

Minor

Backward-compatible functionality.

Patch

Bug fixes, documentation improvements, and minor corrections.

---

# Release Checklist

Before publishing a release, verify:

✓ Documentation updated.

✓ Changelog updated.

✓ Version number updated.

✓ Tests pass.

✓ JSON schema validated.

✓ Examples updated.

✓ README reviewed.

---

# Guiding Principle

The changelog should explain the evolution of the project rather than
repeat the Git commit history.

Every entry should help future maintainers understand what changed,
why it changed, and how it affects the project.

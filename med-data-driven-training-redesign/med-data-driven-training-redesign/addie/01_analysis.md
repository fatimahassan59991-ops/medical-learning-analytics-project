# ADDIE Phase 1: Analysis

## The Course Being Redesigned

**Psychiatric Interviewing & Mental Status Examination** — a mandatory
module taken by all students at the fictional medical school used across
this GitHub's related projects. In its current form, it's a single 6-hour
digital workbook completed in one sitting.

## Performance Gap Analysis

This redesign starts from evidence, not a hunch. In the companion project
*Medical Student Behavioral-Health Training Effectiveness & Learning
Analytics*, analyzing a full year of training data found:

- **Completion rate: 58.9%** — the lowest of any module in the curriculum.
- **Average learning gain: 6.5 points** (post-test minus pre-test) — also
  the lowest in the curriculum, versus 17+ points for short gamified
  microlearning modules covering similarly mandatory behavioral-health
  material.
- **Satisfaction: 2.58 / 5** — well below the 4.0+ scores short-format
  modules received.
- **Campus was not the driver.** Completion rates were nearly flat across
  all five teaching campuses (within about 5.5 points of each other), which
  rules out "one campus just isn't engaged" as the explanation.

A second project, a randomized controlled experiment (*Training A/B Test:
Microlearning vs. Traditional Training*), tested the underlying cause
directly on a different required module (*Suicide Risk Assessment & Safety
Planning*) and confirmed it: switching identical content from one long
sitting to short spaced-out modules produced a 25.7 percentage-point jump
in completion and a statistically significant gain in assessment scores.
Format is the cause, not a coincidence.

**The gap this module needs to close:** get completion and learning gain up
to what the short-format behavioral-health modules already achieve (96%+
completion, 17+ point gain), without reducing what students actually walk
away able to do with a real patient.

## Learner Analysis

- **Audience:** Medical students across all four class years (M1–M4), all
  five teaching campuses. This is a broad audience with mixed clinical
  exposure, not a group of specialists.
- **Prior knowledge:** Mixed. M1 and M2 students are typically encountering
  structured psychiatric interviewing for the first time in a formal way;
  M3 and M4 students have some clinical rotation exposure already but still
  take this as an annual required module. That mix argues for a design that
  doesn't assume zero prior exposure, but also doesn't assume clinical
  fluency.
- **Context of access:** Students complete this training around clinical
  rotations, lectures, and study time — a schedule with very little
  protected open time. A single 6-hour block is difficult to protect on a
  real calendar; short sessions are far more realistic to fit in between
  clinic days.
- **Motivation:** This module is mandatory but easy to under-value relative
  to boards prep and rotation demands. Design needs to respect students'
  time and make the clinical relevance — this is a skill they will use with
  a real, possibly at-risk patient — immediately clear, rather than leading
  with policy or accreditation language.

## Task / Content Analysis

The current 6-hour module bundles four distinct skills into one continuous
workbook with a single exam at the end:

1. Building rapport and structuring a psychiatric interview
2. Performing the core components of a Mental Status Examination (MSE)
3. Asking safety and risk-assessment questions appropriately
4. Documenting findings in a structured note

These four skills don't depend on each other in a strict sequence — a
student doesn't need to master MSE terminology before learning how to ask a
risk-assessment question. That independence is exactly what makes this
content a good candidate for modularization: it can be broken into
self-contained pieces without breaking any instructional sequence.

## Context Analysis

- **Delivery environment:** The medical school's LMS (the same platform
  already used for the other mandatory behavioral-health modules),
  accessible on desktop and mobile.
- **Constraint:** The redesign must keep the same accreditation and
  curriculum content requirements as the original module — nothing required
  is being cut, only restructured and paced differently.
- **Timeline:** Annual mandatory training tied to accreditation
  requirements, so there's a fixed compliance deadline each year that the
  rollout plan (see `04_implementation.md`) needs to work backward from.

## Root Cause Statement

Students aren't failing to complete or retain this training because the
content is too hard or because one campus doesn't care. They're
under-completing and under-learning a single unbroken 6-hour workbook that
doesn't fit into a real rotation schedule and doesn't give them anywhere to
stop, resume, or check their understanding along the way. The fix is
structural, not motivational — which is what makes the plan in
`02_design.md` actionable.

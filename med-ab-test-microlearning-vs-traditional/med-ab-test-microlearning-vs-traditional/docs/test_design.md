# Test Design: Microlearning vs. Traditional Training

This document lays out the experiment the way I'd write it up before running
it — the hypothesis, how students were assigned to groups, how big the
sample needed to be, and what would count as a real result versus noise.

## Background

A companion project on this GitHub (*Medical Student Behavioral-Health
Training Effectiveness & Learning Analytics*) found, by observing existing
training data, that long single-sitting digital-workbook modules had much
lower completion rates than short microlearning modules covering similar
mandatory behavioral-health content. That finding was observational — it
showed a strong pattern, but not proof that switching a module's format
would actually cause better outcomes, since other differences between
modules could have explained it.

This experiment tests that directly: take one required module, hold the
content constant, and change only the delivery format, with students
randomly assigned to one version or the other. A controlled experiment like
this is the only way to say the format itself — not something else about
the module — caused the difference.

## Hypothesis

- **H0 (null):** Completion rate and post-training assessment scores are the
  same whether the module is delivered as one traditional 3-hour module or
  as six 30-minute microlearning modules.
- **H1 (alternative):** The microlearning format produces a higher
  completion rate and higher assessment scores than the traditional format.

## Groups

- **Control (Group A):** *Suicide Risk Assessment & Safety Planning*
  delivered as a single 3-hour, self-paced eLearning module, completed in
  one sitting.
- **Treatment (Group B):** The same content, restructured into six
  30-minute microlearning modules, released over two weeks with a short
  knowledge check after each module.

This module was chosen deliberately: recognizing and responding to suicide
risk is a required competency across medical school curricula, and it is
exactly the kind of high-stakes, easy-to-under-teach content where format
matters — students need to retain and be able to act on it, not just click
through it.

## Randomization

600 medical students were randomly assigned to Control or Treatment,
**stratified by teaching campus** — meaning the random split happened
separately within each campus, so both groups end up with almost the same
campus mix by construction rather than by luck. This matters because it
rules out "maybe Treatment just happened to get more students from one
campus" as an alternative explanation for any difference found later.

Before looking at any outcome, the two groups' **pre-test scores** (measured
before either group started training) were compared as a balance check. If
randomization worked, there should be no meaningful difference — and there
wasn't (see `scripts/analyze.py` output: p = 0.067, not significant).

## Sample size

Using a standard two-proportion power calculation, detecting a jump in
completion rate from a 70% baseline to 85% (a 15-point improvement), at a
5% significance level and 80% power, requires about 118 students per group:

```
n = (z_(a/2) + z_beta)^2 * [p1(1-p1) + p2(1-p2)] / (p1-p2)^2
n = (1.96 + 0.84)^2 * [0.70(0.30) + 0.85(0.15)] / (0.15)^2
n ≈ 118 per group
```

This experiment used 300 per group — well above that minimum — so it has
strong power to detect not just a 15-point difference but a substantially
smaller one too.

## Metrics

- **Primary:** completion rate (did the student finish the module?)
- **Secondary:** post-test score and learning gain (post-test minus
  pre-test), satisfaction score, assessment attempts, and calendar days to
  complete.

## How Success Is Judged

A result counts as a real effect, not noise, if the 95% confidence interval
for the difference between groups doesn't cross zero (equivalently, p <
0.05). `scripts/analyze.py` runs the actual tests: a two-proportion z-test
for completion rate, an independent-samples t-test with Cohen's d for
post-test scores, and a Mann-Whitney U test for satisfaction (an ordinal
1–5 scale, which a t-test isn't the right tool for).

## Result Summary

All three outcomes came back statistically significant and in the
hypothesized direction: completion rate was 25.7 points higher in Treatment
(93.3% vs. 67.7%, p < 0.001), post-test scores were 5.5 points higher
(Cohen's d = 0.36, a small-to-moderate effect), and satisfaction was
sharply higher (median 4.5 vs. 3.0, p < 0.001). See `README.md` and
`scripts/analyze.py`'s printed output for the full numbers, and
`charts/5_effect_size_summary.png` for the confidence intervals at a
glance.

One honest nuance: Treatment took longer in calendar days to finish (12.4
vs. 5.1 days) — expected, since it's spread over two weeks by design — so
"microlearning is better" isn't true on literally every metric. For a
required competency like suicide risk assessment, though, a few extra
calendar days is a reasonable trade for a much higher chance students
actually finish the training and retain the material.

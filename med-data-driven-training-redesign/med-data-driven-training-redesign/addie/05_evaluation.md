# ADDIE Phase 5: Evaluation

## Framework: Kirkpatrick's Four Levels

| Level | What It Measures | How It's Measured Here |
|---|---|---|
| 1. Reaction | Did students like the training? | Satisfaction score after each module (same field used across every project in this series) |
| 2. Learning | Did they actually learn the material? | Pre-test vs. post-test score, by module and overall |
| 3. Behavior | Do they apply it clinically? | Standardized-patient exam (OSCE) performance and clinical preceptor evaluations in the months following training (owned by the clerkship/OSCE team, outside this project's data scope, but named here as the next measurement layer) |
| 4. Results | Did it move a curriculum outcome? | Completion rate and, longer-term, OSCE pass rates on psychiatric-interview stations |

Levels 1 and 2 are directly measurable with the same data structure and
tools already built in this project series; Levels 3 and 4 require
operational data this project doesn't have access to, but the evaluation
plan names exactly what to track and where it would come from.

## Reusing the Existing Analysis Pipeline

This is the payoff of building the earlier two projects with reusable SQL
and Python: evaluating the redesign doesn't require new tooling.

- The **SQL queries and Python analysis script** from *Medical Student
  Behavioral-Health Training Effectiveness & Learning Analytics*
  (completion rate by module, learning gain by module, satisfaction by
  completion status) get pointed at the redesigned module's data after
  launch. Success looks like: completion rate and learning gain for the
  redesigned module landing near the 96% completion / 17+ point gain
  benchmark the short-format behavioral-health modules already hit — not
  just "better than before."
- The **statistical testing approach** from *Training A/B Test:
  Microlearning vs. Traditional Training* (two-proportion z-test for
  completion, t-test with Cohen's d for scores) is exactly the right tool
  if the school wants to run a true before/after or pilot-vs-control
  comparison rather than just eyeballing the new numbers — the same
  scripts apply with a new dataset.

## Success Criteria

The redesign is considered successful if, after the pilot phase:

- Completion rate rises from the baseline 58.9% to at least 90%.
- Average learning gain rises from 6.5 points to at least 14 points.
- Satisfaction rises from 2.58 to at least 4.0 out of 5.
- No required accreditation content is found missing in the SME/QA review.

These aren't arbitrary targets — they're the same numbers the short-format
behavioral-health modules already achieve in the existing data, which is
the proof that this level of performance is realistically reachable with
this population and this content, not an aspirational guess.

## What Happens If the Pilot Falls Short

If pilot data doesn't hit these targets, the item-level assessment data
(tracked per module, not just overall) makes it possible to find exactly
which module is underperforming, rather than scrapping the whole redesign.
That's one more reason five short, separately-measured modules are a better
design than one long module: a problem in one module doesn't hide inside an
overall pass rate.

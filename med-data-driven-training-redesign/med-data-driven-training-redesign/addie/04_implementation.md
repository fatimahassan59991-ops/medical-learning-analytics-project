# ADDIE Phase 4: Implementation

## Rollout Plan

**Phase 1 — Pilot (Weeks 1–2).** Launch the five-module redesign with one or
two teaching campuses rather than the whole school at once, following the
same campus-level breakdown already used in the analysis. A pilot group
around 100–150 students is large enough to see a real completion-rate and
score signal without betting the full rollout on an untested build.

**Phase 2 — Review (Week 3).** Pull completion, score, and satisfaction data
from the pilot group using the same SQL queries and Python analysis script
built for the original data project, and compare against the pilot group's
historical numbers on the old 6-hour version. Fix anything the QA checklist
or pilot data surfaces.

**Phase 3 — School-wide launch (Weeks 4–6).** Roll out to all remaining
campuses in waves rather than all at once, so the LMS and curriculum support
team aren't handling every question on the same day.

## Communication Plan

- **To students:** A short note (not a lengthy policy memo) explaining that
  the required behavioral-health module is changing format — shorter
  sessions, spread out, same requirement — and why: it respects their
  rotation schedule better and actually works better for retention of a
  skill they'll use with real patients.
- **To clinical faculty and rotation coordinators:** A brief heads-up that
  the module will now show as five shorter items instead of one long one on
  the student's training dashboard, so it isn't flagged as incomplete work
  when a student has finished some but not all modules yet.
- **To the Curriculum & Accreditation office:** Confirmation that all
  required accreditation content is still fully covered — nothing was cut,
  only restructured — with the module map from `02_design.md` as
  documentation.

## Support Materials

- A one-page FAQ addressing the most likely question: "Do I have to do all
  five modules in one sitting?" (No — that's the point.)
- A short guide for rotation coordinators on reading the new five-part
  completion status in the LMS dashboard.

## Risk & Mitigation

| Risk | Mitigation |
|---|---|
| Students start Module 1 but never return for the rest | Automated reminder after 5 days of inactivity; the same behavior the LMS already uses for other required modules |
| Students perceive five separate items as "more work" than one module | Communication plan explicitly frames total time (~60 min) as far shorter than the original 6 hours |
| Pilot data doesn't show improvement | Pilot phase exists specifically to catch this before a full rollout; QA checklist and item-level assessment data (not just overall pass/fail) make it possible to find exactly which module needs revision |

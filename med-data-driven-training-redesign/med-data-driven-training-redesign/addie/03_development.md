# ADDIE Phase 3: Development

## What Was Built

- **Full storyboard** for all five modules — `storyboard/module_storyboards.md`
  — screen-by-screen, with visual description, on-screen text, narration
  script, interaction, and navigation notes. This is the document that
  would hand off directly to an Articulate Storyline 360 or Rise 360 build.
- **Assessment items** for every module — `assessment/assessment_design.md`
  — written and ready to load into the authoring tool's quiz feature.
- **An interactive prototype** — `prototype/module_1_prototype.html` — a
  working HTML/CSS/JS build of Module 1, styled to match the look and
  interaction pattern of a Rise 360 microlearning block (click-to-reveal
  cards, then a knowledge check with immediate feedback). This isn't a
  Storyline/Rise file itself (those are proprietary authoring formats), but
  it demonstrates the same interaction design a developer would build in
  either tool, and it's something a hiring manager can actually open and
  click through.

## Why a Prototype Instead of a Native Storyline/Rise File

Storyline `.story` and Rise 360 course files are proprietary and can only be
opened with an Articulate 360 license, which makes them a poor choice for a
portfolio artifact — nobody reviewing this repository could open one
without paying for the software. Building the same interaction as a plain
HTML/CSS/JS page keeps the design decisions (chunking, click-to-reveal,
immediate feedback, a visible progress indicator) fully visible and
functional to anyone, in any browser, while the storyboard document is
exactly what would be handed to a Storyline/Rise developer to build the
real thing.

## Development Standards Applied

- **Consistent visual identity** across the module: the same accent color
  and typography used throughout this project's other repositories, so a
  reviewer moving between them sees one coherent body of work rather than
  three disconnected exercises.
- **Mobile-first layout**, since students may complete microlearning on a
  phone between clinic sessions, not only at a desk.
- **Accessible interaction patterns**: visible focus states, sufficient
  color contrast, and feedback that doesn't rely on color alone (an icon
  and text label accompany every correct/incorrect state).
- **Clinically neutral example content**: all patient scenarios used in the
  storyboard, assessments, and prototype are fictional and written to
  illustrate interview technique, not to simulate detailed clinical
  diagnosis — appropriate for a portfolio artifact rather than a real
  curriculum's full clinical case library.

## Quality Assurance Checklist

Before any module would ship to students, it goes through:

- [ ] Content accuracy review against current curriculum and accreditation
      standards
- [ ] Accessibility check (keyboard navigation, screen reader labels, color
      contrast)
- [ ] Functional check on desktop and mobile browsers
- [ ] Assessment item review against the blueprint (does each item test the
      objective it's supposed to?)
- [ ] Subject-matter-expert sign-off (Psychiatry / Behavioral Science
      faculty)

# NeuroPulse HE — Nine-Screen UI Prototype (430 × 932)

NeuroPulse HE is a neuro-adaptive planning, focus and sensory-regulation app for
neurodivergent students in higher education (ADHD, autism, dyslexia). The
prototype is built as nine standalone HTML screens, one file per screen, so each
artboard can be opened, reviewed and marked in isolation. Nothing is bundled
into a single interactive app.

## Design specification

- **Hardware target**: iPhone-class artboard, 430 × 932 px, fixed height.
- **Design tokens**: `core.css` (colour, type, spacing, radii, elevation).
- **Typography**: Inter for UI; Atkinson Hyperlegible for long-form reading.
- **Iconography**: inline SVG only — no emoji, no icon font.
- **Palette**: warm off-white paper (`#F7F5EF`), ink (`#171E19`), sage accent
  (`#476A55`). A warm and a night variant are included.
- **Research basis**: every screen carries a right-hand spec rail naming the
  studies behind the decisions, the Norman principles applied, and interaction
  notes.
- **Motion**: no decorative animation; transitions are short and are switched
  off when "Reduce animation" is on.

## Screens

| # | File | Purpose |
|---|------|---------|
| 01 | `01-today.html` | Today: one next action, a realistic load, no overdue backlog. |
| 02 | `02-plan.html` | Plan: work broken into 15–25 minute steps across the week. |
| 03 | `03-step.html` | Step detail: what "done" looks like, materials, and a single start button. |
| 04 | `04-focus.html` | Focus: a timer that shows remaining time without pressure. |
| 05 | `05-rest.html` | Rest: a deliberate, guilt-free break between steps. |
| 06 | `06-calm.html` | Calm: a low-demand reset surface with paced breathing. |
| 07 | `07-reading.html` | Reading: size, spacing and typeface controls, with rationale. |
| 08 | `08-sensory.html` | Sensory: colour, motion and sound settings that apply live. |
| 09 | `09-support.html` | Support: progress without streaks, plus routes to human help. |

## Review surfaces

- `index.html` — prototype map: live thumbnails, journeys, design rationale and
  the Harvard reference list used across the screens.
- Append `#embed` to any screen URL (e.g. `01-today.html#embed`) to hide the
  spec rail and render the artboard alone, which is how the report figures were
  captured.

## Shared behaviour

`ui.js` holds the small interactions shared by the screens: live clock, theme
switching, segmented controls, switches, checklist state, timer, breathing
pacer and reading controls. State is deliberately in-memory only; persistence
is out of scope for the prototype.

## Running

Open `index.html` directly in a browser. There is no build step and no
dependency beyond the Google Fonts stylesheet. For figure capture the screens
were rendered in headless Chrome at `1200 × 1180`.

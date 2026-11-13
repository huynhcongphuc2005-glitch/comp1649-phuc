# COMP1649 Human–Computer Interaction and Design (2026–2027)

**University of Greenwich · School of Computing and Mathematical Sciences**

## NeuroPulse HE — Option A

A mobile companion for neurodivergent learners in higher education (ADHD, autism,
dyslexia). The design is built around one next action, an explicit rest state, and
interface settings that can be changed without diagnosis or disclosure.

## Deliverables

| File | What it is |
|------|-----------|
| [`report/COMP1649_Coursework_Report.docx`](report/COMP1649_Coursework_Report.docx) | Report in Word format, ready to upload to Google Docs or submit as PDF |
| [`report/COMP1649_Coursework_Report.pdf`](report/COMP1649_Coursework_Report.pdf) | Print-ready PDF of the same report |
| [`report/report.html`](report/report.html) | Editable source of the report, with figure paths |
| [`report/figures/`](report/figures/) | Figure images used in the report |
| [`prototype/`](prototype/) | Nine standalone screens, one HTML file per screen |

The report runs from the Introduction to the Conclusion at **3,229 words** (the
brief allows 2,000–3,000 words, with 10% over not penalised). Title page,
contents, references and appendices are excluded. All 18 references were checked
against Crossref; titles, authors, volumes, pages and DOIs match the publisher
record.

## Prototype

Open [`prototype/index.html`](prototype/index.html) for the prototype map: live
thumbnails, the three journeys, design rationale and the reference list. Each
screen also opens on its own:

1. [`01-today.html`](prototype/01-today.html) — one next action, no backlog
2. [`02-plan.html`](prototype/02-plan.html) — work split into 15–25 minute steps
3. [`03-step.html`](prototype/03-step.html) — definition of done and a single start
4. [`04-focus.html`](prototype/04-focus.html) — timer without time pressure
5. [`05-rest.html`](prototype/05-rest.html) — rest as a legitimate state
6. [`06-calm.html`](prototype/06-calm.html) — low-demand reset and paced breathing
7. [`07-reading.html`](prototype/07-reading.html) — size, spacing and typeface controls
8. [`08-sensory.html`](prototype/08-sensory.html) — colour, motion and sound
9. [`09-support.html`](prototype/09-support.html) — progress without streaks, plus human support

Every screen has a right-hand spec rail naming the research behind it, the Norman
principles applied, and interaction notes. Add `#embed` to a screen URL to hide
the rail and show the artboard alone.

### Format note

The brief specifies Axure RP or Figma Design. The submission supplies a coded
HTML/CSS build at the same 430 × 932 artboard size, one file per screen, so each
artboard can be reviewed on its own and the interaction logic can be inspected.
The screens use standard components and import into Figma Design; the browser
build is the reference artefact.

## Design decisions with evidence

- **One next action** rather than a dashboard (Sonne et al., 2016).
- **Rest as a screen**, not a modal or a reward (Van Hees, Moyson and Roeyers, 2015).
- **No streaks, scores or badges** (Spiel et al., 2022).
- **OpenDyslexic available but off by default**, because Wery and Diliberto (2017)
  found no reading-rate or accuracy benefit; size and spacing controls are
  prioritised instead (Rello and Baeza-Yates, 2013).
- **Adjustment without disclosure**, in the main navigation (Clouder et al., 2020;
  Morris, Begel and Wiedermann, 2015).
- **Routes to people**, because software is not a substitute for support
  (McDowall and Kiseleva, 2024).

## Running the prototype

No build step. Open `prototype/index.html` in a browser; the only external
dependency is the Google Fonts stylesheet. The report was generated from
`report/report.html` with python-docx, and the figures were captured from the
prototype in headless Chrome at the 430 × 932 artboard size.

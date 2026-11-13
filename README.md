# COMP1649 Human–Computer Interaction and Design (2026–2027)

**University of Greenwich · School of Computing and Mathematical Sciences**

## NeuroPulse HE — Option A

A mobile companion for neurodivergent learners in higher education (ADHD, autism,
dyslexia), built around one next action, rest as a legitimate state, a calm reset
reachable from every screen, and settings that need no disclosure.

## Deliverables

| Path | What it is |
|------|-----------|
| `report/COMP1649_Coursework_Report.docx` | The report: about 3,000 words from Introduction to Conclusion (including captions and tables), 12 Harvard references with active DOI links, appendices A–F |
| `report/figures/sketches/` | Hand-drawn style sketches: first versions, final sketch of each screen, storyboard, card-based prototype. Redraw them on paper, photograph, and save over the PNG with the same name |
| `report/figures/` | One image per screen (`screen-*.png`) and one annotated screen per Norman principle (`norman-*.png`) |
| `figma/NN-*.html` | 8 main screens + 4 state variants (one 430 × 932 frame per file, no device frame) for html.to.design |
| `figma/png/` | 2× screenshots of every screen (860 × 1864) |
| `figma/FIGMA_GUIDE.md` | Import steps and the interaction wiring table for Figma Design |

The brief requires a Figma Design (.fig) prototype: import the screens with
html.to.design and connect the interactions as described in `figma/FIGMA_GUIDE.md`.

## Screens

| Frame | Journey | Purpose |
|---|---|---|
| 01 Today | J1 | One next action |
| 02 Plan | J1, J3 | Work split into steps of 15 minutes or less |
| 03 Step | J1 | Definition of done and a single start |
| 04 Focus / 04b Paused | J1 | Remaining time visible; Pause is the primary control |
| 05 Rest | J1 | Rest as the next task; stopping is never "missed" |
| 06 Calm / 06b Quiet mode | J2 | Low-demand reset, dim colours, silence, hide numbers |
| 07 Settings / 07b Applied | J3 | Text size, spacing, typeface, colour, motion, applied live |
| 08 Progress | J3 | Steps, time and rest days without streaks; routes to people |
| 00 Today (control) | Study | Dashboard condition for the A/B study in Section 5 |

## References

All 12 references were checked against Crossref and the publisher record (authors,
title, venue, volume, issue, pages, DOI), and the 8 annotated sources against their
abstracts. Format: Cite Them Right Harvard.

## Rebuilding

```bash
python3 scripts/build_screens.py      # figma/*.html
bash scripts/capture.sh               # figma/png/*.png (headless Chrome)
python3 scripts/build_figures.py      # report/figures/*.png   (needs Pillow)
bash scripts/build_sketches.sh        # report/figures/sketches/*.png (rough.js, Kalam/Caveat fonts)
python3 scripts/build_report.py       # report .docx           (needs python-docx, pypdf, LibreOffice for page numbers)
```

Set the student name, ID and tutor in `STUDENT` at the top of `scripts/build_report.py`.

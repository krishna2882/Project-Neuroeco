# Presentation

Deck: 30 slides, blue/white: 21 talk slides, a Questions slide, an appendix index with 6 backup answers (A–F), and references. The rendered version (with PowerPoint/PDF export) is shared privately between the authors.

`deck/` is the source of that deck: `deck.json` (slide order, sections, fonts), `deck.css` (shared look) and one HTML
file per slide in `slides/`, with speaker notes in each slide's `<aside>`. Charts are generated from the results by
`python -m analysis.slide_figs` (→ `results/slides/`); every number on the slides comes from the files under `results/`.

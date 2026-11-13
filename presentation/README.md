# Presentation

Live deck (20 slides, blue/white): https://claude.ai/artifact/1j1RRPkYjsrr3iPz5mAoQG (private until shared from its Share
menu, which also exports PowerPoint/PDF).

`deck/` is the source of that deck: `deck.json` (slide order, sections, fonts), `deck.css` (shared look) and one HTML
file per slide in `slides/`, with speaker notes in each slide's `<aside>`. Charts are generated from the results by
`python -m analysis.slide_figs` (→ `results/slides/`); every number on the slides comes from the files under `results/`.

# Local bilingual literature library

Open `index.html` in a browser. The website runs without a server or network dependencies. Language selection supports English, Persian, and both together. Search titles/DOIs and filter by category.

## First delivery — 2026-11-13

- 23 unique source records, deduplicated using opening-page DOI or normalized filename; duplicates remain listed in `inventory.json`.
- LA-UPAHEM: bilingual report, original crops of all 9 figures, printed plot values, original source views for all 14 tables, 20 source pages, 49 extracted references.
- Other articles have explicitly marked pending-analysis pages. Their figures and methods have not yet been analyzed.
- Critical observations are labeled separately from author statements. Original bibliography entries are retained in their published language. Original figure labels and table values remain in English.
- Research source PDFs are unchanged. The generated library and figure reproductions are intended for local research use.

## Evidence limits

The first report summarizes the paper; it does not reproduce the experiments. Only printed numerical values are transcribed; curve samples and unlabeled error bars are not estimated. Full table values and appendix prompts/code are available through their original page images; they have not all been converted to structured data or translated line by line. Bibliography extraction may retain typographical errors; original pp.19–20 are supplied for comparison.

Static checks verified local links, assets, anchors, figure/reference counts, and shared JavaScript syntax. Original figures were visually inspected. Interactive browser layout and behavior have not been verified because the browser tool previously blocked local-file previews.

## Rebuilding

`scripts/build_literature_site.py` builds HTML, inventory, and shared CSS/JS using bundled Python and pypdf. It requires the existing LA-UPAHEM rendered pages and figure crops in `assets/la-upahem/` and the extracted text in `reports/literature/la-upahem-full.txt`. Those source-derived assets are retained in this delivery.

## Second delivery — 2026-11-13

Huang / EECL (`article-02.html`) is now available: bilingual source-based analysis, 16 original figure crops including appendix C14–C16, 11 table source views, all 18 original pages, and 53 references. The report distinguishes data-driven structure learning from expert-derived probability parameters and reports accuracy alongside sensor-count efficiency.

The researcher selected **Technical Dashboard**. The landing and report pages now use the shared navy dashboard theme (`design.css` plus `theme.css`). `design-samples.html` retains the three live alternatives for later comparison. One language is visible by default; both-language mode remains available.

Shared reading tools now include image enlargement, reading progress, a contents indicator, and source-view expansion controls. Local browser inspection confirmed the sample landing and Huang report rendered; static asset/link checks and JavaScript syntax checks passed.

Continue one full article at a time before consolidating P0 specifications. P0 remains open.

## Full local corpus review — 2026-11-13

All 23 unique articles found in the supplied folder now have bilingual analysis pages. Each includes a **Role in our research** section answering importance, contribution, proposed use, and baseline suitability. `research-map.html` brings those assessments together. Baseline recommendations are project assessments, not author claims or approved implementation decisions.

The library retains 542 original PDF page images. Visual indexes include numbered figures, appendix figures, graphical abstracts, and continued figure views; these are evidence-view counts, not counts of independent experiments. Uncertain figure boundaries use explicitly labeled complete source-page images. Original table rows remain available through their source views; unlabeled curves are not numerically estimated. External supplements absent from the supplied PDFs are not claimed reviewed.

The canonical reviewed data for additional reports are `reports/literature/analyses/article-*.json`; the original two reports use their existing builders plus `existing-roles.json`. The JSON records include manual source-page, caption, and prose corrections. Authoring scripts are historical helpers and must not overwrite those corrections without review. Rebuild using `scripts/build_literature_site.py`, then run `scripts/validate_literature_site.py`. Source renders can be prepared with `scripts/prepare_literature_assets.py`.

Numbered bibliographies are linked when a sequential reference list can be identified. Author-year bibliographies are preserved as full transcripts with original reference-page links. Neither format implies that every paper cited by an analyzed article was independently reviewed.

This completes the local literature-library deliverable. P0 research-specification decisions, final baseline selection, and experimental protocols remain open.

## Figure presentation update — 2026-11-13

All 23 homepage cards now include a visual from their source article. The 244 visual evidence records use 162 focused original-figure views and 82 explicitly labeled complete-page views where cropping could lose context. No curve values are estimated.

Each figure has a reading guide, its reviewed explanation, evidence limits when available, its original caption, and a source-page link. Reading guidance is labeled separately from author claims. A figure navigator, images-only mode, and enlarged viewer with zoom and previous/next controls support inspection. English/Persian toggling remains supported.

`scripts/prepare_figure_views.py` prepares the source crops, card previews, and `figure-views.json` manifest from existing page renders. Run it when source assets change; normal rebuilds reuse the manifest. `scripts/build_literature_site.py` applies the presentation through `scripts/enhance_figure_presentation.py`. Validation now checks every card image and every figure presentation, including a regression check against reference markup entering image alt text. Browser checks verified card search, report navigation, figure selection, enlargement, zoom, next/previous navigation, and images-only mode.

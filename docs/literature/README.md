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

`agent/scripts/build_literature_site.py` builds HTML, inventory, and shared CSS/JS using bundled Python and pypdf. It requires the existing LA-UPAHEM rendered pages and figure crops in `assets/la-upahem/` and the extracted text in `reports/literature/la-upahem-full.txt`. Those source-derived assets are retained in this delivery.

## Second delivery — 2026-11-13

Huang / EECL (`article-02.html`) is now available: bilingual source-based analysis, 16 original figure crops including appendix C14–C16, 11 table source views, all 18 original pages, and 53 references. The report distinguishes data-driven structure learning from expert-derived probability parameters and reports accuracy alongside sensor-count efficiency.

The researcher selected **Technical Dashboard**. The landing and report pages now use the shared navy dashboard theme (`design.css` plus `theme.css`). `design-samples.html` retains the three live alternatives for later comparison. One language is visible by default; both-language mode remains available.

Shared reading tools now include image enlargement, reading progress, a contents indicator, and source-view expansion controls. Local browser inspection confirmed the sample landing and Huang report rendered; static asset/link checks and JavaScript syntax checks passed.

Continue one full article at a time before consolidating P0 specifications. P0 remains open.

## Full local corpus review — 2026-11-13

All 23 unique articles found in the supplied folder now have bilingual analysis pages. Each includes a **Role in our research** section answering importance, contribution, proposed use, and baseline suitability. `research-map.html` brings those assessments together. Baseline recommendations are project assessments, not author claims or approved implementation decisions.

The library retains 542 original PDF page images. Visual indexes include numbered figures, appendix figures, graphical abstracts, and continued figure views; these are evidence-view counts, not counts of independent experiments. Uncertain figure boundaries use explicitly labeled complete source-page images. Original table rows remain available through their source views; unlabeled curves are not numerically estimated. External supplements absent from the supplied PDFs are not claimed reviewed.

The canonical reviewed data for additional reports are `reports/literature/analyses/article-*.json`; the original two reports use their existing builders plus `existing-roles.json`. The JSON records include manual source-page, caption, and prose corrections. Authoring scripts are historical helpers and must not overwrite those corrections without review. Rebuild using `agent/scripts/build_literature_site.py`, then run `agent/scripts/validate_literature_site.py`. Source renders can be prepared with `agent/scripts/prepare_literature_assets.py`.

Numbered bibliographies are linked when a sequential reference list can be identified. Author-year bibliographies are preserved as full transcripts with original reference-page links. Neither format implies that every paper cited by an analyzed article was independently reviewed.

This completes the local literature-library deliverable. P0 research-specification decisions, final baseline selection, and experimental protocols remain open.

## Figure presentation update — 2026-11-13

All 23 homepage cards now include a visual from their source article. The 244 visual evidence records use 162 focused original-figure views and 82 explicitly labeled complete-page views where cropping could lose context. No curve values are estimated.

Each figure has a reading guide, its reviewed explanation, evidence limits when available, its original caption, and a source-page link. Reading guidance is labeled separately from author claims. A figure navigator, images-only mode, and enlarged viewer with zoom and previous/next controls support inspection. English/Persian toggling remains supported.

## Jev additions — 2026-11-15

Six supplied Jev manuscripts are analyzed as `article-24` through `article-29`, in the new **Decision models & agent efficiency** category: energy-audit recommendations; JevAgentHarness; REFLEX; the broad System One benchmark; Fast Models, Slow Evidence; and the empirical agent-workflow study. The library now has 29 reports and 293 visual evidence views, with 676 original PDF page images. This addition contributes 49 focused figure views and 106 original table views across 134 pages.

Each new report covers questions/hypotheses, methods and implementation contracts, experiments and controls, reported results, author-stated limits/future work, separate reviewer assessments, and all four project-role questions. Original figure captions remain in linked source pages; displayed bilingual captions are explicitly labeled summaries. Bibliographies end at the actual reference boundary, excluding following appendices. Prices, API details, publication identifiers and release promises are statements in the supplied manuscripts; external services, repositories, model weights and publication records were not independently authenticated or executed.

Reported non-inferiority failures, retired hypotheses/claims, calibration failures, shared denominators, interface confounds and complete cost accounting are retained rather than replaced by abstract-level savings. Jev integration remains a conditional research recommendation, not an approved architectural or baseline change. P0 remains open.

The inventory builder now preserves report IDs when sources are added. `prepare_figure_views.py article-24 article-25 ...` can prepare selected articles while retaining the existing manifest. Reviewed records are canonical; `author_jev_reports.py` is an intentional regeneration helper and must not overwrite later manual corrections without review. Browser checks cover all six report routes, figure navigation, Persian rendering and image enlargement; static checks cover all 29 reports and source links.

`agent/scripts/prepare_figure_views.py` prepares the source crops, card previews, and `figure-views.json` manifest from existing page renders. Run it when source assets change; normal rebuilds reuse the manifest. `agent/scripts/build_literature_site.py` applies the presentation through `agent/scripts/enhance_figure_presentation.py`. Validation now checks every card image and every figure presentation, including a regression check against reference markup entering image alt text. Browser checks verified card search, report navigation, figure selection, enlargement, zoom, next/previous navigation, and images-only mode.

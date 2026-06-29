# Template resync status — `ab458cb` → `5c0e94c`

Single source of truth for where this dossier stands against the template lineage.
**Read this before any template sync** — it records which upstream migrations were
adopted, which were deliberately deferred, and why. It survives the resync ritual's
wholesale rewrite of `template-sync.json` (which stays a clean 3-field machine pin).

## Landed
- ✅ **Bucket 1 — machinery** (CI-green subset) · `160d681`
- ✅ **Migrations #1 + #2 — single-source front door** (`index.html` generated from
  `editions/index.source.html` over `skin/edition.html`; `paper.html` → redirect stub;
  three edition/markdown/projection gates live) · `2fabcfa`
- ✅ **README reconcile (Decision 1)** — `README.md` "argument in one move" now bridges
  to Chapter 2's scoping result, matching the front door · `12dbf7f`
- ✅ **Nav arc** — all 3 standalone pages (dossier/verify/lineage) to the 4-button front-door nav;
  site-wide HTML-escape sweep · `debcc85`, `90afa4c`
- ✅ **Migration #6 (adapted)** — lineage oldest-first, working draft at the foot, "The landscape"
  dropped, `llms.txt` doubled-title fixed · `01a9dad`, `96e9899`. **`sealed()` kept ours**
  (single record door to `chapters/<tag>/index.html`); the template's two-door version routes its
  primary "Read (current edition)" link through `live/<tag>/`, which depends on the deferred #5 —
  so #6 is adopted EXCEPT that door, by the same design as #5.
- ✅ **Migrations #3 + #4 — absorbed into #1 (no-ops).** Both introduced the source/skin
  single-source partition upstream, which we adopted wholesale in migration #1. #3 (avenues
  single-source): `bake_machinery.js` is byte-identical to template and bakes our 4 avenue
  cards + console verdict from `avenues.json`; gated by `verify_projection`. #4 (cite data
  split): cite DATA lives in the source's `<!--slot:cites-->` JSON (11 entries), cite MACHINERY
  (popcards, term/cite handlers) in the skin — the clean split #4 specifies. No separate work.
  (The "seal `avenues.json` into `chapters/<tag>/`" half of #3's upstream commits belongs to the
  freeze/back-catalog process = deferred #5, not the live front-door single-sourcing.)

## ⛔ Deferred — permanent unless a chapter is re-sealed new-model
- **Migration #5 — back-catalog lifecycle (`live/<tag>/`)**
  - **Reason:** `render_backcatalog.js` re-skins each chapter from its OWN sealed source,
    requiring `chapters/<tag>/editions/index.source.html` + `chapters/<tag>/avenues.json`.
    Our `v1.0`/`v2.0` were frozen BEFORE the single-source freeze existed (`f0af2b0`), so
    they lack both. Providing them means writing into the DOI'd / OpenTimestamped, write-once
    `chapters/<tag>/` dirs (doctrine forbids; it would re-diverge from the `v1.0`/`v2.0` tags
    we restored in `3a74e20`) AND reconstructing source that never existed.
  - **Forward instruction to future syncs:** do **NOT** add `.github/workflows/reskin-backcatalog.yml`
    or the `verify_backcatalog` CI gate. A sync that touches `skin/` or `render_*` would
    normally pull these in — skip them. They cannot run against our legacy back-catalog.
  - **Why it costs nothing:** the version of record (`chapters/<tag>/`) is always served and is
    what the DOI cites. Old chapters keep their as-published skin — which the doctrine treats as
    a feature (the design visibly matures across chapters; the record isn't retro-themed).
  - **Revisit only if** a future chapter is frozen under the new model — then `live/` applies to
    THAT chapter natively, with no seal modification.
  - **Note on the living-figure work:** it does NOT return via `live/<tag>/` (that re-skins sealed
    content verbatim and cannot inject new figures). It belongs in a future chapter authored with
    living figures in its source, or in the working draft — not a re-skin of v1.0/v2.0.

## Pending (light migrations — none touch the sealed back-catalog)
- ⏭️ **#8** — EST→FORECAST ledger relabel
- ⏭️ **`AUTHORING.md`** — hand-merge (236-line three-way; its own focused pass)

## Known follow-ups (non-blocking)
- **Standalone editions drift on skin changes.** `dossier.html`, `verify.html`, and `lineage.html` are NOT
  skin-rendered (no render script touches them), so their chrome (nav, footer) does not update
  when `skin/edition.html` changes. This caused a nav-version drift after migrations #1+#2 (the
  front door moved to the 4-button nav; these two stayed on the old 5-button nav until manually
  fixed in `debcc85`). The durable fix is bringing them into the single-source/skin model so
  their nav is generated, not hand-maintained — candidate for a future migration. Until then,
  any skin nav/footer change must be hand-mirrored into these two files.
- **Literal-escape mangle hazard in standalone files.** `dossier.html`'s footer carried a literal
  6-char `\u2190` string (rendered as visible text, not a `←` arrow) — a pre-existing escape
  mangle, fixed in `debcc85`; a further cluster of five literal `\u2192` escapes in
  dossier.html's HTML content was found and fixed later (always byte-scan the WHOLE file). Other standalone/hand-authored files may carry similar literal
  `\uXXXX` escapes or PUA characters; worth a byte-scan when next editing them. When editing
  literal-vs-rendered characters, express both via escapes in code, never paste the glyph.
- **Multi-line edits: literal full-block anchors only, never regex bounding.** Two edits this resync
  nearly corrupted files via regex (the verify.html footer greedy-match; an Edit-5 `(?=...var...)`
  lookahead that would have eaten the `(function(){` IIFE opener in lineage.html — caught pre-write
  by an IIFE-survival + `node --check` guard). Every literal full-string anchor with a `count==1`
  assert has landed clean; every regex-bounded multi-line replace has misfired or nearly did. Use
  literal anchors + count asserts + a parse check for any code edit.

## Sealed-chapter nav audit (recorded so it isn't re-litigated)
- **Live-tracking nav is AS-DESIGNED — do NOT "fix" it.** `freeze_chapter.py`'s `rewire()` deliberately
  repoints a sealed chapter's cross-edition/lineage nav to the live root (`../../index.html`,
  `../../dossier.html`, etc.) so an old chapter is not a navigational dead-end — its buttons return
  the reader to the CURRENT live series, not to its frozen siblings. So from `chapters/v1.0/`, the
  "easy-read/self-explaining" button correctly goes to the live front door (via the `paper.html`
  redirect stub). The button LABELS are historical ("The landscape", "Self-explaining edition" =
  what the live editions were called at seal time) — that is the "as-published, don't retro-theme"
  doctrine working, not a bug. Relabeling them would fight the live-tracking design AND retro-theme
  the record. Leave them.
- **Known unfixed: `chapters/<tag>/paper.html` PDF button 404s.** `rewire()` covers `.html` nav +
  `<img>`/`<script>` srcs but missed `<a href>` PDF paths, so `paper.html`'s `paper/manuscript.pdf`
  stayed bare (404) while `index.html`'s got `../../` (resolves). Deliberately UNFIXED: editing the
  frozen `chapters/<tag>/` dirs diverges the served copy from the Zenodo deposit, and the PDF button
  is deprecated chrome retired from live editions (commit 1B), slated for Phase-3 removal — not worth
  it for a dead button. Root-cause fix (if ever): extend the template's `rewire()` to cover `<a href>`
  PDFs so FUTURE freezes don't repeat it — upstream machinery, no seal touch.

## Final step
- ⏭️ Stamp `template-sync.json` → `5c0e94c` **after** the pending items land.
  This stamp means "synced through `5c0e94c` **except migration #5, by permanent design**."
  A drift audit comparing the pin to the template will see `reskin-backcatalog.yml` absent —
  that absence is deliberate and explained above, not unfinished work.

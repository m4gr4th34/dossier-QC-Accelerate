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
- ⏭️ **#3** — avenues single-source (survey-shaped; applies)
- ⏭️ **#4** — cite data split (skin vs content)
- ⏭️ **#6** — lineage oldest-first / two-doors (carries the `llms.txt` doubled-title fix)
- ⏭️ **#8** — EST→FORECAST ledger relabel
- ⏭️ **`AUTHORING.md`** — hand-merge (236-line three-way; its own focused pass)

## Known follow-ups (non-blocking)
- **Standalone editions drift on skin changes.** `dossier.html` and `verify.html` are NOT
  skin-rendered (no render script touches them), so their chrome (nav, footer) does not update
  when `skin/edition.html` changes. This caused a nav-version drift after migrations #1+#2 (the
  front door moved to the 4-button nav; these two stayed on the old 5-button nav until manually
  fixed in `debcc85`). The durable fix is bringing them into the single-source/skin model so
  their nav is generated, not hand-maintained — candidate for a future migration. Until then,
  any skin nav/footer change must be hand-mirrored into these two files.
- **Literal-escape mangle hazard in standalone files.** `dossier.html`'s footer carried a literal
  6-char `\u2190` string (rendered as visible text, not a `←` arrow) — a pre-existing escape
  mangle, fixed in `debcc85`. Other standalone/hand-authored files may carry similar literal
  `\uXXXX` escapes or PUA characters; worth a byte-scan when next editing them. When editing
  literal-vs-rendered characters, express both via escapes in code, never paste the glyph.

## Final step
- ⏭️ Stamp `template-sync.json` → `5c0e94c` **after** the pending items land.
  This stamp means "synced through `5c0e94c` **except migration #5, by permanent design**."
  A drift audit comparing the pin to the template will see `reskin-backcatalog.yml` absent —
  that absence is deliberate and explained above, not unfinished work.

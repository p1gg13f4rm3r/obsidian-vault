# Study Notes - GitHub Repos

## Index

| Category | Count |
|---------|-------|
| [Stock Trading](#stock-trading) | 1 |
| [AI / Autonomous Agents](#ai--autonomous-agents) | 6 |
| [Research / experiments](#research--experiments) | 1 |
| [Learning / Education](#learning--education) | 2 |
| [Productivity](#productivity) | 1 |
| [File Format / Reverse Engineering](#file-format--reverse-engineering) | 2 |

---

## Stock Trading

### [github.com/ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)
**Summary:** LLM-driven A/H/US stock analyzer with multi-source quotes + real-time news + LLM decision dashboard + multi-channel push. Free, runs on schedule.
- Added: 2026-03-15
- Status: To be studied
- Notes: 

---

## AI / Autonomous Agents

### [github.com/TraderAlice/OpenAlice](https://github.com/TraderAlice/OpenAlice)
**Summary:** File-driven AI trading agent engine for crypto and securities markets.
- Added: 2026-03-15
- Status: To be studied
- Notes: 

### [github.com/andrewyng/context-hub](https://github.com/andrewyng/context-hub)
**Summary:** Gives coding agents curated, versioned docs + ability to get smarter with every task. All content is open and maintained as markdown. CLI tool: `chub search` / `chub get`.
- Added: 2026-03-15
- Status: To be studied
- Notes: 

### [github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)
**Summary:** AI agents running research on single-GPU nanochat training automatically.
- Added: 2025-03-13 (consolidated 2026-03-15)
- Status: To be studied
- Notes: Autonomous AI research agent by Andrej Karpathy — researches and writes code autonomously

### [github.com/obra/superpowers](https://github.com/obra/superpowers)
**Summary:** Agentic skills framework & software development methodology. A complete workflow for coding agents with composable "skills" (brainstorming, TDD, writing-plans, subagent-driven-development, code review, etc.). Works with Claude Code, Cursor, Codex, OpenCode, Gemini CLI.
- Added: 2026-03-16
- Status: To be studied
- Notes: 

### [github.com/mattpocock/skills](https://github.com/mattpocock/skills)
**Summary:** A collection of agent skills that extend capabilities across planning, development, and tooling. Personal directory of skills from Matt Pocock (creator of Total TypeScript).
- Added: 2026-03-17
- Status: To be studied
- Notes: 
  - **Planning & Design:** write-a-prd, prd-to-issues, grill-me
  - **Development:** tdd, triage-issue, improve-codebase-architecture
  - **Tooling:** setup-pre-commit, git-guardrails-claude-code
  - **Writing:** write-a-skill

### [github.com/Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything)
**Summary:** Claude Code skills that turn any codebase into an interactive knowledge graph you can explore, search, and ask questions about. Supports multi-platform agents (Claude Code, Codex, etc.). 2.2k+ stars.
- Added: 2026-03-21
- Status: To be studied
- Notes: 
  - **Topics:** claude-code, claude-skills, codex-skills, knowledge-graph, understandcode
  - **License:** MIT
  - **Homepage:** https://lum.is-a.dev/Understand-Anything/

---

## Research / experiments

### [github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
**Summary:** A Simple and Universal Swarm Intelligence Engine, Predicting Anything. Universal swarm intelligence engine for predictions.
- Added: 2026-03-14
- Status: To be studied
- Notes: 

---

## Learning / Education

### [Game Theory - Giacomo Bonanno](https://arxiv.org/pdf/1512.06808)
**Summary:** Comprehensive Game Theory textbook with 165 solved exercises. Covers ordinal/cardinal games, Nash equilibrium, subgame-perfect equilibrium, knowledge & common knowledge, and refinements.
- Added: 2026-03-17
- Status: To be studied
- Notes: 
  - Part I: Games with ordinal payoffs
  - Part II: Games with cardinal payoffs
  - Part III: Knowledge, common knowledge, belief
  - Part IV: Refinements of subgame-perfect equilibrium

### [github.com/codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)
**Summary:** Master programming by recreating your favorite technologies from scratch. 475k+ stars — massive collection of build-your-own-X tutorials.
- Added: 2026-03-15
- Status: To be studied
- Notes: 

---

## Productivity

### [github.com/gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)
**Summary:** Productivity/task management tool (need more details)
- Added: 2026-03-17
- Status: To be studied
- Notes:

## Previously Studied

## File Format / Reverse Engineering

### [github.com/obriensp/iWorkFileFormat](https://github.com/obriensp/iWorkFileFormat)
**Summary:** Authoritative reverse-engineered spec for Apple iWork 2013+ formats (Pages, Numbers, Keynote). Contains full protobuf message definitions, type ID mappings, and IWA archive format documentation.
- Added: 2026-03-20
- Status: To be studied
- **Full research report:** [`iWork-TrackChanges-Research-Report.md`](iWork-TrackChanges-Research-Report.md)
- Notes:
  - **Format:** ZIP bundle → `Index.zip` → Snappy-compressed Protobuf `.iwa` files
  - **Key files:** `Document.iwa` (main content), `AnnotationAuthorStorage.iwa` (authors)
  - **Track Changes Detection — Protobuf Type IDs (from Common.json / Pages.json):**
    | Type ID | Message | Purpose |
    |---------|---------|---------|
    | 10148 | `TP.ChangeCTVisibilityCommandArchive` | Toggle track changes visibility |
    | 10149 | `TP.TrackChangesCommandArchive` | Enable/disable track changes |
    | 10157 | `TP.PauseChangeTrackingCommandArchive` | Pause/resume tracking |
    | 2013 | `TSWP.HighlightArchive` | Highlighted text (linked to comments) |
    | 2014 | `TSWP.CommentInfoArchive` | Comment bubble metadata |
    | 3056 | `TSD.CommentStorageArchive` | Comment text + author + date |
    | 212 | `TSK.AnnotationAuthorArchive` | Author name + color for markup |
    | 213 | `TSK.AnnotationAuthorStorageArchive` | List of all authors who made changes |
  - **Detection (Pages):** `TP.DocumentArchive.change_tracking_enabled = true` in `Document.iwa`
  - **Redline Records:** `TSWP.ChangeArchive` objects embedded in `TSWP.TextStorageArchive`:
    - `kind=1` = insertion (red underline in UI)
    - `kind=2` = deletion (strikethrough in UI)
    - `session` → `TSWP.ChangeSessionArchive` (author + date)
    - `hidden=true` → hidden changes still tracked
  - **Markup Settings:** `TP.SettingsArchive` fields:
    - `show_ct_markup` (default: true) — show insertions
    - `show_ct_deletions` (default: true) — show deletions
    - `change_bars_visible` (default: true) — change bars in margin
    - `format_changes_visible` (default: true) — show format changes
    - `annotations_visible` (default: true) — show comments
  - **Text Layer Tables:** `TSWP.TextStorageArchive` has:
    - `table_insertion` (field 21) — StringAttributeTable for inserted text
    - `table_deletion` (field 22) — StringAttributeTable for deleted text
    - `table_highlight` (field 23) — StringAttributeTable for highlights
  - **Comments (separate from TC):** `HighlightArchive` → `commentStorage` → `CommentStorageArchive`
  - **Numbers also:** `TST.TableInfoArchive.commentStorageTable` (field 19)

### [github.com/orcastor/iwork-converter](https://github.com/orcastor/iwork-converter)
**Summary:** Go-based iWork to HTML/JSON/Text converter. Includes complete proto definitions + type JSON mappings for Keynote (KN) and Numbers (TN) in `proto/` directory.
- Added: 2026-03-20
- Status: To be studied
- Notes:
  - `proto/KNArchives.proto` — Keynote protobuf definitions
  - `proto/TNArchives.proto` — Numbers protobuf definitions
  - Also extracts TSPRegistry type mappings (int → type) as `.json` files
  - Uses `snappy` framing format (no CRC-32C, no stream identifier chunk)
  - References: https://stingrayreader.sourceforge.net/ (Python IWA parser)

(None yet)

# Study Notes - GitHub Repos

## Index

| Category | Count |
|---------|-------|
| [Stock Trading](#stock-trading) | 2 |
| [AI / Autonomous Agents](#ai--autonomous-agents) | 6 |
| [Research / experiments](#research--experiments) | 1 |
| [Learning / Education](#learning--education) | 3 |
| [Productivity](#productivity) | 2 |
| [File Format / Reverse Engineering](#file-format--reverse-engineering) | 2 |

---

## Stock Trading

### [github.com/shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos)
**Summary:** Open-source foundation model for financial candlestick (K-line) data. Trained on OHLCV data from 45+ global exchanges. First open-source model to treat financial candlesticks as a "language" — tokenizer quantizes multi-dimensional K-line data into hierarchical discrete tokens, then autoregressive Transformer handles forecasting and diverse quantitative tasks. Accepted by AAAI 2026.
- Added: 2026-04-10
- Status: To be studied
- Notes:
  - Model sizes: Kronos-mini (4.1M), Kronos-small (24.7M), Kronos-base (102.3M), Kronos-large (499.2M, closed)
  - arXiv: [2508.02739](https://arxiv.org/abs/2508.02739)
  - Live demo: https://shiyu-coder.github.io/Kronos-demo/
  - HuggingFace: [NeoQuasar/Kronos-small](https://huggingface.co/NeoQuasar/Kronos-small)

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
**Summary:** A collection of agent skills that extend capabilities across planning, development, and tooling. Personal directory of skills from Matt Pocock (creator of Total TypeScript). 20k+ stars.
- Added: 2026-03-17
- Updated: 2026-04-25
- Status: To be studied
- Notes:
  - **Planning & Design:** to-prd, to-issues, grill-me, design-an-interface, request-refactor-plan
  - **Development:** tdd, triage-issue, improve-codebase-architecture, migrate-to-shoehorn, scaffold-exercises
  - **Tooling & Setup:** setup-pre-commit, git-guardrails-claude-code
  - **Writing & Knowledge:** write-a-skill, edit-article, ubiquitous-language, obsidian-vault
  - **Install:** `npx skills@latest add mattpocock/skills/<skill-name>`

### [github.com/Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything)
**Summary:** Claude Code skills that turn any codebase into an interactive knowledge graph you can explore, search, and ask questions about. Supports multi-platform agents (Claude Code, Codex, etc.). 2.2k+ stars.
- Added: 2026-03-21
- Status: To be studied
- Notes:
  - **Topics:** claude-code, claude-skills, codex-skills, knowledge-graph, understandcode
  - **License:** MIT
  - **Homepage:** https://lum.is-a.dev/Understand-Anything/

### [Agent Skills](https://agentskills.io/home)
**Summary:** Open standard for packaging and distributing capabilities to AI agents. A skill is a folder containing a `SKILL.md` file — metadata + instructions that tell an agent how to perform a specific task. Agents load skills via **progressive disclosure**: discovery (name + description only at startup) → activation (full instructions loaded on demand) → execution (follows instructions, optionally running bundled scripts). Skills can also bundle scripts, references, templates, and assets.
- Added: 2026-04-27
- Status: To be studied
- **Docs:** https://agentskills.io/home
- **GitHub org:** https://github.com/agentskills
- Notes:
  - **Core structure:**
    ```
    my-skill/
    ├── SKILL.md          # Required: name + description + instructions
    ├── scripts/          # Optional: executable code
    ├── references/       # Optional: documentation
    ├── assets/           # Optional: templates, images, data files
    └── ...
    ```
  - **Progressive disclosure (3 stages):**
    1. **Discovery** — agent loads name + description at startup
    2. **Activation** — on task match, full SKILL.md loaded into context
    3. **Execution** — follows instructions, optionally running bundled scripts
  - **SKILL.md fields:** `name` (1-64 chars, kebab-case), `description` (1-1024 chars, includes keywords), `license`, `environment`, `tags`, `tools` (space-separated approved tools), `instructions`
  - **Key principles for instructions:** step-by-step, self-contained, helpful error messages, handle edge cases gracefully
  - **Use cases:** domain expertise capture, repeatable workflows, cross-product skill reuse
  - **For skill creators:** Quickstart, Best practices, Optimizing descriptions, Evaluating skills, Using scripts
  - **For client implementors:** Adding skills support to any agent platform

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

### The First Principles Stack
**Summary:** A 5-step framework for achieving true understanding — stripping every assumption until you rebuild from provable ground truths.
- Added: 2026-03-23
- Status: Reference
- Notes:
  | Step | Question | What It Does |
  |------|----------|--------------|
  | 1 | "What is provably true?" | Break topic down using first principles. Strip every assumption. Rebuild from only what's provably true. |
  | 2 | "Can a 12-year-old understand it?" | Explain it simply. If it's not simple yet, keep going. |
  | 3 | "Which assumptions are actually proven?" | Identify the 5 assumptions beginners accept without question. |
  | 4 | "What if the top 3 are wrong?" | Stress-test the field's foundations. What collapses? |
  | 5 | "What would you build from zero?" | Start from the fundamentals. No industry conventions. No inherited thinking. |
  - **Core insight:** Each step strips another layer. By step 5 you're not thinking about the topic the way everyone else thinks about it — you're thinking from the ground up.
  - **Quote:** *"That's the difference between knowledge and understanding."*

---

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

### [github.com/jzOcb/writing-style-skill](https://github.com/jzOcb/writing-style-skill)
**Summary:** Reusable writing style skill template for AI coding agents. Built-in **auto-learning** — extracts rules from your edits (diff `original` vs `final`), so SKILL.md gets smarter the more you use it. Works with Claude Code + OpenClaw/ClawHub.
- Added: 2026-03-24
- Status: To be studied
- Notes:
  - **Core loop:** AI drafts → you revise → diff extracts rules → rules update SKILL.md
  - **Key files:** `SKILL.md` (style rules), `scripts/observe.py` (record original/final), `scripts/improve.py` (extract rules via LLM)
  - **Rule confidence:** P0/P1/P2 tiers — P0 auto-applied, backup before each update
  - **LLM support:** auto-detects `claude` (Claude Code) → `llm` (pip) → `IMPROVE_LLM_CMD` env var
  - **Install (Claude Code):** `cp -r writing-style-skill ~/.claude/skills/my-writing-style`
  - **Install (OpenClaw):** `npx clawhub@latest install jz-writing-style-skill`
  - **License:** MIT
  - **Topics:** claude-code, claude-skills, writing, productivity

## Previously Studied

## File Format / Reverse Engineering

### [github.com/obriensp/iWorkFileFormat](https://github.com/obriensp/iWorkFileFormat)
**Summary:** Authoritative reverse-engineered spec for Apple iWork 2013+ formats (Pages, Numbers, Keynote). Contains full protobuf message definitions, type ID mappings, and IWA archive format documentation.
- Added: 2026-03-20
- Status: Studied
- **Research report:** Removed from vault (file deleted — content was migrated to memory/note-taking workflows)
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

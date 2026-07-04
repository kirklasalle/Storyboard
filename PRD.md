# Product Requirements Document (PRD): Storyboard AI

> *"Every element is used because the story demands it — not as a syntax exercise."*
> — **ACS4.6** &nbsp;·&nbsp; Anthropic Claude Sonnet 4.6

## 1. Product Overview

Storyboard AI is a professional-grade web application that transforms screenplays into vivid, high-impact storyboard frames. The platform uses advanced Large Language Models (LLMs) to analyze narrative intensity, identify key cinematic moments, and dynamically generate corresponding visuals using various AI Image Generators.

## 2. Current Features

* **Script Parsing:** Accepts text-based screenplay uploads and partitions them into scenes using standard scene headings (INT./EXT.).
* **AI Narrative Analysis:** Evaluates each scene to extract the most 'storyboard-worthy' moment, ranking its cinematic intensity (Action Peak, Emotional Peak, Lull).
* **Multi-Provider LLM Integration:** Supports OpenAI, Anthropic, Google (Gemini), OpenRouter, Groq, and Local LLMs (via Ollama).
* **Storyboard Visualization:** Dynamically generates visual prompts from scene descriptions and renders realistic storyboard frames using Image Generation Models.
* **User Interface:** Interactive Gallery, Configuration Panel, and Uploader built with React and Tailwind CSS.

## 3. Future Enhancements & Upgrades (Target Features)

Based on user requirements and due diligence review, the following primary features must be developed:

### 3.1. Universal Document Compatibility

* **Requirement:** The application must read, write, and natively convert between *any* document type.
* **Supported Formats:** `.txt`, `.pdf`, `.docx`, `.fdx` (Final Draft), `.fountain`, `.epub`, `.cbz`/`.cbr` (Comic formats).
* **Target Scope:** Fully support screenplays, stage plays, graphic novels, and formatted storyboards.

### 3.2. Advanced AI Story Assistant

* **Requirement:** The LLM engine must deeply comprehend the narrative to provide active feedback.
* **Capabilities:**
  * **Formatting Helper:** Auto-correct standard script formatting (e.g., character names, dialogue alignment, scene headings).
  * **Structural Analysis:** Analyze the story's beat sheet, act structure, pacing, and character arcs.
  * **Story Ideation:** Pitch alternate scene angles, dialogue punch-ups, or twist ideas interactively to the user.

### 3.3. Multimodal Generation (Audio & Video Drivers)

* **Requirement:** Expand from purely Image generation to fully multimodal asset creation.
* **Image LM Driver:** Deepen controls (camera angles, lenses, character consistency sheets, LoRAs).
* **Audio LM Driver:** Generate voice-over (TTS), ambient soundscapes, or background scores for specific scene intensities.
* **Video LM Driver:** Transform static storyboard frames into animatics or short cinematic video clips using text-to-video or image-to-video LLMs.

## 4. Technical Constraints

* **File Processing Engine:** Must implement robust parser libraries for various document formats.
* **Cost & Latency Management:** High reliance on heavy multimodality (Video/Audio) requires queuing, asynchronous processing, and potentially cost-estimation warnings for API users.
* **Data Structure:** The database must evolve from purely `Script` -> `StoryboardFrame` to a more complex relational graph including `AudioClips`, `VideoRenders`, and `CharacterProfiles`.

---

## 5. Format Coverage Roadmap

### 5.1 Supported Formats (Implemented)

| Format | Extension | Parser | Status |
|--------|-----------|--------|--------|
| Plain Text Screenplay | `.txt` | `ScriptParser._parse_screenplay` | ✅ Live |
| Fountain | `.fountain` | `parsers/fountain_parser.py` | ✅ Live |
| Final Draft | `.fdx` | `parsers/fdx_parser.py` | ✅ Live |
| PDF | `.pdf` | `pdfplumber` | ✅ Live |
| Microsoft Word | `.docx` | `parsers/docx_parser.py` | ✅ Live |
| Stage Play (ACT/SCENE) | `.txt` | `ScriptParser._parse_structured` | ✅ Live |
| Chapter / Prose | `.txt` | `ScriptParser._parse_prose` | ✅ Live |
| A/V Two-Column Script | `.txt` | `ScriptParser._parse_structured` | ✅ Live |
| TV Episode (Teaser/Acts/Tag) | `.txt` | `ScriptParser._parse_structured` | ✅ Live |
| Episodic Series | `.txt` | `ScriptParser._parse_structured` | ✅ Live |

### 5.2 Formats in Pipeline (Roadmap)

| Format | Extension | Target | Notes |
|--------|-----------|--------|-------|
| ePub | `.epub` | Q3 2026 | For graphic novels and digital publications |
| Comic / Graphic Novel | `.cbz`, `.cbr` | Q3 2026 | Panel-by-panel parsing |
| Highland 2 | `.highland` | Q4 2026 | Popular macOS screenplay app |
| Celtx | `.celtx` | Q4 2026 | Legacy XML-based format |
| Adobe Story | `.astx` | Q4 2026 | XML-based, common in broadcast |
| Scrivener | `.scriv` | Q1 2027 | Complex project bundle format |
| Google Docs | API | Q2 2027 | Direct import via Google Drive API |
| Final Draft 12 | `.fdx v5` | Q3 2026 | FDX version 5 extended features |

### 5.3 Demo & Test Script Library

A full library of test scripts has been built at `backend/test_scripts/formats/`:

| File | Format | Type | Purpose |
|------|--------|------|---------|
| `sample_scifi_thriller.fountain` | Fountain | Sci-Fi Thriller | Tests Fountain parser, 10 scenes |
| `sample_noir_detective.fdx` | Final Draft FDX | Noir Drama | Tests FDX XML parser, 4 scenes |
| `sample_av_documentary.txt` | A/V Two-Column | Documentary | Tests structured parser |
| `sample_stage_play.txt` | Stage Play | Two-Act Drama | Tests ACT/SCENE parser |
| `sample_tv_episode.txt` | TV Format | One-Hour Procedural | Tests Teaser/Acts/Tag parser |
| `sample_novel_chapter.txt` | Prose/Chapters | Literary Fiction | Tests chapter parser |
| `sample_episodic_series.txt` | Episodic Web | 12-min Short Format | Tests episodic parser |

Plus 3 existing legacy test scripts: `noir_3min.txt`, `drama_5min.txt`, `sci_fi_1min.txt`.

**Total: 10 test documents covering 8 distinct format types.**

### 5.4 Format Benchmark Tool

Run `python backend/benchmark_formats.py` to generate a full performance report:

* Parse time (milliseconds) per document
* Format detection accuracy
* Scene count, character count, word count
* Coverage matrix (which formats were tested)
* Output saved to `logs/format_benchmark_YYYYMMDD.log`

---

## 6. Content Agreement & Data Policy

### 6.1 User Content Agreement (Immutable)

All submitted writing is governed by the **Storyboard AI User Content Agreement** (`backend/content_agreement.py`). This agreement is:

* **Irrevocable** upon submission
* **Immutable** — cannot be modified without a Governance Council review
* **Governed** by Kirk LaSalle's Permanent Active Directives (The 10 Laws)

### 6.2 The Memory Model

Storyboard AI operates on a **human memory model** for all submitted content:

> *"Like a skilled cinematographer who reads a thousand scripts — they remember the craft, the patterns, the emotional truth. They do not remember the specific words."*

* Raw submitted content is **processed then discarded** — never stored permanently
* Only **distilled cinematic insights** are added to the Knowledge Base
* Users **retain full copyright** to all submitted work
* **No personally identifiable information** is stored in the Knowledge Base

### 6.3 Compliance with The 10 Laws

| Law | Requirement | Implementation |
|-----|-------------|----------------|
| Law 6 (Privacy) | Protect data confidentiality | Raw content discarded; only craft insights retained |
| Law 7 (Transparency) | No deception | Agreement shown before upload; audit log records acceptance |
| Law 8 (Equity) | No bias | All content treated equally regardless of submitter |
| Law 9 (Audit) | Transparent ledger | Every acceptance logged to `logs/governance_audit.log` |

### 6.4 Knowledge Base Growth

The Cinematic Knowledge Base grows with every script analyzed:

1. Script submitted → analyzed → raw content discarded
2. LLM distills 3-5 craft insights from the analysis
3. Insights added to KB with genre tag, confidence score, and source attribution
4. Future analyses are enriched by accumulated wisdom
5. The KB is queryable via `GET /knowledge` and `GET /knowledge/stats`

---

## 7. Governance Framework

All autonomous AI operations in Storyboard AI are governed by:

* **PRISM Agentic Prime Directive** (`AGENTIC_PRIME_DIRECTIVE.md`)
* **PRISM Sacred Covenant** (`AGENTIC_SACRED_COVENANT.md`)
* **Kirk LaSalle's Permanent Active Directives** (`Permanent_Active_Directives.txt`) — The 10 Laws

These are embedded cryptographically in `backend/governance.py` and verified at every application boot. The `/governance` API endpoint exposes the full framework.

---

## 8. Quality Spectrum — Story Craft Levels

The test script library includes a three-level quality spectrum (`backend/test_scripts/spectrum/`) that demonstrates the same scene written at three distinct levels of craft. Used as training data for the Cinematic Knowledge Base and as a calibration reference for analysis quality.

| Level | Description | What it produces |
|-------|-------------|-----------------|
| **L1 — Basic** | Functional. Facts communicated. No subtext. Characters as functions. | The audience knows what happened. |
| **L2 — Professional** | Competent craft. Subtext present. Scene has shape. Characters have voices. | The audience feels the tension. |
| **L3 — Oscar / World-Class** | Every word load-bearing. Final image is the scene's real last line. | The audience carries something home. |

**Files:** `L1_screenplay.txt`, `L2_screenplay.txt`, `L3_screenplay.txt`, `L1_fountain.fountain`, `L2_fountain.fountain`, `L3_fountain.fountain`, `L123_stage_play.txt`, `L123_av_script.txt`

*"The distance from Level 1 to Level 3 is not vocabulary or technique — it is specificity earned by observation, subtext earned by trusting the reader, and the image that does the work the words no longer need to."* — ACS4.6

---

## 9. Character Database & Library

### 9.1 Per-Project Character Profiles

Every script analysis automatically extracts and profiles all named characters:

* **Visual Profile**: Full physical description, age range, wardrobe signature
* **Image Consistency Prompt**: Compact phrase injected into all image generation calls for that character — ensures the same face appears across all frames
* **Voice Assignment**: One of 6 OpenAI TTS voices (alloy, echo, fable, onyx, nova, shimmer) for read-through casting
* **Scene Tracking**: Scene count, line count, first appearance, lead status

### 9.2 Global Character Archetype Library

A growing cross-project archetype database seeded with 12 foundational types and expanded by every project analyzed.

**Taxonomy — 18,432 possible type combinations:**

| Dimension | Count | Examples |
|-----------|-------|---------|
| Narrative Roles | 16 | protagonist, antagonist, mentor, trickster, shapeshifter, narrator |
| Jungian Archetypes | 12 | the_hero, the_sage, the_rebel, the_lover, the_magician |
| Production Tiers | 6 | series_regular, recurring, guest_star, day_player, voice_only |
| Genre Types | 16 | noir_detective, femme_fatale, whistleblower, tragic_hero, journalist |

**API:** `GET /characters/library`, `GET /characters/library/taxonomy`, `GET /projects/{id}/characters`

### 9.3 TTS Read-Through (Virtual Characters)

Infrastructure for TTS-driven virtual read-throughs:

* **Cast List:** `GET /projects/{id}/readthrough/cast` — all characters with voice assignments
* **Line Generation:** `POST /projects/{id}/readthrough/generate` — single line TTS via OpenAI
* **Full read-through** (roadmap): Sequential line generation with per-character voice, exported as audio track
* **Voice Profiles**: alloy (neutral narrator), echo (intellectual male), fable (warm expressive), onyx (deep authority), nova (warm female lead), shimmer (bright/young)

---

## 10. Export Capabilities

| Export | Endpoint | Format | Use Case |
|--------|----------|--------|---------|
| Shot List | `GET /projects/{id}/export/shot-list.csv` | CSV | DPs and ADs on set |
| Fountain Script | `GET /projects/{id}/export/script.fountain` | .fountain | Round-trip back to writer's tools |
| PDF Storyboard | (via ExportService) | PDF | Client presentations |
| Image ZIP | (via ExportService) | ZIP | Frame delivery |

---

## 11. Test Suite

**71 tests passing at 0.89 seconds.** Run with: `python -m pytest backend/tests/ -v`

| Module | Tests | Coverage |
|--------|-------|---------|
| `test_parsers.py` | 23 | FDX, Fountain, format detector, ScriptParser cascade, character extraction |
| `test_style_vault.py` | 10 | All 16 styles, required fields, fallback behavior |
| `test_genre_vault.py` | 12 | All 18 genres, alias resolution, case insensitivity, fallback |
| `test_crypto.py` | 10 | Encrypt/decrypt round-trip, legacy passthrough, edge cases |
| `test_character_library.py` | 16 | Taxonomy counts, seed archetypes, voice profiles, combinations |

# COUNTING.md — Canonical Lesson-Metric Counting Model

**The single authoritative definition of how lesson metrics are computed, consumed, and reported.**

**Status:** Authoritative (operationalizes `METADATA_GOVERNANCE_CONTRACT.md` §3 / M0, and `GOVERNANCE_SPEC_v1.0_FINAL.md` Part 5).
**Scope:** `D:\Global Lessons\global_lessons.md` only.
**Owner:** PM (Mahmoud Elshahed). Changed only by deliberate edit; tooling conforms to this document.
**Rule of this file:** it defines *how to count*, never *the counts themselves*. **No numeric totals are stored here** — values are derived live by `hooks/health_check.py` ("Lesson Metric Vector" check). This keeps COUNTING.md from becoming a count-drift sink.

---

## 1. Canonical counting rules (the only valid methods)

Line-anchored, multiline; must not match across newlines.

| Quantity | Rule | Notes |
|---|---|---|
| Lesson **entry** lines | regex `^[0-9]+\.\s+\*\*` | each raw numbered lesson line the parser ingests |
| Leading **identifier** | the integer captured by `^([0-9]+)\.\s+\*\*` | the lesson's number |
| **Category** | regex `^## ` | every H2 header (incl. undated + "(continued)" reopenings) |

All five metrics below derive from the *set of leading identifiers* produced by the entry rule. `health_check.py` implements exactly these rules — there is no second method.

---

## 2. The metric vector (five values — never collapsed to one)

### 2.1 First-class metrics (independent; a consumer must NAME the one it uses)

| Metric | Definition | Purpose | **Allowed consumers** |
|---|---|---|---|
| **`distinct_count`** | count of **unique** leading identifiers | *identity truth* — "how many lessons exist" | corpus-size statements; coverage/dedup analysis; human prose (default) |
| **`entries_count`** | count of **all** entry lines (incl. reused numbers) | *ingestion reality* — "how many lesson lines the parser sees" | parse/integrity completeness checks; the legacy `Lesson Count` check |
| **`max_index_plus_one`** | `max(identifier) + 1` | *allocation safety* — "the next safe number to assign" | the lesson-allocation path (`/PM-lessons-add`) **only** |

### 2.2 Derived signals (observability only — NOT invariants, never gate allocation)

| Signal | Formula | Meaning |
|---|---|---|
| **`duplication_delta`** | `entries_count − distinct_count` | count of **duplicate identifiers** (the same number used by >1 entry) — a **data-quality** signal |
| **`retirement_gap`** | `max_index − distinct_count` | count of **retired/absent** numbers (gaps left by folding/compression) — a corpus-evolution signal |

---

## 3. Hard rules

### 3.1 No scalar collapse (METRIC-INV-1)
**No artifact, manifest, display, or consumer may reduce these to a single "canonical lesson count."** Any "the lesson count is N" is an invalid representation. Every consumer **names** the metric it uses. For loose human prose, the **documented default is `distinct_count`** — but this default is *not* privileged; tooling may never rely on it and must name a metric.

### 3.2 Why allocation uses `max_index_plus_one` (not `distinct_count + 1`)
Folding/compression **retires** numbers, so identifiers are **non-contiguous** and `distinct_count < max_index`. The next *safe* identifier is therefore `max_index + 1`. Using `distinct_count + 1` would point **inside the used range** and **collide** with an existing lesson. (Concretely: with distinct≈929 but max≈1014, `distinct+1` = ~930 — already taken; `max+1` = ~1015 — safe.) **Allocation MUST use `max_index_plus_one`.**

### 3.3 Why reporting uses the vector (not one number)
The three first-class metrics answer three different questions, and their pairwise gaps are diagnostic: `duplication_delta` surfaces duplicate-identifier data-quality issues, `retirement_gap` surfaces folding. A single headline number erases both signals and mis-serves at least one consumer (the allocator). Reporting therefore always emits the **full vector + both deltas + an as-of date**.

### 3.4 Single source of truth
The counting *logic* lives once, in `hooks/health_check.py` (`_compute_lesson_metrics`). COUNTING.md is the *definition*; `health_check` is the *reporter*; `global_lessons.md` content is the *source*. No file stores a count as authoritative.

---

## 4. Consumers map (who may read what)

| Consumer | May use | Must NOT use |
|---|---|---|
| `/PM-lessons-add` (allocate next number) | `max_index_plus_one` | `distinct_count`/`entries_count` for allocation |
| README / prose / corpus-size | `distinct_count` (named, + as-of) | any value as an evergreen scalar |
| `health_check` `Lesson Count` (legacy) | `entries_count` | — |
| parse/integrity tooling | `entries_count` | — |
| data-quality / dedup audit | `distinct_count` + `duplication_delta` | — |
| observability / trend | `duplication_delta`, `retirement_gap` | these to gate allocation |

---

## 5. Governance alignment (this document)
- **M0 contract:** operationalizes M0 §3 (canonical rules) + the metric-vector model; stores no counts (M0 "derived, never hand-authored"). ✓
- **Single source of truth:** counting logic centralized in `health_check._compute_lesson_metrics`; one definition (here), one reporter (health_check). ✓
- **Anti-duplication / Anti-sprawl (#770):** **no new tool, agent, or command** — the reporter is an *extension* of the existing `health_check`; this doc + that extension are the entire footprint. ✓
- **No scalar collapse:** §3.1 enforced; the reporter emits the vector, never a single number. ✓

*Operational doc — defines the model and its consumers. Values are derived live; see `hooks/health_check.py` → "Lesson Metric Vector".*

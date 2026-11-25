"""aptitude_questions/__init__.py — Aggregates all aptitude question modules.

Imports QUESTIONS lists from each topic module and merges them into
ALL_APTITUDE_QUESTIONS used by the aptitude engine.
"""

import logging

logger = logging.getLogger(__name__)

ALL_APTITUDE_QUESTIONS: list[dict] = []

# ── Load each module safely (graceful fallback if a file is missing) ──────────

def _safe_load(module_name: str, attr: str = "QUESTIONS") -> list[dict]:
    try:
        import importlib
        mod = importlib.import_module(f"aptitude_questions.{module_name}")
        questions = getattr(mod, attr, [])
        logger.info("Loaded %d questions from %s.", len(questions), module_name)
        return questions
    except Exception as exc:
        logger.warning("Could not load aptitude_questions.%s: %s", module_name, exc)
        return []


# Phase 1-3: Percentages, Ratios, Averages, Mixtures, Profit & Loss
ALL_APTITUDE_QUESTIONS += _safe_load("quantitative")

# Phase 4-6: Time & Work, Pipes, Speed & Distance, Interest
ALL_APTITUDE_QUESTIONS += _safe_load("time_work_speed")

# Phase 7-10: Number System, PnC, Probability, Logical Reasoning
ALL_APTITUDE_QUESTIONS += _safe_load("number_perm_prob")

# Phase 11-13: DI, Verbal Ability, Spatial Reasoning, Mixed Aptitude
ALL_APTITUDE_QUESTIONS += _safe_load("di_verbal_spatial")

# ── Deduplication by ID ───────────────────────────────────────────────────────
seen_ids: set[str] = set()
deduped: list[dict] = []
for q in ALL_APTITUDE_QUESTIONS:
    qid = q.get("id", "")
    if qid and qid not in seen_ids:
        seen_ids.add(qid)
        deduped.append(q)
    elif not qid:
        logger.warning("Question missing 'id' field: %s", str(q)[:80])

ALL_APTITUDE_QUESTIONS = deduped
logger.info("Total aptitude questions loaded: %d", len(ALL_APTITUDE_QUESTIONS))

# ── Validation ────────────────────────────────────────────────────────────────
REQUIRED_FIELDS = {"id", "phase", "subject", "topic", "type", "q", "answer", "explanation"}

invalid_count = 0
for q in ALL_APTITUDE_QUESTIONS:
    missing = REQUIRED_FIELDS - set(q.keys())
    if missing:
        logger.warning("Question '%s' missing fields: %s", q.get("id", "?"), missing)
        invalid_count += 1

if invalid_count:
    logger.warning("%d questions have missing required fields.", invalid_count)

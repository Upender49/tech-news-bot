"""
quiz_generator.py — CS Fundamentals quiz engine.

Replaces fetcher.py + filter.py + formatter.py from the old news pipeline.

Flow:
  1. load_quiz_state()  — read which question IDs were already sent
  2. pick_questions()   — select 5 unseen questions rotating across topics
  3. build_quiz_message() — format them as a clean Telegram HTML message
  4. After send: save_quiz_state() — persist the newly sent IDs
"""

import json
import logging
import random
from datetime import datetime, timezone
from pathlib import Path

from question_bank import QUESTIONS

logger = logging.getLogger(__name__)

# ── State file (committed back to repo, same pattern as sent_urls.json) ────────
QUIZ_STATE_FILE = Path(__file__).parent / "quiz_state.json"

# How many questions per message
QUESTIONS_PER_QUIZ = 5

# Max IDs to remember (prevents file growing forever)
MAX_STORED_IDS = 300

# Topic rotation order — cycles through and repeats
TOPIC_ROTATION: list[str] = [
    "Data Structures",
    "Algorithms",
    "Operating Systems",
    "Databases",
    "Computer Networks",
    "Object-Oriented Programming",
    "Programming Fundamentals",
    "System Design",
    "Software Engineering",
    "Computer Architecture",
    "Web Fundamentals",
]

# Difficulty mix for 5 questions
DIFFICULTY_MIX: list[str] = ["easy", "medium", "medium", "interview", "tricky"]


# ── State I/O ─────────────────────────────────────────────────────────────────

def load_quiz_state() -> dict:
    """
    Load quiz state from disk.
    Returns {sent_ids: list[str], topic_index: int}
    """
    if not QUIZ_STATE_FILE.exists():
        logger.info("No quiz state file found — starting fresh.")
        return {"sent_ids": [], "topic_index": 0}
    try:
        with open(QUIZ_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(
            "Quiz state loaded: %d sent IDs, next topic index %d.",
            len(data.get("sent_ids", [])),
            data.get("topic_index", 0),
        )
        return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read quiz state (%s) — starting fresh.", exc)
        return {"sent_ids": [], "topic_index": 0}


def save_quiz_state(state: dict, new_ids: list[str]) -> None:
    """Merge new_ids into state and persist to disk."""
    existing = state.get("sent_ids", [])
    combined = [i for i in existing if i not in new_ids] + new_ids
    trimmed = combined[-MAX_STORED_IDS:]

    new_state = {
        "sent_ids": trimmed,
        "topic_index": state.get("topic_index", 0),
    }
    try:
        with open(QUIZ_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(new_state, f, indent=2, ensure_ascii=False)
        logger.info("Quiz state saved: %d total IDs tracked.", len(trimmed))
    except OSError as exc:
        logger.error("Could not write quiz state: %s", exc)


# ── Question selection ─────────────────────────────────────────────────────────

def pick_questions(state: dict) -> tuple[list[dict], dict]:
    """
    Select QUESTIONS_PER_QUIZ questions using topic rotation and difficulty mix.
    Returns (selected_questions, updated_state).
    """
    sent_ids: set[str] = set(state.get("sent_ids", []))
    topic_index: int = state.get("topic_index", 0)

    # Unseen questions pool
    unseen = [q for q in QUESTIONS if q["id"] not in sent_ids]

    # If more than 80% of questions have been seen, reset to avoid drying up
    if len(unseen) < QUESTIONS_PER_QUIZ:
        logger.info("Less than %d unseen questions — resetting sent history.", QUESTIONS_PER_QUIZ)
        sent_ids = set()
        unseen = list(QUESTIONS)
        state["sent_ids"] = []

    # Primary topic for this session
    primary_topic = TOPIC_ROTATION[topic_index % len(TOPIC_ROTATION)]
    next_topic_index = (topic_index + 1) % len(TOPIC_ROTATION)
    state["topic_index"] = next_topic_index

    logger.info("Primary topic this session: %s", primary_topic)

    selected: list[dict] = []
    topics_used: list[str] = []

    # Try to fill using difficulty mix, preferring primary topic
    for difficulty in DIFFICULTY_MIX:
        # First: primary topic + matching difficulty
        candidates = [
            q for q in unseen
            if q["topic"] == primary_topic
            and q["difficulty"] == difficulty
            and q["id"] not in {s["id"] for s in selected}
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            topics_used.append(chosen["topic"])
            continue

        # Second: any topic + matching difficulty
        candidates = [
            q for q in unseen
            if q["difficulty"] == difficulty
            and q["id"] not in {s["id"] for s in selected}
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            topics_used.append(chosen["topic"])
            continue

        # Fallback: any unseen question
        candidates = [
            q for q in unseen
            if q["id"] not in {s["id"] for s in selected}
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            topics_used.append(chosen["topic"])

    logger.info(
        "Selected %d questions. Topics: %s",
        len(selected),
        ", ".join(topics_used),
    )
    return selected, state


# ── Message formatter ─────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    """Minimal HTML escaping for Telegram HTML mode."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _difficulty_stars(difficulty: str) -> str:
    mapping = {
        "easy":      "⭐☆☆☆☆",
        "medium":    "⭐⭐⭐☆☆",
        "interview": "⭐⭐⭐⭐☆",
        "tricky":    "⭐⭐⭐⭐⭐",
        "hard":      "⭐⭐⭐⭐⭐",
    }
    return mapping.get(difficulty, "⭐⭐⭐☆☆")


def _format_question_block(number: int, q: dict) -> str:
    """Format a single question with its options."""
    lines = [f"<b>Q{number}.</b> {_esc(q['q'])}"]
    lines.append("")
    for opt_key in ("A", "B", "C", "D"):
        opt_val = q["options"].get(opt_key, "")
        lines.append(f"  <b>{opt_key})</b> {_esc(opt_val)}")
    return "\n".join(lines)


def _format_answer_block(number: int, q: dict) -> str:
    """Format the answer + explanation for one question."""
    answer_key = q["answer"]
    answer_val = q["options"].get(answer_key, "")
    stars = _difficulty_stars(q["difficulty"])

    lines = [
        f"<b>{number}️⃣ Ans: {answer_key}) {_esc(answer_val)}</b>",
        f"🎯 Difficulty: {stars}",
        f"📘 {_esc(q['explanation'])}",
    ]
    if q.get("tip"):
        lines.append(f"\n💡 <b>Interview Tip:</b> {_esc(q['tip'])}")
    return "\n".join(lines)


def build_quiz_message(questions: list[dict]) -> tuple[str, str]:
    """
    Build the complete Telegram quiz message.
    Returns (message_text, parse_mode).
    """
    if not questions:
        return (
            "🧠 <b>CS FUNDAMENTALS — DAILY QUIZ</b>\n\n"
            "No questions available right now. Check back soon!",
            "HTML",
        )

    now_utc = datetime.now(timezone.utc).strftime("%d %b %Y · %I:%M %p UTC")
    topics_shown = sorted(set(q["topic"] for q in questions))
    avg_diff_map = {"easy": 1, "medium": 3, "interview": 4, "tricky": 5, "hard": 5}
    avg_diff = sum(avg_diff_map.get(q["difficulty"], 3) for q in questions) / len(questions)
    overall_stars = "⭐" * round(avg_diff) + "☆" * (5 - round(avg_diff))

    # ── HEADER ────────────────────────────────────────────────────────────────
    parts = [
        "🧠 <b>CS FUNDAMENTALS — DAILY QUIZ</b>",
        f"📅 <i>{now_utc}</i>",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    # ── QUESTIONS ─────────────────────────────────────────────────────────────
    for i, q in enumerate(questions, start=1):
        parts.append(_format_question_block(i, q))
        parts.append("━━━━━━━━━━━━━━━━━━━━━━━━")
        parts.append("")

    # ── ANSWERS SECTION ───────────────────────────────────────────────────────
    parts.append("📝 <b>ANSWERS &amp; EXPLANATIONS</b>")
    parts.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    parts.append("")

    for i, q in enumerate(questions, start=1):
        parts.append(_format_answer_block(i, q))
        parts.append("")

    # ── FOOTER ────────────────────────────────────────────────────────────────
    parts.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    parts.append(f"🎯 <b>Today's Topics:</b> {_esc(', '.join(topics_shown))}")
    parts.append(f"📊 <b>Overall Difficulty:</b> {overall_stars}")
    parts.append("")
    parts.append("💪 Keep learning. Keep growing!")
    parts.append("#CSFundamentals #PlacementPrep #TechInterview #CSE")

    message = "\n".join(parts)
    logger.info("Quiz message built: %d chars, %d questions.", len(message), len(questions))
    return message, "HTML"

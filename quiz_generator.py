"""
quiz_generator.py — CS Fundamentals quiz engine.

Replaces fetcher.py + filter.py + formatter.py from the old news pipeline.

Flow:
  1. load_quiz_state()        — read which question IDs were already sent
  2. pick_questions()         — select questions rotating across topics
  3. build_questions_message()— Part 1: questions only (fits in one Telegram message)
  4. build_answers_message()  — Part 2: answers + explanations (fits in one message)
  5. After send: save_quiz_state() — persist the newly sent IDs
"""

import json
import logging
import random
import re
from datetime import datetime, timezone
from pathlib import Path

from question_bank import QUESTIONS

logger = logging.getLogger(__name__)

# ── State file ────────────────────────────────────────────────────────────────
QUIZ_STATE_FILE = Path(__file__).parent / "quiz_state.json"

# How many questions per quiz
QUESTIONS_PER_QUIZ = 10

# Max IDs to remember
MAX_STORED_IDS = 500

# Topic rotation order
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

# Difficulty mix for 10 questions
DIFFICULTY_MIX: list[str] = [
    "easy",
    "easy",
    "medium",
    "medium",
    "medium",
    "medium",
    "interview",
    "interview",
    "tricky",
    "tricky",
]


# ── State I/O ─────────────────────────────────────────────────────────────────

def load_quiz_state() -> dict:
    """Load quiz state. Returns {sent_ids: list, topic_index: int}."""
    if not QUIZ_STATE_FILE.exists():
        logger.info("No quiz state file — starting fresh.")
        return {"sent_ids": [], "topic_index": 0}
    try:
        with open(QUIZ_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(
            "Quiz state loaded: %d sent IDs, topic index %d.",
            len(data.get("sent_ids", [])),
            data.get("topic_index", 0),
        )
        return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read quiz state (%s) — starting fresh.", exc)
        return {"sent_ids": [], "topic_index": 0}


def save_quiz_state(state: dict, new_ids: list[str]) -> None:
    """Merge new_ids into state and persist."""
    existing = state.get("sent_ids", [])
    combined = [i for i in existing if i not in new_ids] + new_ids
    trimmed = combined[-MAX_STORED_IDS:]
    new_state = {"sent_ids": trimmed, "topic_index": state.get("topic_index", 0)}
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

    unseen = [q for q in QUESTIONS if q["id"] not in sent_ids]

    # Reset if fewer than needed
    if len(unseen) < QUESTIONS_PER_QUIZ:
        logger.info("Resetting sent history (only %d unseen).", len(unseen))
        sent_ids = set()
        unseen = list(QUESTIONS)
        state["sent_ids"] = []

    primary_topic = TOPIC_ROTATION[topic_index % len(TOPIC_ROTATION)]
    state["topic_index"] = (topic_index + 1) % len(TOPIC_ROTATION)
    logger.info("Primary topic this session: %s", primary_topic)

    selected: list[dict] = []

    for difficulty in DIFFICULTY_MIX:
        selected_ids = {s["id"] for s in selected}

        # Try primary topic + difficulty
        candidates = [
            q for q in unseen
            if q["topic"] == primary_topic
            and q["difficulty"] == difficulty
            and q["id"] not in selected_ids
        ]
        if candidates:
            selected.append(random.choice(candidates))
            continue

        # Any topic + difficulty
        candidates = [
            q for q in unseen
            if q["difficulty"] == difficulty
            and q["id"] not in selected_ids
        ]
        if candidates:
            selected.append(random.choice(candidates))
            continue

        # Any unseen question as fallback
        candidates = [q for q in unseen if q["id"] not in selected_ids]
        if candidates:
            selected.append(random.choice(candidates))

    topics_used = [q["topic"] for q in selected]
    logger.info("Selected %d questions. Topics: %s", len(selected), ", ".join(topics_used))
    return selected, state


# ── HTML helpers ──────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    """Escape plain text for Telegram HTML mode."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def _text_to_html(text: str) -> str:
    """
    Convert text that may contain ```code blocks``` to Telegram-safe HTML.
    Everything outside code blocks is HTML-escaped.
    Code blocks are wrapped in <pre><code>...</code></pre>.
    """
    parts: list[str] = []
    pattern = re.compile(r'```(?:\w*)\n(.*?)```', re.DOTALL)
    last_end = 0
    for m in pattern.finditer(text):
        before = text[last_end:m.start()]
        if before:
            parts.append(_esc(before))
        code_content = m.group(1)
        parts.append(f"<pre><code>{_esc(code_content)}</code></pre>")
        last_end = m.end()
    remaining = text[last_end:]
    if remaining:
        parts.append(_esc(remaining))
    return "".join(parts)


def _difficulty_stars(difficulty: str) -> str:
    mapping = {
        "easy":      "⭐☆☆☆☆ Easy",
        "medium":    "⭐⭐⭐☆☆ Medium",
        "interview": "⭐⭐⭐⭐☆ Interview-level",
        "tricky":    "⭐⭐⭐⭐⭐ Tricky/Advanced",
        "hard":      "⭐⭐⭐⭐⭐ Hard",
    }
    return mapping.get(difficulty, "⭐⭐⭐☆☆")


# ── Message builders ─────────────────────────────────────────────────────────

def build_questions_message(questions: list[dict]) -> str:
    """
    Part 1: Questions only.
    Compact format — no explanations, so always fits in one Telegram message.
    """
    now_utc = datetime.now(timezone.utc).strftime("%d %b %Y · %I:%M %p UTC")
    topics = sorted(set(q["topic"] for q in questions))

    lines = [
        "🧠 <b>CS FUNDAMENTALS QUIZ</b>",
        f"📅 <i>{now_utc}</i>",
        f"📚 Topics: <i>{_esc(', '.join(topics))}</i>",
        f"❓ {len(questions)} questions • Try to answer before scrolling!",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    for i, q in enumerate(questions, start=1):
        # Question text (handles code blocks)
        q_html = _text_to_html(q["q"])
        lines.append(f"<b>Q{i}.</b> {q_html}")
        lines.append("")
        for key in ("A", "B", "C", "D"):
            val = q["options"].get(key, "")
            lines.append(f"  {key}) {_esc(val)}")
        lines.append("─ ─ ─ ─ ─ ─ ─ ─ ─ ─")
        lines.append("")

    lines.append("✏️ <b>Answer key in the next message ↓</b>")

    return "\n".join(lines)


def _build_answers_block(questions: list[dict], start_num: int, label: str) -> str:
    """Build an answers block for a subset of questions."""
    lines = [
        f"📝 <b>ANSWERS &amp; EXPLANATIONS {label}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]
    for i, q in enumerate(questions, start=start_num):
        answer_key = q["answer"]
        answer_val = q["options"].get(answer_key, "")
        stars = _difficulty_stars(q["difficulty"])
        lines.append(f"<b>{i}. {_esc(answer_val)}</b> ✅ ({answer_key})")
        lines.append(f"📊 {stars}")
        lines.append(f"💬 {_text_to_html(q['explanation'])}")
        if q.get("tip"):
            lines.append(f"💡 <b>Interview Tip:</b> {_esc(q['tip'])}")
        lines.append("")
    return "\n".join(lines)


def build_quiz_messages(questions: list[dict]) -> tuple[list[str], str]:
    """
    Build all quiz messages and return (list_of_messages, parse_mode).

    For 10 questions, returns 3 messages:
      [0] Questions 1-10 (compact, always fits)
      [1] Answers 1-5   (fits under 4096)
      [2] Answers 6-10 + footer (fits under 4096)
    """
    if not questions:
        fallback = "🧠 <b>CS FUNDAMENTALS</b>\n\nNo questions available. Check back soon!"
        return [fallback], "HTML"

    mid = len(questions) // 2
    first_half  = questions[:mid]
    second_half = questions[mid:]

    q_msg  = build_questions_message(questions)
    a1_msg = _build_answers_block(first_half,  start_num=1,       label=f"(Q1–{mid})")
    a2_body= _build_answers_block(second_half, start_num=mid + 1, label=f"(Q{mid+1}–{len(questions)})")

    # Append footer to the last answers message
    footer = (
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💪 <b>Keep learning. Keep growing!</b>\n"
        "#CSFundamentals #PlacementPrep #TechInterview #CSE"
    )
    a2_msg = a2_body + "\n" + footer

    messages = [q_msg, a1_msg, a2_msg]
    logger.info(
        "Messages built: Q=%d, A1=%d, A2=%d chars (limit 4096).",
        len(q_msg), len(a1_msg), len(a2_msg),
    )
    return messages, "HTML"

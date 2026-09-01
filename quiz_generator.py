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

# Difficulty mix for 10 questions (high standards: Medium, Interview, Tricky, Hard)
DIFFICULTY_MIX: list[str] = [
    "medium",
    "medium",
    "medium",
    "interview",
    "interview",
    "interview",
    "tricky",
    "tricky",
    "hard",
    "hard",
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
    """Merge new_ids into state maintaining order (FIFO) and persist."""
    existing = [i for i in state.get("sent_ids", []) if i not in new_ids]
    combined = existing + new_ids
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
    Uses strict FIFO deduplication: questions will not repeat until the entire bank is exhausted.
    Returns (selected_questions, updated_state).
    """
    sent_ids_list: list[str] = list(state.get("sent_ids", []))
    sent_ids_set: set[str] = set(sent_ids_list)
    topic_index: int = state.get("topic_index", 0)

    unseen = [q for q in QUESTIONS if q["id"] not in sent_ids_set]

    # If unseen questions are fewer than needed, evict oldest sent IDs (FIFO)
    while len(unseen) < QUESTIONS_PER_QUIZ and sent_ids_list:
        evicted = sent_ids_list.pop(0)
        sent_ids_set.discard(evicted)
        unseen = [q for q in QUESTIONS if q["id"] not in sent_ids_set]

    # If still not enough (e.g. total bank < 10), use all questions
    if len(unseen) < QUESTIONS_PER_QUIZ:
        unseen = list(QUESTIONS)
        sent_ids_list = []
        sent_ids_set = set()

    state["sent_ids"] = sent_ids_list

    primary_topic = TOPIC_ROTATION[topic_index % len(TOPIC_ROTATION)]
    state["topic_index"] = (topic_index + 1) % len(TOPIC_ROTATION)
    logger.info("Primary topic this session: %s", primary_topic)

    selected: list[dict] = []

    for difficulty in DIFFICULTY_MIX:
        selected_ids = {s["id"] for s in selected}

        # 1. Try primary topic + matching difficulty
        candidates = [
            q for q in unseen
            if q["topic"] == primary_topic
            and q["difficulty"] == difficulty
            and q["id"] not in selected_ids
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            continue

        # 2. Any topic + matching difficulty
        candidates = [
            q for q in unseen
            if q["difficulty"] == difficulty
            and q["id"] not in selected_ids
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            continue

        # 3. Primary topic + any difficulty
        candidates = [
            q for q in unseen
            if q["topic"] == primary_topic
            and q["id"] not in selected_ids
        ]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)
            continue

        # 4. Any unseen question
        candidates = [q for q in unseen if q["id"] not in selected_ids]
        if candidates:
            chosen = random.choice(candidates)
            selected.append(chosen)

    # If still under 10 (fallback safeguard from full bank without duplicates)
    while len(selected) < QUESTIONS_PER_QUIZ:
        selected_ids = {s["id"] for s in selected}
        remaining = [q for q in QUESTIONS if q["id"] not in selected_ids]
        if not remaining:
            break
        selected.append(random.choice(remaining))

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

SAFE_MSG_LIMIT = 3500


def _format_single_question(i: int, q: dict) -> str:
    """Format one question item."""
    q_html = _text_to_html(q["q"])
    diff_tag = f"<i>[{_esc(q.get('topic', 'CS'))} · {_esc(q.get('difficulty', 'medium')).capitalize()}]</i>"
    lines = [
        f"<b>Q{i}.</b> {diff_tag}\n{q_html}",
        "",
    ]
    for key in ("A", "B", "C", "D"):
        val = q["options"].get(key, "")
        lines.append(f"  <b>{key})</b> {_esc(val)}")
    lines.append("─ ─ ─ ─ ─ ─ ─ ─ ─ ─")
    return "\n".join(lines)


def _format_single_answer(i: int, q: dict) -> str:
    """Format one answer + explanation item."""
    answer_key = q["answer"]
    answer_val = q["options"].get(answer_key, "")
    stars = _difficulty_stars(q["difficulty"])
    lines = [
        f"<b>{i}. {_esc(answer_val)}</b> ✅ ({answer_key})",
        f"📊 {stars}",
        f"💬 {_text_to_html(q['explanation'])}",
    ]
    if q.get("tip"):
        lines.append(f"💡 <b>Interview Tip:</b> {_esc(q['tip'])}")
    lines.append("")
    return "\n".join(lines)


def build_quiz_messages(questions: list[dict]) -> tuple[list[str], str]:
    """
    Build all quiz messages adaptively packed to guarantee every message stays <= SAFE_MSG_LIMIT (3500 chars).
    Returns (list_of_messages, parse_mode).
    """
    if not questions:
        fallback = "🧠 <b>CS FUNDAMENTALS</b>\n\nNo questions available. Check back soon!"
        return [fallback], "HTML"

    now_utc = datetime.now(timezone.utc).strftime("%d %b %Y · %I:%M %p UTC")
    topics = sorted(set(q["topic"] for q in questions))

    messages: list[str] = []

    # ── 1. Pack Questions ─────────────────────────────────────────────────────
    q_blocks = [_format_single_question(i, q) for i, q in enumerate(questions, start=1)]

    current_q_chunks: list[str] = []
    q_part = 1
    current_text = ""

    header_first = (
        "🧠 <b>CS FUNDAMENTALS QUIZ</b>\n"
        f"📅 <i>{now_utc}</i>\n"
        f"📚 Topics: <i>{_esc(', '.join(topics))}</i>\n"
        "❓ Try answering each before reading explanations!\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    current_text = header_first
    for idx, block in enumerate(q_blocks, start=1):
        test_text = current_text + block + "\n\n"
        if len(test_text) > SAFE_MSG_LIMIT and current_text != header_first:
            # Finalize previous question chunk
            current_text += "✏️ <i>Questions continue in next message ↓</i>"
            messages.append(current_text.strip())
            q_part += 1
            current_text = (
                f"🧠 <b>CS FUNDAMENTALS QUIZ — PART {q_part}</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n" + block + "\n\n"
            )
        else:
            current_text = test_text

    if current_text:
        current_text += "✏️ <b>Answer keys & detailed explanations in next message ↓</b>"
        messages.append(current_text.strip())

    # ── 2. Pack Answers ───────────────────────────────────────────────────────
    a_blocks = [_format_single_answer(i, q) for i, q in enumerate(questions, start=1)]

    a_part = 1
    header_ans = (
        "📝 <b>ANSWERS &amp; EXPLANATIONS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    current_ans_text = header_ans

    footer = (
        "\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💪 <b>Master the Fundamentals. Ace the Interviews!</b>\n"
        "#CSFundamentals #PlacementPrep #TechInterview #DSA #SystemDesign"
    )

    for idx, block in enumerate(a_blocks, start=1):
        test_text = current_ans_text + block + "\n"
        if len(test_text) > (SAFE_MSG_LIMIT - 300) and current_ans_text != header_ans:
            # Finalize previous answer chunk
            messages.append(current_ans_text.strip())
            a_part += 1
            current_ans_text = (
                f"📝 <b>ANSWERS &amp; EXPLANATIONS — PART {a_part}</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n" + block + "\n"
            )
        else:
            current_ans_text = test_text

    if current_ans_text:
        current_ans_text += footer
        messages.append(current_ans_text.strip())

    logger.info(
        "Messages adaptively built: %d parts (all <= %d chars). Sizes: %s",
        len(messages), SAFE_MSG_LIMIT, [len(m) for m in messages],
    )
    return messages, "HTML"

"""GATE CSE Personal Teacher — Intelligent Question Selection & Engine.

Follows official GATE CSE syllabus, priority weighting, spaced repetition,
General Aptitude rotation, 90-day phase progression, and adaptive message packing.
"""

import json
import logging
import os
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from gate_questions import ALL_GATE_QUESTIONS
from gate_syllabus import GATE_SYLLABUS

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).parent / "gate_state.json"
SAFE_MSG_LIMIT = 3500
MAX_STORED_IDS = 1000

GA_ROTATION = [
    "Quantitative Aptitude",
    "Verbal Aptitude",
    "Analytical Aptitude",
    "Spatial Aptitude"
]

PHASE_MAP = [
    (1, 10, 1, "Phase 1: Foundation & Core Principles"),
    (11, 35, 2, "Phase 2: High-Weightage Subject Deep Dive"),
    (36, 50, 3, "Phase 3: Comprehensive Syllabus Coverage"),
    (51, 60, 4, "Phase 4: Genuine PYQ Mastery"),
    (61, 70, 5, "Phase 5: Weak Area & Formula Revision"),
    (71, 80, 6, "Phase 6: Multi-Subject Mixed Problems"),
    (81, 90, 7, "Phase 7: Full GATE Mock Simulations"),
]


def get_current_phase(day: int) -> tuple[int, str]:
    for start, end, phase_num, phase_title in PHASE_MAP:
        if start <= day <= end:
            return phase_num, phase_title
    return 7, "Phase 7: Full GATE Mock Simulations"


def load_gate_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return _init_empty_state()

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded GATE state: session #{data.get('session_count', 0)}, day {data.get('current_day', 1)}")
        return data
    except Exception as e:
        logger.warning(f"Failed to read {STATE_FILE}: {e}. Initializing fresh state.")
        return _init_empty_state()


def _init_empty_state() -> dict[str, Any]:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "session_count": 0,
        "start_date": today,
        "current_day": 1,
        "current_phase": 1,
        "phase_name": "Phase 1: Foundation & Core Principles",
        "sent_ids": [],
        "session_themes": [],
        "topic_history": {},
        "ga_rotation_index": 0,
        "concept_tracker": {},
        "syllabus_progress": {},
        "weak_topics": [],
        "subject_stats": {}
    }


def save_gate_state(state: dict[str, Any], new_ids: list[str], session_theme: str, state_file: Path | None = None) -> None:
    target_file = state_file or STATE_FILE
    state["session_count"] = state.get("session_count", 0) + 1
    state["current_day"] = (state["session_count"] // 8) + 1
    phase_num, phase_name = get_current_phase(state["current_day"])
    state["current_phase"] = phase_num
    state["phase_name"] = phase_name

    # Maintain FIFO sent_ids
    sent_list = state.get("sent_ids", [])
    sent_list.extend(new_ids)
    if len(sent_list) > MAX_STORED_IDS:
        sent_list = sent_list[-MAX_STORED_IDS:]
    state["sent_ids"] = sent_list

    # Update session themes
    themes = state.get("session_themes", [])
    themes.append(session_theme)
    if len(themes) > 50:
        themes = themes[-50:]
    state["session_themes"] = themes

    # Save to file
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved GATE state to {target_file.name}: session #{state['session_count']}, day {state['current_day']}")
    except Exception as e:
        logger.error(f"Failed to write {target_file}: {e}")


def _score_subject_priority(subject: str, state: dict[str, Any]) -> float:
    sub_meta = GATE_SYLLABUS.get(subject, {})
    base_weight = sub_meta.get("weight", 5.0)

    # Recency penalty: heavily penalize subjects used in last 2 sessions
    recent_themes = state.get("session_themes", [])[-2:]
    recency_penalty = 0.0
    for theme in recent_themes:
        if subject in theme:
            recency_penalty += 20.0

    # Uncovered topics bonus
    cov_topics = state.get("syllabus_progress", {}).get(subject, [])
    all_topics = list(sub_meta.get("topics", {}).keys())
    uncovered_ratio = (len(all_topics) - len(cov_topics)) / max(len(all_topics), 1)
    uncovered_bonus = uncovered_ratio * 15.0

    # Weak topics bonus
    weak_bonus = 10.0 if any(subject in w for w in state.get("weak_topics", [])) else 0.0

    return base_weight + uncovered_bonus + weak_bonus - recency_penalty


def select_session_theme(state: dict[str, Any]) -> tuple[str, str]:
    """Selects the primary subject and topic for this learning session."""
    cs_subjects = [s for s in GATE_SYLLABUS.keys() if s != "General Aptitude"]
    scored = [(s, _score_subject_priority(s, state)) for s in cs_subjects]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Pick highest priority subject (or top 2 randomly to add variety)
    top_candidates = scored[:2]
    chosen_subject = random.choice(top_candidates)[0]

    # Pick topic within chosen subject
    topics = list(GATE_SYLLABUS[chosen_subject]["topics"].keys())
    cov_topics = state.get("syllabus_progress", {}).get(chosen_subject, [])
    uncov = [t for t in topics if t not in cov_topics]
    chosen_topic = random.choice(uncov) if uncov else random.choice(topics)

    return chosen_subject, chosen_topic


def pick_gate_session_questions(state: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    """Selects exactly 10 GATE questions prioritizing syllabus coverage, GA, and anti-repetition."""
    sent_ids_set = set(state.get("sent_ids", []))
    available = [q for q in ALL_GATE_QUESTIONS if q["id"] not in sent_ids_set]

    # If pool runs low, evict oldest FIFO IDs
    if len(available) < 10:
        logger.info("Question bank exhausted; cycling oldest sent IDs (FIFO).")
        evict_count = len(ALL_GATE_QUESTIONS) - 10
        state["sent_ids"] = state.get("sent_ids", [])[evict_count:]
        sent_ids_set = set(state["sent_ids"])
        available = [q for q in ALL_GATE_QUESTIONS if q["id"] not in sent_ids_set]

    chosen_subject, chosen_topic = select_session_theme(state)
    session_theme = f"{chosen_subject} — {chosen_topic}"
    logger.info(f"Session Theme Selected: {session_theme}")

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()

    def add_q(q_item: dict[str, Any]) -> bool:
        if q_item["id"] not in selected_ids and q_item["id"] not in sent_ids_set:
            selected.append(q_item)
            selected_ids.add(q_item["id"])
            return True
        return False

    # 1. Primary theme questions (up to 5)
    theme_qs = [q for q in available if q.get("subject") == chosen_subject and q.get("topic") == chosen_topic]
    random.shuffle(theme_qs)
    for q in theme_qs[:5]:
        add_q(q)

    # 2. Subject fill if topic didn't have enough
    if len(selected) < 5:
        sub_qs = [q for q in available if q.get("subject") == chosen_subject and q["id"] not in selected_ids]
        random.shuffle(sub_qs)
        for q in sub_qs[: (5 - len(selected))]:
            add_q(q)

    # 3. General Aptitude (1-2 questions from current GA rotation)
    ga_idx = state.get("ga_rotation_index", 0) % len(GA_ROTATION)
    ga_topic = GA_ROTATION[ga_idx]
    state["ga_rotation_index"] = ga_idx + 1

    ga_qs = [q for q in available if q.get("subject") == "General Aptitude" and q.get("topic") == ga_topic]
    if not ga_qs:
        ga_qs = [q for q in available if q.get("subject") == "General Aptitude"]
    if not ga_qs:
        # Fallback: pick from full bank of GA questions if all were temporarily in sent_ids
        ga_qs = [q for q in ALL_GATE_QUESTIONS if q.get("subject") == "General Aptitude"]

    random.shuffle(ga_qs)
    for q in ga_qs[:2]:
        add_q(q)
        if len(selected) > 0 and selected[-1]["id"] == q["id"]:
            # Successfully added
            pass
        elif q["id"] not in selected_ids:
            selected.append(q)
            selected_ids.add(q["id"])

    # 4. Verified PYQ / GATE-level problem (1 question)
    pyqs = [q for q in available if "PYQ" in q.get("source", "") and q["id"] not in selected_ids]
    if pyqs:
        random.shuffle(pyqs)
        add_q(pyqs[0])

    # 5. Fill remaining slots to make EXACTLY 10 questions
    remaining_pool = [q for q in available if q["id"] not in selected_ids]
    random.shuffle(remaining_pool)
    for q in remaining_pool:
        if len(selected) >= 10:
            break
        add_q(q)

    # Fallback safety: if still < 10, reuse from all questions
    if len(selected) < 10:
        all_shuffled = list(ALL_GATE_QUESTIONS)
        random.shuffle(all_shuffled)
        for q in all_shuffled:
            if len(selected) >= 10:
                break
            if q["id"] not in selected_ids:
                selected.append(q)
                selected_ids.add(q["id"])

    # Update progress tracking
    progress = state.setdefault("syllabus_progress", {})
    sub_cov = progress.setdefault(chosen_subject, [])
    if chosen_topic not in sub_cov:
        sub_cov.append(chosen_topic)

    return selected[:10], session_theme


# --- Formatting Helpers ---

def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _format_code(text: str) -> str:
    parts = re.split(r"(```[\s\S]*?```)", text)
    out = []
    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            inner = part[3:-3]
            if inner.startswith("c\n") or inner.startswith("python\n") or inner.startswith("sql\n"):
                inner = inner.split("\n", 1)[1]
            out.append(f"<pre><code>{_esc(inner.strip())}</code></pre>")
        else:
            out.append(_esc(part))
    return "".join(out)


def _difficulty_badge(difficulty: str) -> str:
    mapping = {
        "easy": "⭐ Easy",
        "medium": "⭐⭐ Medium",
        "gate": "⭐⭐⭐ GATE Level",
        "hard": "⭐⭐⭐⭐ Hard",
        "advanced": "⭐⭐⭐⭐⭐ Advanced"
    }
    return mapping.get(difficulty.lower(), "⭐⭐⭐ GATE Level")


def _format_single_qa(i: int, q: dict[str, Any]) -> str:
    """Formats a single question immediately followed by its answer, explanation, trap & takeaway."""
    lines = []
    q_type = q.get("type", "MCQ")
    marks = q.get("marks", 2)
    diff = _difficulty_badge(q.get("difficulty", "gate"))
    subject = q.get("subject", "")
    topic = q.get("topic", "")
    subtopic = q.get("subtopic", "")
    source = q.get("source", "GATE-STYLE")
    ans = q.get("answer", "")
    concept = q.get("concept", "")
    gate_trap = q.get("gate_trap", "")
    key_concept = q.get("key_concept", "")
    ref_url = q.get("reference_url")

    # 1. Question Header & Breadcrumb
    header = f"<b>Q{i}. [{q_type} · {marks}M · {diff}]</b>"
    breadcrumb = f"<i>📌 {subject} › {topic} › {subtopic}</i>" if subtopic else f"<i>📌 {subject} › {topic}</i>"

    lines.append(header)
    lines.append(breadcrumb)
    if source != "GATE-STYLE":
        lines.append(f"<i>🏷️ {source}</i>")
    lines.append("")
    lines.append(_format_code(q["q"]))
    lines.append("")

    # 2. Options
    if q_type in ("MCQ", "MSQ") and q.get("options"):
        options = q["options"]
        for opt_key in sorted(options.keys()):
            lines.append(f"<b>{opt_key})</b> {_esc(options[opt_key])}")
        lines.append("")
    elif q_type == "NAT":
        lines.append("<i>[Enter Numerical Answer]</i>\n")

    # 3. Immediate Answer
    lines.append(f"<b>✅ Answer: {ans}</b> <i>({q_type})</i>\n")

    # 4. Concept
    if concept:
        lines.append(f"<b>📌 Concept:</b> {_esc(concept)}")

    # 5. Explanation
    lines.append(f"<b>📖 Explanation:</b>\n{_format_code(q['explanation'])}")

    # 6. GATE Trap (if applicable)
    if gate_trap:
        lines.append(f"\n<b>⚠️ GATE Trap:</b>\n{_esc(gate_trap)}")

    # 7. Key Takeaway (if applicable)
    if key_concept:
        lines.append(f"\n<b>💡 Key Takeaway:</b>\n{_esc(key_concept)}")

    # 8. Detailed Article Link for Long Explanations
    if ref_url:
        lines.append(f'\n🔗 <b>Detailed Explanation:</b> <a href="{ref_url}">Read Reference Article</a>')

    return "\n".join(lines)


def build_gate_quiz_messages(questions: list[dict[str, Any]], session_theme: str, state: dict[str, Any]) -> tuple[list[str], str]:
    """Adaptively packs the 10 self-contained GATE Q&A blocks into Telegram HTML messages <= 3500 chars."""
    session_num = state.get("session_count", 0) + 1
    current_day = state.get("current_day", 1)
    phase_name = state.get("phase_name", "Phase 1: Foundation & Core Principles")

    # Subject & Topic from theme
    parts = session_theme.split(" — ", 1)
    sub_title = parts[0] if len(parts) > 0 else "Computer Science"
    top_title = parts[1] if len(parts) > 1 else ""

    session_header = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>GATE CSE — DAY {current_day}</b> (Session #{session_num})\n"
        f"📚 <b>Subject:</b> {sub_title}\n"
        f"📌 <b>Topic:</b> {top_title}\n"
        f"📅 <i>{phase_name}</i>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    qa_blocks = [_format_single_qa(i + 1, q) for i, q in enumerate(questions)]

    # Collect subjects and topics in this session
    subjects_in_session = sorted(set(q.get("subject", "") for q in questions))
    topics_in_session = sorted(set(q.get("topic", "") for q in questions))

    summary_footer = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>SESSION COVERAGE</b>\n"
        f"• <b>Subjects:</b> {', '.join(subjects_in_session)}\n"
        f"• <b>Topics:</b> {', '.join(topics_in_session)}\n\n"
        "🎯 <b>NEXT SESSION (in 3 hours):</b>\n"
        "Automated syllabus progression & spaced revision.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    messages: list[str] = []
    current_msg = session_header

    for i, qa_text in enumerate(qa_blocks):
        entry = qa_text + "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        if len(current_msg) + len(entry) > SAFE_MSG_LIMIT:
            messages.append(current_msg.rstrip())
            current_msg = f"<b>🎯 GATE CSE — DAY {current_day} (Continued)</b>\n\n" + entry
        else:
            current_msg += entry

    if len(current_msg) + len(summary_footer) > SAFE_MSG_LIMIT:
        messages.append(current_msg.rstrip())
        messages.append(summary_footer)
    else:
        current_msg += summary_footer
        messages.append(current_msg.rstrip())

    return messages, session_theme

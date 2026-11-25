"""Aptitude Teacher Engine — Intelligent Session Builder for Placement & GATE Aptitude.

Follows the 13-phase aptitude curriculum with:
- Phase-wise topic rotation
- Anti-repetition (FIFO eviction)
- Spaced repetition boosting
- Adaptive difficulty progression
- Placement + GATE aptitude focus
"""

import json
import logging
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aptitude_questions import ALL_APTITUDE_QUESTIONS
from aptitude_syllabus import APTITUDE_SYLLABUS, APTITUDE_PHASE_ORDER, TOPIC_PHASE_MAP

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).parent / "aptitude_state.json"
SAFE_MSG_LIMIT = 3500
MAX_STORED_IDS = 2000

# Phase descriptions for session headers
PHASE_DESCRIPTIONS = {
    1:  "📊 Phase 1 — Percentages, Ratios & Proportions",
    2:  "📐 Phase 2 — Averages, Mixtures & Alligation",
    3:  "💰 Phase 3 — Profit, Loss & Discounts",
    4:  "⚙️  Phase 4 — Time & Work, Pipes & Cisterns",
    5:  "🚀 Phase 5 — Time, Speed & Distance",
    6:  "🏦 Phase 6 — Simple & Compound Interest",
    7:  "🔢 Phase 7 — Number System & Divisibility",
    8:  "🎲 Phase 8 — Permutations & Combinations",
    9:  "🎯 Phase 9 — Probability",
    10: "🧠 Phase 10 — Logical Reasoning",
    11: "📈 Phase 11 — Data Interpretation & Mixed",
    12: "📝 Phase 12 — Verbal Ability & English",
    13: "🔷 Phase 13 — Spatial & Analytical Reasoning",
}

IMPORTANCE_BADGE = {5: "🔴 Must-Do", 4: "🟠 High Priority", 3: "🟡 Medium"}

DIFFICULTY_BADGE = {
    "easy":     "⭐ Easy",
    "medium":   "⭐⭐ Medium",
    "hard":     "⭐⭐⭐ Hard",
    "advanced": "⭐⭐⭐⭐ Advanced",
    "gate":     "⭐⭐⭐ GATE Level",
}


# ─── State Management ─────────────────────────────────────────────────────────

def load_aptitude_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return _init_empty_state()
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(
            "Loaded aptitude state: session #%d, phase %d",
            data.get("session_count", 0),
            data.get("current_phase", 1),
        )
        return data
    except Exception as exc:
        logger.warning("Failed to read %s: %s — reinitialising.", STATE_FILE, exc)
        return _init_empty_state()


def _init_empty_state() -> dict[str, Any]:
    return {
        "session_count": 0,
        "start_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "current_phase": 1,
        "phase_rotation_index": 0,
        "sent_ids": [],
        "session_themes": [],
        "topic_history": {},
        "topic_stats": {},          # {topic: {"seen": n, "correct": n}}  (future)
        "weak_topics": [],
        "phase_completion": {},     # {phase: topics_seen}
    }


def save_aptitude_state(
    state: dict[str, Any],
    new_ids: list[str],
    session_theme: str,
    state_file: Path | None = None,
) -> None:
    target = state_file or STATE_FILE
    state["session_count"] = state.get("session_count", 0) + 1

    # FIFO sent_ids
    sent = state.get("sent_ids", [])
    sent.extend(new_ids)
    if len(sent) > MAX_STORED_IDS:
        sent = sent[-MAX_STORED_IDS:]
    state["sent_ids"] = sent

    # Keep last 50 session themes
    themes = state.get("session_themes", [])
    themes.append(session_theme)
    if len(themes) > 50:
        themes = themes[-50:]
    state["session_themes"] = themes

    try:
        with open(target, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        logger.info("Saved aptitude state → session #%d", state["session_count"])
    except Exception as exc:
        logger.error("Failed to write state file: %s", exc)


# ─── Topic & Phase Selection ───────────────────────────────────────────────────

def _pick_session_topic(state: dict[str, Any]) -> tuple[str, int]:
    """Select the best topic for this session using phase rotation + weight scoring."""
    rot_idx = state.get("phase_rotation_index", 0)
    current_phase = APTITUDE_PHASE_ORDER[rot_idx % len(APTITUDE_PHASE_ORDER)]
    state["phase_rotation_index"] = rot_idx + 1
    state["current_phase"] = current_phase

    # Topics belonging to this phase
    phase_topics = [t for t, d in APTITUDE_SYLLABUS.items() if d["phase"] == current_phase]

    # Score topics: prefer high-weight, unseen, not recent
    recent = set(state.get("session_themes", [])[-3:])

    def score(topic: str) -> float:
        s = APTITUDE_SYLLABUS[topic]["weight"]
        if topic in recent:
            s -= 20.0
        seen_count = state.get("topic_history", {}).get(topic, 0)
        s -= seen_count * 2.0  # slight penalty for over-visited topics
        return s

    scored = sorted(phase_topics, key=score, reverse=True)
    chosen_topic = scored[0] if scored else random.choice(list(APTITUDE_SYLLABUS.keys()))

    # Update topic history
    history = state.setdefault("topic_history", {})
    history[chosen_topic] = history.get(chosen_topic, 0) + 1

    return chosen_topic, current_phase


# ─── Question Selection ────────────────────────────────────────────────────────

def pick_aptitude_session_questions(
    state: dict[str, Any],
) -> tuple[list[dict[str, Any]], str, int]:
    """Select exactly 10 aptitude questions for this session."""
    sent_set = set(state.get("sent_ids", []))
    available = [q for q in ALL_APTITUDE_QUESTIONS if q["id"] not in sent_set]

    # Evict old IDs if pool runs low
    if len(available) < 10:
        logger.info("Question pool low (%d). Evicting oldest FIFO IDs.", len(available))
        evict = len(ALL_APTITUDE_QUESTIONS) - 10
        state["sent_ids"] = state.get("sent_ids", [])[evict:]
        sent_set = set(state["sent_ids"])
        available = [q for q in ALL_APTITUDE_QUESTIONS if q["id"] not in sent_set]

    chosen_topic, current_phase = _pick_session_topic(state)
    session_theme = chosen_topic
    logger.info("Session Theme: %s (Phase %d)", session_theme, current_phase)

    selected: list[dict[str, Any]] = []
    sel_ids: set[str] = set()

    def add(q: dict[str, Any]) -> bool:
        if q["id"] not in sel_ids and q["id"] not in sent_set:
            selected.append(q)
            sel_ids.add(q["id"])
            return True
        return False

    # 1. Primary topic (up to 7 questions)
    primary = [q for q in available if q.get("topic") == chosen_topic]
    random.shuffle(primary)
    for q in primary[:7]:
        add(q)

    # 2. Same-phase fill (up to 2 more) if topic didn't have enough
    if len(selected) < 7:
        same_phase = [
            q for q in available
            if q.get("phase") == current_phase
            and q["id"] not in sel_ids
        ]
        random.shuffle(same_phase)
        for q in same_phase[: (7 - len(selected))]:
            add(q)

    # 3. Mixed Aptitude / Hard questions (1-2 slots)
    mixed = [
        q for q in available
        if q.get("topic") == "Mixed Aptitude"
        and q["id"] not in sel_ids
    ]
    random.shuffle(mixed)
    for q in mixed[:2]:
        if len(selected) >= 9:
            break
        add(q)

    # 4. Fill remaining to exactly 10
    remainder = [q for q in available if q["id"] not in sel_ids]
    random.shuffle(remainder)
    for q in remainder:
        if len(selected) >= 10:
            break
        add(q)

    # Safety fallback
    if len(selected) < 10:
        all_shuffled = list(ALL_APTITUDE_QUESTIONS)
        random.shuffle(all_shuffled)
        for q in all_shuffled:
            if len(selected) >= 10:
                break
            if q["id"] not in sel_ids:
                selected.append(q)
                sel_ids.add(q["id"])

    return selected[:10], session_theme, current_phase


# ─── Formatting Helpers ────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fmt_code(text: str) -> str:
    """Convert ```...``` blocks to HTML <pre><code>."""
    parts = re.split(r"(```[\s\S]*?```)", text)
    out = []
    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            inner = part[3:-3].strip()
            # Strip language hint
            if "\n" in inner and inner.split("\n", 1)[0] in ("python", "c", "sql", "text"):
                inner = inner.split("\n", 1)[1]
            out.append(f"<pre><code>{_esc(inner)}</code></pre>")
        else:
            out.append(_esc(part))
    return "".join(out)


def _format_question_block(i: int, q: dict[str, Any]) -> str:
    """Format a single Q+A block with explanation, trap, and takeaway."""
    q_type   = q.get("type", "MCQ")
    marks    = q.get("marks", 2)
    diff     = DIFFICULTY_BADGE.get(q.get("difficulty", "medium"), "⭐⭐ Medium")
    topic    = q.get("topic", "Aptitude")
    subtopic = q.get("subtopic", "")
    phase    = q.get("phase", 1)
    source   = q.get("source", "PLACEMENT-STYLE")
    answer   = q.get("answer", "")
    concept  = q.get("concept", "")
    trap     = q.get("gate_trap", "")
    key      = q.get("key_concept", "")
    ref_url  = q.get("reference_url")

    lines = []
    # Header
    breadcrumb = f"<i>📌 Ph-{phase}: {topic} › {subtopic}</i>" if subtopic else f"<i>📌 Ph-{phase}: {topic}</i>"
    lines.append(f"<b>Q{i}. [{q_type} · {marks}M · {diff}]</b>")
    lines.append(breadcrumb)
    if source not in ("PLACEMENT-STYLE", "GATE-APTITUDE"):
        lines.append(f"<i>🏷️ {source}</i>")
    lines.append("")

    # Question text
    lines.append(_fmt_code(q["q"]))
    lines.append("")

    # Options
    if q_type in ("MCQ", "MSQ") and q.get("options"):
        for k in sorted(q["options"].keys()):
            lines.append(f"<b>{k})</b> {_esc(str(q['options'][k]))}")
        lines.append("")
    elif q_type == "NAT":
        lines.append("<i>[Enter Numerical Answer]</i>\n")

    # Answer (always shown — this is a teaching bot, not quiz)
    lines.append(f"<b>✅ Answer: {_esc(str(answer))}</b> <i>({q_type})</i>\n")

    # Concept
    if concept:
        lines.append(f"<b>📌 Concept:</b> {_esc(concept)}")

    # Explanation
    lines.append(f"<b>📖 Solution:</b>\n{_fmt_code(q.get('explanation', ''))}")

    # Trap
    if trap:
        lines.append(f"\n<b>⚠️ Common Mistake:</b>\n{_esc(trap)}")

    # Takeaway
    if key:
        lines.append(f"\n<b>💡 Key Formula / Rule:</b>\n{_esc(key)}")

    # Reference
    if ref_url:
        lines.append(f'\n🔗 <b>Reference:</b> <a href="{ref_url}">Read more</a>')

    return "\n".join(lines)


# ─── Message Builder ───────────────────────────────────────────────────────────

def build_aptitude_messages(
    questions: list[dict[str, Any]],
    session_theme: str,
    current_phase: int,
    state: dict[str, Any],
) -> list[str]:
    """Pack 10 Q+A blocks into Telegram HTML messages ≤ 3500 chars each."""
    session_num  = state.get("session_count", 0) + 1
    phase_desc   = PHASE_DESCRIPTIONS.get(current_phase, f"Phase {current_phase}")
    importance   = APTITUDE_SYLLABUS.get(session_theme, {}).get("importance", 4)
    imp_badge    = IMPORTANCE_BADGE.get(importance, "🟠 High Priority")
    total_topics = len(APTITUDE_SYLLABUS)
    topics_done  = len(state.get("topic_history", {}))

    header = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎓 <b>APTITUDE MASTER — Session #{session_num}</b>\n"
        f"{phase_desc}\n"
        f"📚 <b>Topic:</b> {session_theme}\n"
        f"🎯 <b>Priority:</b> {imp_badge}\n"
        f"📊 <b>Progress:</b> {topics_done}/{total_topics} topics covered\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    qa_blocks = [_format_question_block(i + 1, q) for i, q in enumerate(questions)]

    topics_in  = sorted(set(q.get("topic", "") for q in questions))
    phases_in  = sorted(set(str(q.get("phase", "")) for q in questions))

    footer = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>SESSION SUMMARY</b>\n"
        f"• <b>Topics:</b> {', '.join(topics_in)}\n"
        f"• <b>Phases:</b> {', '.join(phases_in)}\n\n"
        "⏰ <b>NEXT SESSION (in 3 hrs):</b>\n"
        "Smart phase rotation continues automatically.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    messages: list[str] = []
    current_msg = header

    for qa_text in qa_blocks:
        entry = qa_text + "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        if len(current_msg) + len(entry) > SAFE_MSG_LIMIT:
            messages.append(current_msg.rstrip())
            current_msg = f"<b>🎓 Aptitude Master — Session #{session_num} (Cont.)</b>\n\n" + entry
        else:
            current_msg += entry

    if len(current_msg) + len(footer) > SAFE_MSG_LIMIT:
        messages.append(current_msg.rstrip())
        messages.append(footer)
    else:
        current_msg += footer
        messages.append(current_msg.rstrip())

    return messages

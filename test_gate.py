"""test_gate.py — Comprehensive Test Suite & Multi-Session Simulation for GATE Bot."""

import json
import sys
from collections import Counter

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from gate_engine import (
    ALL_GATE_QUESTIONS,
    build_gate_quiz_messages,
    load_gate_state,
    pick_gate_session_questions,
    save_gate_state,
)
from gate_syllabus import GATE_SYLLABUS


def test_question_bank_integrity():
    print("=== TEST 1: Question Bank Integrity ===")
    assert len(ALL_GATE_QUESTIONS) > 0, "No questions loaded!"
    print(f"Total Questions in Bank: {len(ALL_GATE_QUESTIONS)}")

    subjects = Counter(q["subject"] for q in ALL_GATE_QUESTIONS)
    types = Counter(q["type"] for q in ALL_GATE_QUESTIONS)
    diffs = Counter(q["difficulty"] for q in ALL_GATE_QUESTIONS)

    print("\nSubjects Distribution:")
    for s, c in sorted(subjects.items()):
        print(f"  {s:40s}: {c:2d} questions")

    print("\nQuestion Types Distribution:")
    for t, c in sorted(types.items()):
        print(f"  {t:15s}: {c:2d}")

    print("\nDifficulty Distribution:")
    for d, c in sorted(diffs.items()):
        print(f"  {d:15s}: {c:2d}")

    # Verify required fields for every single question
    for q in ALL_GATE_QUESTIONS:
        assert q.get("id"), "Missing id"
        assert q.get("subject") in GATE_SYLLABUS, f"Invalid subject: {q.get('subject')}"
        assert q.get("type") in ("MCQ", "MSQ", "NAT"), f"Invalid type: {q.get('type')}"
        assert q.get("marks") in (1, 2), f"Invalid marks: {q.get('marks')}"
        assert q.get("q"), f"Empty question statement in {q['id']}"
        assert q.get("answer"), f"Empty answer in {q['id']}"
        assert q.get("explanation"), f"Empty explanation in {q['id']}"
        if q["type"] in ("MCQ", "MSQ"):
            assert q.get("options") and len(q["options"]) >= 2, f"Invalid options in {q['id']}"

    print("\n[PASS] Test 1: All questions conform strictly to GATE schema.")


def test_single_session_generation():
    print("\n=== TEST 2: Single Session Generation & Message Sizing ===")
    state = load_gate_state()
    questions, theme = pick_gate_session_questions(state)

    assert len(questions) == 10, f"Expected exactly 10 questions, got {len(questions)}"
    print(f"Session Theme: {theme}")
    print(f"Selected {len(questions)} questions:")
    for idx, q in enumerate(questions, 1):
        print(f"  {idx:2d}. [{q['type']}] [{q['marks']}M] [{q['difficulty']}] {q['subject']} › {q['topic']} ({q['id']})")

    messages, _ = build_gate_quiz_messages(questions, theme, state)
    print(f"\nGenerated {len(messages)} Telegram message parts:")
    for i, msg in enumerate(messages, 1):
        print(f"  Message Part {i}: {len(msg)} characters")
        assert len(msg) <= 3500, f"Message part {i} exceeded 3500 chars limit ({len(msg)} chars)!"
        assert len(msg) <= 4096, f"Message part {i} exceeded hard 4096 limit!"

    print("[PASS] Test 2: Single session generated 10 valid questions with safe message sizing.")


def test_multi_session_simulation():
    print("\n=== TEST 3: Multi-Session Simulation (15 Sessions) ===")
    sim_state = {
        "session_count": 0,
        "current_day": 1,
        "current_phase": 1,
        "sent_ids": [],
        "session_themes": [],
        "topic_history": {},
        "ga_rotation_index": 0,
        "concept_tracker": {},
        "syllabus_progress": {},
        "weak_topics": [],
        "subject_stats": {}
    }

    all_sent: list[str] = []
    for s_num in range(1, 16):
        qs, theme = pick_gate_session_questions(sim_state)
        assert len(qs) == 10, f"Session {s_num} did not generate 10 questions!"
        new_ids = [q["id"] for q in qs]
        all_sent.extend(new_ids)

        # Check GA inclusion
        ga_count = sum(1 for q in qs if q["subject"] == "General Aptitude")
        assert ga_count >= 1, f"Session {s_num} missing General Aptitude!"

        save_gate_state(sim_state, new_ids, theme)
        print(f"  Session {s_num:2d} (Day {sim_state['current_day']}, Phase {sim_state['current_phase']}): Theme '{theme}' | {len(qs)} Qs | GA: {ga_count}")

    print(f"\nTotal questions served across 15 sessions: {len(all_sent)}")
    print(f"Syllabus coverage achieved:\n{json.dumps(sim_state['syllabus_progress'], indent=2)}")
    print("[PASS] Test 3: Multi-session simulation completed successfully.")


if __name__ == "__main__":
    test_question_bank_integrity()
    test_single_session_generation()
    test_multi_session_simulation()

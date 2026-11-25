"""test_aptitude.py — Comprehensive unit and integrity test suite for Aptitude Master Bot.

Tests:
1. Question schema integrity (all required fields present)
2. Question answer & explanation validation
3. No duplicate question IDs
4. Phase & topic validity against syllabus
5. Session selection engine (exactly 10 questions chosen)
6. Anti-repetition FIFO logic
7. Telegram message length budget (each chunk <= 3500 chars)
8. Telegram HTML escaping & formatting
"""

import json
import unittest
from pathlib import Path

from aptitude_questions import ALL_APTITUDE_QUESTIONS
from aptitude_syllabus import APTITUDE_SYLLABUS, APTITUDE_PHASE_ORDER
from aptitude_engine import (
    load_aptitude_state,
    pick_aptitude_session_questions,
    build_aptitude_messages,
    save_aptitude_state,
    SAFE_MSG_LIMIT,
)


class TestAptitudeQuestionBank(unittest.TestCase):
    def test_total_questions_loaded(self):
        """Ensure question bank is loaded with substantial questions."""
        self.assertGreaterEqual(
            len(ALL_APTITUDE_QUESTIONS),
            50,
            f"Expected at least 50 questions, loaded {len(ALL_APTITUDE_QUESTIONS)}",
        )

    def test_no_duplicate_ids(self):
        """Ensure every question has a unique ID across the entire bank."""
        ids = [q["id"] for q in ALL_APTITUDE_QUESTIONS]
        self.assertEqual(len(ids), len(set(ids)), "Found duplicate question IDs!")

    def test_question_schema_compliance(self):
        """Verify each question has all required fields with proper types."""
        required_fields = {
            "id": str,
            "phase": int,
            "subject": str,
            "topic": str,
            "type": str,
            "q": str,
            "answer": str,
            "explanation": str,
            "gate_trap": str,
            "key_concept": str,
        }
        for q in ALL_APTITUDE_QUESTIONS:
            qid = q.get("id", "UNKNOWN")
            for field, expected_type in required_fields.items():
                self.assertIn(field, q, f"Question {qid} missing field: '{field}'")
                self.assertIsInstance(
                    q[field],
                    expected_type,
                    f"Question {qid} field '{field}' must be {expected_type.__name__}",
                )

            # Check question types
            self.assertIn(
                q["type"],
                ("MCQ", "NAT", "MSQ"),
                f"Question {qid} has invalid type: {q['type']}",
            )

            # For MCQs, ensure options dictionary exists with 4 choices
            if q["type"] == "MCQ":
                self.assertIsInstance(
                    q.get("options"),
                    dict,
                    f"Question {qid} (MCQ) must have an options dict",
                )
                self.assertIn(
                    q["answer"],
                    q["options"],
                    f"Question {qid} answer '{q['answer']}' not in options keys {list(q['options'].keys())}",
                )

            # Verify explanation is substantial (not empty or trivial)
            self.assertGreater(
                len(q["explanation"].strip()),
                20,
                f"Question {qid} has an explanation that is too short",
            )

    def test_syllabus_topic_alignment(self):
        """Verify that every question maps to a valid phase (1-13) and recognized topic."""
        valid_topics = set(APTITUDE_SYLLABUS.keys())
        for q in ALL_APTITUDE_QUESTIONS:
            qid = q.get("id", "UNKNOWN")
            self.assertIn(
                q["phase"],
                range(1, 14),
                f"Question {qid} has invalid phase: {q.get('phase')}",
            )
            self.assertIn(
                q["topic"],
                valid_topics,
                f"Question {qid} topic '{q.get('topic')}' not in APTITUDE_SYLLABUS",
            )


class TestAptitudeEngine(unittest.TestCase):
    def setUp(self):
        self.test_state = {
            "session_count": 0,
            "start_date": "2026-11-25",
            "current_phase": 1,
            "phase_rotation_index": 0,
            "sent_ids": [],
            "session_themes": [],
            "topic_history": {},
            "topic_stats": {},
            "weak_topics": [],
            "phase_completion": {},
        }

    def test_pick_session_questions_count(self):
        """Verify pick_aptitude_session_questions returns exactly 10 questions."""
        questions, theme, phase = pick_aptitude_session_questions(self.test_state)
        self.assertEqual(len(questions), 10, f"Expected 10 questions, got {len(questions)}")
        self.assertIn(phase, APTITUDE_PHASE_ORDER)
        self.assertTrue(theme)

    def test_anti_repetition_fifo(self):
        """Verify previously sent questions are not repeated in immediate subsequent sessions."""
        q1, theme1, phase1 = pick_aptitude_session_questions(self.test_state)
        ids1 = [q["id"] for q in q1]
        self.test_state["sent_ids"].extend(ids1)

        q2, theme2, phase2 = pick_aptitude_session_questions(self.test_state)
        ids2 = [q["id"] for q in q2]

        overlap = set(ids1).intersection(set(ids2))
        self.assertEqual(
            len(overlap),
            0,
            f"Questions repeated across consecutive sessions: {overlap}",
        )

    def test_message_formatting_and_length_limit(self):
        """Ensure all generated Telegram messages strictly respect the 3500 char safety limit."""
        questions, theme, phase = pick_aptitude_session_questions(self.test_state)
        messages = build_aptitude_messages(questions, theme, phase, self.test_state)

        self.assertGreater(len(messages), 0, "No messages generated")
        for i, msg in enumerate(messages, 1):
            self.assertLessEqual(
                len(msg),
                SAFE_MSG_LIMIT,
                f"Message chunk {i} length ({len(msg)}) exceeds safe limit {SAFE_MSG_LIMIT}",
            )
            # Ensure proper Telegram HTML formatting
            self.assertIn("<b>", msg)
            self.assertIn("</b>", msg)
            self.assertNotIn("```", msg, "Markdown backticks leaked into HTML message")

    def test_state_saving(self):
        """Ensure saving state increments session count and updates sent_ids."""
        tmp_state_file = Path("test_aptitude_state_tmp.json")
        try:
            questions, theme, phase = pick_aptitude_session_questions(self.test_state)
            ids = [q["id"] for q in questions]
            save_aptitude_state(self.test_state, ids, theme, state_file=tmp_state_file)

            self.assertTrue(tmp_state_file.exists())
            with open(tmp_state_file, "r", encoding="utf-8") as f:
                saved = json.load(f)

            self.assertEqual(saved["session_count"], 1)
            self.assertEqual(saved["sent_ids"], ids)
            self.assertEqual(saved["session_themes"], [theme])
        finally:
            if tmp_state_file.exists():
                tmp_state_file.unlink()


if __name__ == "__main__":
    unittest.main()

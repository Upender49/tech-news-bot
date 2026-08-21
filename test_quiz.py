"""
test_quiz.py — Local smoke test for the CS Quiz Bot.
Run: python3.12.exe test_quiz.py
Does NOT send to Telegram. Verifies the full question selection and formatting pipeline.
"""

import sys
import os
import logging

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "DUMMY_TOKEN")
os.environ.setdefault("TELEGRAM_CHAT_ID", "DUMMY_CHAT")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

from quiz_generator import load_quiz_state, pick_questions, build_quiz_message
from question_bank import QUESTIONS

print("\n" + "=" * 60)
print("  CS Quiz Bot - Local Smoke Test")
print("=" * 60 + "\n")

print(f"[INFO] Total questions in bank: {len(QUESTIONS)}")

print("\n[Step 1] Loading quiz state...")
state = load_quiz_state()
print(f"   -> Sent IDs so far: {len(state.get('sent_ids', []))}")
print(f"   -> Topic index: {state.get('topic_index', 0)}")

print("\n[Step 2] Picking 5 questions...")
questions, updated_state = pick_questions(state)
print(f"   -> {len(questions)} questions selected:")
for i, q in enumerate(questions, 1):
    print(f"      Q{i}: [{q['difficulty']:10s}] [{q['topic']}] {q['id']}")

print("\n[Step 3] Building Telegram message...")
message, parse_mode = build_quiz_message(questions)
print(f"   -> Parse mode  : {parse_mode}")
print(f"   -> Message size: {len(message)} chars")

print("\n" + "=" * 60)
print("  MESSAGE PREVIEW (first 3000 chars):")
print("=" * 60)
print(message[:3000])
if len(message) > 3000:
    print(f"\n... ({len(message) - 3000} more chars)")

print("\n[OK] Smoke test complete!")

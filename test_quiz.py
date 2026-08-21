"""
test_quiz.py — Local smoke test for the CS Quiz Bot.
Run: python3.12.exe test_quiz.py
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

from quiz_generator import load_quiz_state, pick_questions, build_quiz_messages
from question_bank import QUESTIONS

LIMIT = 4096

print("\n" + "=" * 62)
print("  CS Quiz Bot - Local Smoke Test")
print("=" * 62 + "\n")

print(f"[INFO] Total questions in bank: {len(QUESTIONS)}")

print("\n[Step 1] Loading quiz state...")
state = load_quiz_state()
print(f"   -> Sent IDs: {len(state.get('sent_ids', []))}, Topic index: {state.get('topic_index', 0)}")

print("\n[Step 2] Picking questions...")
questions, updated_state = pick_questions(state)
print(f"   -> {len(questions)} questions selected:")
for i, q in enumerate(questions, 1):
    print(f"      Q{i:2d}: [{q['difficulty']:10s}] [{q['topic']:<30s}] {q['id']}")

print("\n[Step 3] Building messages...")
messages, parse_mode = build_quiz_messages(questions)

labels = ["Questions (Part 1)", "Answers  (Part 2)", "Answers  (Part 3)"]
all_ok = True
for i, (msg, label) in enumerate(zip(messages, labels), 1):
    ok = len(msg) <= LIMIT
    status = "✅ OK" if ok else "❌ TOO LONG!"
    print(f"   -> Msg {i} {label}: {len(msg):4d} chars  {status}")
    if not ok:
        all_ok = False

print(f"\n   -> All messages under 4096: {'✅ YES — will work!' if all_ok else '❌ NO — WILL FAIL!'}")

print("\n" + "=" * 62)
for i, (msg, label) in enumerate(zip(messages, labels), 1):
    print(f"\n  MSG {i} PREVIEW — {label} (first 800 chars):")
    print("=" * 62)
    print(msg[:800])
    if len(msg) > 800:
        print(f"\n  ... ({len(msg) - 800} more chars)")

print(f"\n\n{'[OK]' if all_ok else '[FAIL]'} Smoke test complete!")
if not all_ok:
    sys.exit(1)

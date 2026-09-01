"""
test_quiz.py — Local smoke test & multi-run simulation for the CS Quiz Bot.
Run: python3.12.exe test_quiz.py
Verifies deduplication across multiple cycles and guarantees all messages stay strictly <= 4096 characters.
"""

import sys
import os
import logging
import copy

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "DUMMY_TOKEN")
os.environ.setdefault("TELEGRAM_CHAT_ID", "DUMMY_CHAT")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

from question_bank import QUESTIONS
from quiz_generator import load_quiz_state, pick_questions, build_quiz_messages, save_quiz_state

LIMIT = 4096

print("\n" + "=" * 65)
print("  CS Quiz Bot — Verification & Deduplication Test")
print("=" * 65 + "\n")

print(f"[INFO] Total questions in bank: {len(QUESTIONS)}")

# ── Single Run Test ───────────────────────────────────────────────────────────
print("\n[Step 1] Loading initial state and picking 10 questions...")
state = load_quiz_state()
questions, updated_state = pick_questions(state)
print(f"   -> {len(questions)} questions selected:")
for i, q in enumerate(questions, 1):
    print(f"      Q{i:2d}: [{q['difficulty']:10s}] [{q['topic']:<28s}] {q['id']}")

print("\n[Step 2] Building Telegram messages...")
messages, parse_mode = build_quiz_messages(questions)
print(f"   -> Generated {len(messages)} message parts.")

all_sizes_ok = True
for idx, m in enumerate(messages, start=1):
    sz = len(m)
    status = "✅ OK" if sz <= LIMIT else f"❌ EXCEEDS LIMIT BY {sz - LIMIT} CHARS!"
    print(f"      Part {idx}: {sz:4d} chars  {status}")
    if sz > LIMIT:
        all_sizes_ok = False

if not all_sizes_ok:
    print("\n❌ Single run size validation failed!")
    sys.exit(1)

# ── Multi-Run Simulation ──────────────────────────────────────────────────────
print("\n[Step 3] Running 14-run consecutive simulation (140 questions)...")
sim_state = {"sent_ids": [], "topic_index": 0}
all_picked_ids = []
consecutive_ok = True

for run_i in range(1, 15):
    q_batch, sim_state = pick_questions(sim_state)
    batch_ids = [q["id"] for q in q_batch]
    
    msgs, _ = build_quiz_messages(q_batch)
    for part_idx, msg in enumerate(msgs, start=1):
        if len(msg) > LIMIT:
            print(f"   ❌ Run {run_i} Part {part_idx} length {len(msg)} > {LIMIT}")
            consecutive_ok = False
            
    # Check if there are internal duplicates within the same batch
    if len(batch_ids) != len(set(batch_ids)):
        print(f"   ❌ Run {run_i} contained internal duplicate IDs!")
        consecutive_ok = False

    # Save to state
    existing = [i for i in sim_state.get("sent_ids", []) if i not in batch_ids]
    sim_state["sent_ids"] = existing + batch_ids
    all_picked_ids.extend(batch_ids)

# Check total unique in first (len(QUESTIONS) // 10) runs
runs_before_full_cycle = len(QUESTIONS) // 10
first_cycle_ids = all_picked_ids[:runs_before_full_cycle * 10]
unique_in_first_cycle = len(set(first_cycle_ids))

print(f"\n   -> Questions in bank: {len(QUESTIONS)}")
print(f"   -> Questions picked in first {runs_before_full_cycle} runs: {len(first_cycle_ids)}")
print(f"   -> Unique IDs in first cycle: {unique_in_first_cycle}")

if unique_in_first_cycle == len(first_cycle_ids) and consecutive_ok:
    print("\n✅ Multi-run simulation SUCCESSFUL! Zero duplicates before full bank exhaustion.")
else:
    print("\n❌ Deduplication test failed!")
    sys.exit(1)

print("\n" + "=" * 65)
print("  PREVIEW OF PART 1 (Questions 1–5):")
print("=" * 65)
print(messages[0][:600] + "...\n")

print("=" * 65)
print("  PREVIEW OF PART 3 (Answers 1–5):")
print("=" * 65)
print(messages[2][:600] + "...\n")

print("🎉 ALL TESTS PASSED! System is ready.")

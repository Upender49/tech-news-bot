"""
main.py — Orchestrator / entry-point.
NEW pipeline: generate quiz → format → send → save state.

Preserved from old pipeline:
  - config (Telegram token, chat ID, env vars)
  - sender (Telegram API, retry logic, chunking)
  - setup_logging
  - validate_config
  - sys.exit codes for GitHub Actions

Replaced:
  - fetcher / filter / formatter → quiz_generator
  - state (URL/title tracking) → quiz_generator (ID-based tracking)
"""

import logging
import sys

import config
from quiz_generator import (
    load_quiz_state,
    pick_questions,
    build_quiz_message,
    save_quiz_state,
)
from sender import send_long_message


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run() -> None:
    """Main pipeline: load state → pick questions → format → send → save state."""
    logger = logging.getLogger("main")
    logger.info("═══════════ CS Quiz Bot starting ═══════════")

    # 1. Validate Telegram configuration (unchanged)
    if not config.validate_config():
        logger.critical("Aborting — fix environment variables first.")
        sys.exit(1)

    # 2. Load quiz state (sent question IDs + topic rotation index)
    state = load_quiz_state()

    # 3. Pick 5 questions with topic rotation & difficulty mix
    questions, updated_state = pick_questions(state)

    if not questions:
        logger.error("No questions could be selected. Check question_bank.py.")
        sys.exit(1)

    # 4. Build formatted Telegram message (HTML mode)
    message, parse_mode = build_quiz_message(questions)

    # 5. Send to Telegram (same sender, same config — unchanged)
    success = send_long_message(message, parse_mode=parse_mode)

    if success:
        # 6. Persist state so next run uses fresh questions
        new_ids = [q["id"] for q in questions]
        save_quiz_state(updated_state, new_ids)
        logger.info("Quiz sent successfully. ✅ IDs: %s", new_ids)
    else:
        logger.error("Failed to send quiz. ❌")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    run()

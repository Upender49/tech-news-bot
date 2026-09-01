"""
main.py — Orchestrator / entry-point.
Pipeline: generate quiz → send 3 messages → save state.

Messages sent per run:
  1. Questions 1-10
  2. Answers Q1-5
  3. Answers Q6-10 + footer

Preserved: config, sender, setup_logging, validate_config.
"""

import logging
import sys

import config
from quiz_generator import (
    load_quiz_state,
    pick_questions,
    build_quiz_messages,
    save_quiz_state,
)
from sender import send_message


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run() -> None:
    """Main pipeline: load state → pick 10 questions → send 3 messages → save state."""
    logger = logging.getLogger("main")
    logger.info("═══════════ CS Quiz Bot starting ═══════════")

    # 1. Validate Telegram config
    if not config.validate_config():
        logger.critical("Aborting — fix environment variables first.")
        sys.exit(1)

    # 2. Load quiz state
    state = load_quiz_state()

    # 3. Pick questions
    questions, updated_state = pick_questions(state)
    if not questions:
        logger.error("No questions selected.")
        sys.exit(1)

    # 4. Build messages (returns list: [questions, answers_pt1, answers_pt2])
    messages, parse_mode = build_quiz_messages(questions)

    # 5. Send all messages sequentially
    for i, msg in enumerate(messages, start=1):
        logger.info(
            "Sending message %d/%d (%d chars)...",
            i, len(messages), len(msg),
        )
        if len(msg) > 4096:
            logger.error(
                "Message %d is %d chars — exceeds 4096! Aborting.",
                i, len(msg),
            )
            sys.exit(1)

        ok = send_message(msg, parse_mode=parse_mode)
        if not ok:
            logger.error("Failed to send message %d/%d. ❌", i, len(messages))
            sys.exit(1)
        logger.info("Message %d/%d sent. ✅", i, len(messages))

    # 6. Save state (only after all messages succeed)
    new_ids = [q["id"] for q in questions]
    save_quiz_state(updated_state, new_ids)
    logger.info("Pipeline completed. %d question IDs saved. ✅", len(new_ids))


if __name__ == "__main__":
    setup_logging()
    run()

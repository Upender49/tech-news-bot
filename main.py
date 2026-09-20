"""main.py — Main orchestrator for GATE CSE Personal Teacher Bot.

Pipeline:
1. Validate Telegram credentials
2. Load persistent state from gate_state.json
3. Select 10 GATE questions based on syllabus priority & GA rotation
4. Adaptively pack questions and answers into Telegram HTML messages (<= 3500 chars)
5. Sequentially send messages to Telegram with retry protection
6. Save updated learning progress and state
"""

import logging
import sys

import config
from gate_engine import (
    build_gate_quiz_messages,
    load_gate_state,
    pick_gate_session_questions,
    save_gate_state,
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
    """Execute one scheduled learning session."""
    logger = logging.getLogger("main")
    logger.info("═══════════ GATE CSE Personal Teacher Starting ═══════════")

    # 1. Validate credentials
    if not config.validate_config():
        logger.critical("Aborting — Please configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        sys.exit(1)

    # 2. Load learning state
    state = load_gate_state()

    # 3. Select 10 questions using priority engine
    questions, session_theme = pick_gate_session_questions(state)
    if not questions or len(questions) != config.QUESTIONS_PER_SESSION:
        logger.error(f"Expected {config.QUESTIONS_PER_SESSION} questions, got {len(questions) if questions else 0}.")
        sys.exit(1)

    logger.info(f"Selected {len(questions)} questions for session theme: {session_theme}")

    # 4. Build Telegram HTML messages
    messages, _ = build_gate_quiz_messages(questions, session_theme, state)

    # 5. Sequentially send messages
    for i, msg in enumerate(messages, start=1):
        msg_len = len(msg)
        logger.info(f"Sending message {i}/{len(messages)} ({msg_len} chars)...")

        if msg_len > 4096:
            logger.critical(f"Message {i} exceeds Telegram 4096-char limit ({msg_len} chars)! Aborting.")
            sys.exit(1)

        ok = send_message(msg, parse_mode="HTML")
        if not ok:
            logger.critical(f"Failed to deliver message {i}/{len(messages)} to Telegram. ❌")
            sys.exit(1)

        logger.info(f"Message {i}/{len(messages)} delivered successfully. ✅")

    # 6. Save updated state (only after all messages succeed)
    new_ids = [q["id"] for q in questions]
    save_gate_state(state, new_ids, session_theme)
    logger.info(f"Session complete. State saved for {len(new_ids)} question IDs. ✅")
    logger.info("════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    setup_logging()
    run()

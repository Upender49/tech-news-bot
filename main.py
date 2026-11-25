"""main.py — Aptitude Master Bot: Main Orchestrator.

Pipeline:
1. Validate Telegram credentials
2. Load persistent aptitude learning state
3. Select 10 aptitude questions (phase-rotation + spaced repetition)
4. Build Telegram HTML messages (≤ 3500 chars each)
5. Send messages sequentially with retry protection
6. Save updated state for next session
"""

import logging
import sys

import config
from aptitude_engine import (
    build_aptitude_messages,
    load_aptitude_state,
    pick_aptitude_session_questions,
    save_aptitude_state,
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
    """Execute one scheduled aptitude learning session."""
    logger = logging.getLogger("main")
    logger.info("═══════════ Aptitude Master Bot Starting ═══════════")

    # 1. Validate credentials
    if not config.validate_config():
        logger.critical("Aborting — Configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        sys.exit(1)

    # 2. Load state
    state = load_aptitude_state()

    # 3. Select 10 questions
    questions, session_theme, current_phase = pick_aptitude_session_questions(state)
    if len(questions) != config.QUESTIONS_PER_SESSION:
        logger.error(
            "Expected %d questions, got %d.", config.QUESTIONS_PER_SESSION, len(questions)
        )
        sys.exit(1)

    logger.info("Session theme: %s (Phase %d)", session_theme, current_phase)

    # 4. Build messages
    messages = build_aptitude_messages(questions, session_theme, current_phase, state)

    # 5. Send messages
    for i, msg in enumerate(messages, start=1):
        msg_len = len(msg)
        logger.info("Sending message %d/%d (%d chars)...", i, len(messages), msg_len)

        if msg_len > 4096:
            logger.critical("Message %d exceeds 4096-char limit (%d). Aborting.", i, msg_len)
            sys.exit(1)

        ok = send_message(msg, parse_mode="HTML")
        if not ok:
            logger.critical("Failed to deliver message %d/%d. ❌", i, len(messages))
            sys.exit(1)

        logger.info("Message %d/%d delivered. ✅", i, len(messages))

    # 6. Save state
    new_ids = [q["id"] for q in questions]
    save_aptitude_state(state, new_ids, session_theme)
    logger.info(
        "Session complete. %d IDs saved. Theme: %s ✅", len(new_ids), session_theme
    )
    logger.info("════════════════════════════════════════════════════════")


if __name__ == "__main__":
    setup_logging()
    run()

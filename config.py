"""config.py — Central configuration loader for GATE CSE Personal Teacher Bot."""

import logging
import os

# ── Telegram Credentials ──────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── GATE Engine Configuration ─────────────────────────────────────────────────
QUESTIONS_PER_SESSION: int = int(os.environ.get("QUESTIONS_PER_SESSION", "10"))
QUIZ_INTERVAL_HOURS: int = int(os.environ.get("QUIZ_INTERVAL_HOURS", "3"))
STUDY_PLAN_DAYS: int = int(os.environ.get("STUDY_PLAN_DAYS", "90"))
GATE_BRANCH: str = os.environ.get("GATE_BRANCH", "CS")
PYQ_ENABLED: bool = os.environ.get("PYQ_ENABLED", "true").lower() == "true"
GA_ENABLED: bool = os.environ.get("GA_ENABLED", "true").lower() == "true"
SPACED_REPETITION: bool = os.environ.get("SPACED_REPETITION", "true").lower() == "true"

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()


def validate_config() -> bool:
    """Return True only if all mandatory Telegram credentials are present."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if missing:
        logging.critical("Missing required environment variables: %s", ", ".join(missing))
        return False
    return True

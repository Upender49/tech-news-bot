"""config.py — Central configuration for Aptitude Master Bot."""

import logging
import os

# ── Telegram Credentials ──────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID:   str = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── Session Configuration ─────────────────────────────────────────────────────
QUESTIONS_PER_SESSION: int = int(os.environ.get("QUESTIONS_PER_SESSION", "10"))
QUIZ_INTERVAL_HOURS:   int = int(os.environ.get("QUIZ_INTERVAL_HOURS", "3"))

# ── Bot Behaviour ─────────────────────────────────────────────────────────────
# Set to "aptitude" (default) or "gate" to switch context
BOT_MODE: str = os.environ.get("BOT_MODE", "aptitude").lower()

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
        logging.critical("Missing required env vars: %s", ", ".join(missing))
        return False
    return True

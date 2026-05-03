"""
sender.py — Telegram Bot API integration module.
Sends a formatted message to the configured group/channel.
"""

import logging
import urllib.parse
import urllib.request
import urllib.error
import json
import time

import config

logger = logging.getLogger(__name__)

_TELEGRAM_API_BASE = "https://api.telegram.org/bot"
_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


def _build_api_url(method: str) -> str:
    return f"{_TELEGRAM_API_BASE}{config.TELEGRAM_BOT_TOKEN}/{method}"


def send_message(text: str, parse_mode: str = "Markdown") -> bool:
    """
    Send *text* to the configured Telegram chat.
    Returns True on success, False on failure.
    Uses urllib (stdlib only) — no external HTTP library required.
    """
    url = _build_api_url("sendMessage")
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                if body.get("ok"):
                    logger.info("Message sent successfully (attempt %d).", attempt)
                    return True
                else:
                    logger.error(
                        "Telegram API returned ok=false: %s", body.get("description")
                    )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            logger.error(
                "HTTP %d on attempt %d: %s", exc.code, attempt, body[:200]
            )
            # 400 Bad Request — likely a config issue, no point retrying
            if exc.code == 400:
                return False
        except (urllib.error.URLError, TimeoutError) as exc:
            logger.error("Network error on attempt %d: %s", attempt, exc)

        if attempt < _MAX_RETRIES:
            logger.info("Retrying in %d seconds…", _RETRY_DELAY)
            time.sleep(_RETRY_DELAY)

    logger.critical("Failed to send message after %d attempts.", _MAX_RETRIES)
    return False


def send_long_message(text: str, parse_mode: str = "Markdown") -> bool:
    """
    Splits text at safe boundaries if it exceeds Telegram's 4096-char limit
    and sends each chunk separately. Returns True only if all chunks succeed.
    """
    limit = 4096
    if len(text) <= limit:
        return send_message(text, parse_mode)

    # Split on double-newline (article boundaries)
    chunks: list[str] = []
    current = ""
    for part in text.split("\n\n"):
        candidate = current + ("\n\n" if current else "") + part
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = part
    if current:
        chunks.append(current)

    logger.info("Splitting message into %d chunks.", len(chunks))
    return all(send_message(chunk, parse_mode) for chunk in chunks)

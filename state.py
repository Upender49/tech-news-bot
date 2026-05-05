"""
state.py — Persistent state management across GitHub Actions runs.
Tracks URLs of articles already sent to avoid re-sending duplicates.
State is stored in sent_urls.json (committed back to the repo after each run).
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).parent / "sent_urls.json"

# Prevent the file from growing unbounded — keep the most recent N URLs
MAX_STORED_URLS = 500


def load_sent_urls() -> set[str]:
    """
    Read the persisted state file and return a set of already-sent URLs.
    Returns an empty set if the file doesn't exist or is unreadable.
    """
    if not STATE_FILE.exists():
        logger.info("State file not found — this appears to be the first run.")
        return set()

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        urls = set(data.get("sent_urls", []))
        logger.info("Loaded %d previously sent URLs from state file.", len(urls))
        return urls
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read state file (%s) — starting fresh.", exc)
        return set()


def save_sent_urls(existing: set[str], new_urls: list[str]) -> None:
    """
    Merge new_urls into the existing set and write to disk.
    Trims the list to MAX_STORED_URLS (keeps the most recent entries).
    """
    # Build ordered list: old first, new appended at tail
    combined = [u for u in existing if u not in new_urls] + new_urls

    # Keep only the most recent MAX_STORED_URLS
    trimmed = combined[-MAX_STORED_URLS:]

    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"sent_urls": trimmed}, f, indent=2, ensure_ascii=False)
        logger.info(
            "State saved: %d URLs tracked (%d new this run).",
            len(trimmed),
            len(new_urls),
        )
    except OSError as exc:
        logger.error("Could not write state file: %s", exc)

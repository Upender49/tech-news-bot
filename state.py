"""
state.py — Persistent state management across GitHub Actions runs.

Tracks BOTH URLs and normalised titles of already-sent articles.
This dual-key approach handles Google News, which generates a new
redirect URL for the same article on every fetch — so URL-only
deduplication was causing the same articles to be re-sent.

State is stored in sent_urls.json and committed back to the repo
after each successful run.
"""

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).parent / "sent_urls.json"

# Keep most recent N entries to prevent unbounded growth
MAX_STORED = 500


# ── Title normalisation ────────────────────────────────────────────────────────

def _normalise_title(title: str) -> str:
    """
    Reduce a title to a canonical form for fuzzy deduplication.
    Strips source attribution (e.g. "- TechCrunch"), lowercases,
    removes punctuation, and collapses whitespace.
    """
    # Remove trailing "- Source" or "| Source" patterns
    title = re.sub(r"\s*[-–—|]\s*[\w][\w\s,\.]+$", "", title)
    # Lowercase
    title = title.lower()
    # Keep only letters, digits, spaces
    title = re.sub(r"[^a-z0-9\s]", " ", title)
    # Collapse whitespace
    return " ".join(title.split())


# ── Public API ─────────────────────────────────────────────────────────────────

def load_state() -> tuple[set[str], set[str]]:
    """
    Load the persisted state file.
    Returns (seen_urls: set, seen_titles: set).
    """
    if not STATE_FILE.exists():
        logger.info("State file not found — first run.")
        return set(), set()

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        seen_urls   = set(data.get("sent_urls",   []))
        seen_titles = set(data.get("sent_titles", []))
        logger.info(
            "State loaded: %d URLs, %d titles tracked.",
            len(seen_urls), len(seen_titles),
        )
        return seen_urls, seen_titles
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read state (%s) — starting fresh.", exc)
        return set(), set()


def save_state(
    existing_urls:   set[str],
    existing_titles: set[str],
    new_articles,           # list[Article]  (avoid circular import)
) -> None:
    """
    Merge new article URLs and normalised titles into existing sets,
    trim to MAX_STORED, and persist to disk.
    """
    new_urls   = [a.link                   for a in new_articles]
    new_titles = [_normalise_title(a.title) for a in new_articles]

    combined_urls   = [u for u in existing_urls   if u not in new_urls]   + new_urls
    combined_titles = [t for t in existing_titles if t not in new_titles] + new_titles

    trimmed_urls   = combined_urls[-MAX_STORED:]
    trimmed_titles = combined_titles[-MAX_STORED:]

    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"sent_urls": trimmed_urls, "sent_titles": trimmed_titles},
                f, indent=2, ensure_ascii=False,
            )
        logger.info(
            "State saved: %d URLs, %d titles (%d new this run).",
            len(trimmed_urls), len(trimmed_titles), len(new_urls),
        )
    except OSError as exc:
        logger.error("Could not write state file: %s", exc)


# ── Legacy shim (keeps main.py backward-compatible if needed) ─────────────────
def load_sent_urls() -> set[str]:
    urls, _ = load_state()
    return urls

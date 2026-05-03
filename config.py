"""
config.py — Central configuration loader.
Reads environment variables (set locally or via GitHub Secrets).
"""

import os
import logging

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str   = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── Fetch settings ────────────────────────────────────────────────────────────
MAX_ARTICLES_PER_FEED: int = int(os.environ.get("MAX_ARTICLES_PER_FEED", "5"))
MAX_TOTAL_ARTICLES: int    = int(os.environ.get("MAX_TOTAL_ARTICLES", "12"))

# ── Keyword filter (comma-separated in env, or use defaults) ──────────────────
_raw_keywords = os.environ.get(
    "FILTER_KEYWORDS",
    "AI,ML,machine learning,deep learning,LLM,GPT,coding,DSA,data structure,"
    "algorithm,software,developer,hiring,placement,interview,internship,"
    "programming,Python,Java,JavaScript,cloud,open source,GitHub,tech",
)
FILTER_KEYWORDS: list[str] = [kw.strip().lower() for kw in _raw_keywords.split(",") if kw.strip()]

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()

# ── RSS feed list ─────────────────────────────────────────────────────────────
RSS_FEEDS: list[dict] = [
    # Google News — topic-based
    {
        "name": "Google News – AI",
        "url": "https://news.google.com/rss/search?q=artificial+intelligence+machine+learning&hl=en-IN&gl=IN&ceid=IN:en",
    },
    {
        "name": "Google News – Coding",
        "url": "https://news.google.com/rss/search?q=programming+software+developer&hl=en-IN&gl=IN&ceid=IN:en",
    },
    {
        "name": "Google News – DSA",
        "url": "https://news.google.com/rss/search?q=data+structures+algorithms+competitive+programming&hl=en-IN&gl=IN&ceid=IN:en",
    },
    {
        "name": "Google News – Placements",
        "url": "https://news.google.com/rss/search?q=tech+hiring+placement+internship+software+engineer+2025&hl=en-IN&gl=IN&ceid=IN:en",
    },
    # Hacker News top stories
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
    },
    # Dev.to
    {
        "name": "Dev.to",
        "url": "https://dev.to/feed",
    },
    # TechCrunch
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
    },
    # The Verge – Tech
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
    },
]


def validate_config() -> bool:
    """Return True only if all mandatory config values are present."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if missing:
        logging.critical("Missing required environment variables: %s", ", ".join(missing))
        return False
    return True

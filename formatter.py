"""
formatter.py — Message formatting module.
Converts filtered articles into a Telegram-safe message string.
"""

import logging
from datetime import datetime, timezone

from fetcher import Article

logger = logging.getLogger(__name__)

# Telegram message hard limit is 4096 chars; we stay safely below it
_MAX_MSG_LEN = 4000

# Category emoji mapping for known sources / keywords
_SOURCE_EMOJI: dict[str, str] = {
    "hacker news": "🟠",
    "dev.to": "👩‍💻",
    "techcrunch": "🚀",
    "the verge": "📰",
    "google news – ai": "🤖",
    "google news – coding": "💻",
    "google news – dsa": "🧮",
    "google news – placements": "🏢",
}


def _source_emoji(source: str) -> str:
    return _SOURCE_EMOJI.get(source.lower(), "📌")


def _format_article(index: int, article: Article) -> str:
    """Format a single article entry."""
    emoji = _source_emoji(article.source)
    lines = [f"{index}. {emoji} *{article.title}*"]
    if article.description:
        # Truncate description to ~120 chars
        desc = article.description[:120].rstrip()
        if len(article.description) > 120:
            desc += "…"
        lines.append(f"   ↳ _{desc}_")
    lines.append(f"   🔗 {article.link}")
    return "\n".join(lines)


def build_message(articles: list[Article]) -> str:
    """
    Build the full Telegram message from a list of articles.
    Respects the Telegram 4096-character limit.
    """
    if not articles:
        logger.warning("No articles to format — sending a fallback message.")
        return (
            "🔕 *Tech & Placement Update*\n\n"
            "No relevant news found this cycle. Check back in 3 hours! 🕐"
        )

    now_ist = datetime.now(timezone.utc).strftime("%d %b %Y, %I:%M %p UTC")
    header = (
        "🔥 *Tech & Placement Update*\n"
        f"📅 _{now_ist}_\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    footer = (
        "\n\n━━━━━━━━━━━━━━━━━━━━\n"
        "🎓 Stay sharp. Stay ahead.\n"
        "#TechNews #Placements #CSE #AI #Coding"
    )

    body_parts: list[str] = []
    current_len = len(header) + len(footer)

    for i, article in enumerate(articles, start=1):
        entry = _format_article(i, article)
        # +1 for the blank-line separator between entries
        if current_len + len(entry) + 2 > _MAX_MSG_LEN:
            logger.info("Message length cap reached at article %d.", i)
            break
        body_parts.append(entry)
        current_len += len(entry) + 2  # '\n\n' separator

    message = header + "\n\n".join(body_parts) + footer
    logger.info("Message built: %d chars, %d articles.", len(message), len(body_parts))
    return message

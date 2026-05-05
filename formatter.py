"""
formatter.py — Message formatting module.
Converts filtered articles into a Telegram-safe HTML message.
Uses HTML parse mode so links render as clickable underlined text,
not as long raw URLs.
"""

import logging
import html
from datetime import datetime, timezone

from fetcher import Article

logger = logging.getLogger(__name__)

# Telegram message hard limit is 4096 chars; stay safely below
_MAX_MSG_LEN = 4000

# Source emoji mapping
_SOURCE_EMOJI: dict[str, str] = {
    "hacker news":            "🟠",
    "dev.to":                 "👩‍💻",
    "techcrunch":             "🚀",
    "the verge":              "📰",
    "google news – ai":       "🤖",
    "google news – coding":   "💻",
    "google news – dsa":      "🧮",
    "google news – placements": "🏢",
}


def _source_emoji(source: str) -> str:
    return _SOURCE_EMOJI.get(source.lower(), "📌")


def _esc(text: str) -> str:
    """Escape text for Telegram HTML mode."""
    return html.escape(text)


def _format_article(index: int, article: Article) -> str:
    """
    Format one article entry using Telegram HTML.

    Output looks like:
        1. 🤖 <b>Article Title Here</b>
           ↳ Short description of the article...
           <a href="URL">📖 Read article</a>
    """
    emoji = _source_emoji(article.source)
    title = _esc(article.title)

    lines = [f"{index}. {emoji} <b>{title}</b>"]

    if article.description:
        desc = article.description[:120].rstrip()
        if len(article.description) > 120:
            desc += "…"
        lines.append(f"   ↳ <i>{_esc(desc)}</i>")

    # ── Compact hyperlink instead of raw URL ──────────────────────────────
    lines.append(f'   <a href="{article.link}">📖 Read article</a>')

    return "\n".join(lines)


def build_message(articles: list[Article]) -> tuple[str, str]:
    """
    Build the full Telegram message.
    Returns (message_text, parse_mode) tuple.
    parse_mode is always "HTML" now.
    """
    if not articles:
        logger.warning("No articles to format — sending fallback message.")
        return (
            "🔕 <b>Tech &amp; Placement Update</b>\n\n"
            "No new articles this cycle. Check back in 3 hours! 🕐",
            "HTML",
        )

    now_utc = datetime.now(timezone.utc).strftime("%d %b %Y, %I:%M %p UTC")
    header = (
        "🔥 <b>Tech &amp; Placement Update</b>\n"
        f"📅 <i>{now_utc}</i>\n"
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
        if current_len + len(entry) + 2 > _MAX_MSG_LEN:
            logger.info("Message length cap reached at article %d.", i)
            break
        body_parts.append(entry)
        current_len += len(entry) + 2  # '\n\n' separator

    message = header + "\n\n".join(body_parts) + footer
    logger.info("Message built: %d chars, %d articles.", len(message), len(body_parts))
    return message, "HTML"

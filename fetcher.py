"""
fetcher.py — RSS feed fetching module.
Retrieves articles from all configured feeds with retry logic.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.error import URLError

import feedparser

import config

logger = logging.getLogger(__name__)


@dataclass
class Article:
    """Represents a single news article."""
    title: str
    link: str
    description: str = ""
    source: str = ""
    published: str = ""

    def __hash__(self) -> int:
        return hash(self.link)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Article):
            return False
        return self.link == other.link


def _clean_html(raw: str) -> str:
    """Strip basic HTML tags from a string."""
    import re
    clean = re.sub(r"<[^>]+>", "", raw)
    # Collapse whitespace
    clean = " ".join(clean.split())
    return clean[:300]  # cap description length


def _fetch_single_feed(feed_info: dict, retries: int = 2) -> list[Article]:
    """Fetch and parse one RSS feed, returning a list of Articles."""
    name = feed_info["name"]
    url  = feed_info["url"]
    articles: list[Article] = []

    for attempt in range(1, retries + 2):
        try:
            parsed = feedparser.parse(url)
            if parsed.bozo and parsed.bozo_exception:
                # bozo flag means malformed feed — log but try to continue
                logger.warning("[%s] Malformed feed (attempt %d): %s", name, attempt, parsed.bozo_exception)

            entries = parsed.entries[: config.MAX_ARTICLES_PER_FEED]
            for entry in entries:
                title = _clean_html(getattr(entry, "title", "").strip())
                link  = getattr(entry, "link", "").strip()
                if not title or not link:
                    continue

                raw_desc = (
                    getattr(entry, "summary", "")
                    or getattr(entry, "description", "")
                    or ""
                )
                description = _clean_html(raw_desc)
                published   = getattr(entry, "published", "")

                articles.append(
                    Article(
                        title=title,
                        link=link,
                        description=description,
                        source=name,
                        published=published,
                    )
                )

            logger.info("[%s] Fetched %d articles.", name, len(articles))
            return articles

        except (URLError, Exception) as exc:
            logger.error("[%s] Attempt %d failed: %s", name, attempt, exc)
            if attempt <= retries:
                time.sleep(2)

    logger.error("[%s] All attempts failed; skipping feed.", name)
    return []


def fetch_all_feeds() -> list[Article]:
    """
    Iterate over all configured RSS feeds and aggregate unique articles.
    Returns a de-duplicated list ordered by feed priority.
    """
    seen_links: set[str] = set()
    all_articles: list[Article] = []

    for feed_info in config.RSS_FEEDS:
        articles = _fetch_single_feed(feed_info)
        for article in articles:
            if article.link not in seen_links:
                seen_links.add(article.link)
                all_articles.append(article)

    logger.info("Total unique articles fetched: %d", len(all_articles))
    return all_articles

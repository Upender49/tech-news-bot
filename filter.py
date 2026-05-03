"""
filter.py — Content filtering and prioritisation module.
Applies keyword matching, removes obvious clickbait, and caps results.
"""

import logging
import re
from typing import Optional

from fetcher import Article
import config

logger = logging.getLogger(__name__)

# Patterns that strongly suggest clickbait / low-quality titles
_CLICKBAIT_PATTERNS: list[re.Pattern] = [
    re.compile(r"\byou won'?t believe\b", re.I),
    re.compile(r"\bshocking\b", re.I),
    re.compile(r"\b\d+\s+things\s+you\b", re.I),
    re.compile(r"\bthis\s+one\s+trick\b", re.I),
    re.compile(r"\bmust[-\s]see\b", re.I),
    re.compile(r"\bblown away\b", re.I),
    re.compile(r"\bgone viral\b", re.I),
]


def _is_clickbait(title: str) -> bool:
    return any(pat.search(title) for pat in _CLICKBAIT_PATTERNS)


def _keyword_score(article: Article) -> int:
    """
    Return a relevance score based on keyword hits in title + description.
    Higher = more relevant.
    """
    haystack = (article.title + " " + article.description).lower()
    score = sum(1 for kw in config.FILTER_KEYWORDS if kw in haystack)
    return score


def filter_articles(articles: list[Article]) -> list[Article]:
    """
    Filter and rank articles:
    1. Remove clickbait titles.
    2. Score by keyword relevance.
    3. Keep articles with score >= 1 (at least one keyword match).
    4. Sort by score descending.
    5. Cap at MAX_TOTAL_ARTICLES.
    """
    scored: list[tuple[int, Article]] = []

    for article in articles:
        if _is_clickbait(article.title):
            logger.debug("Dropped (clickbait): %s", article.title[:60])
            continue

        score = _keyword_score(article)
        if score == 0:
            logger.debug("Dropped (no keyword match): %s", article.title[:60])
            continue

        scored.append((score, article))

    # Sort by score descending, then keep top N
    scored.sort(key=lambda x: x[0], reverse=True)
    filtered = [art for _, art in scored[: config.MAX_TOTAL_ARTICLES]]

    logger.info(
        "Filtered: %d → %d articles (max %d).",
        len(articles),
        len(filtered),
        config.MAX_TOTAL_ARTICLES,
    )
    return filtered

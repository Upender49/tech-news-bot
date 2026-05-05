"""
main.py — Orchestrator / entry-point.
Wires together: fetch → filter → format → send.
"""

import logging
import sys

import config
from fetcher import fetch_all_feeds
from filter import filter_articles
from formatter import build_message
from sender import send_long_message
from state import load_sent_urls, save_sent_urls


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run() -> None:
    """Main pipeline: fetch → filter (dedup) → format → send → save state."""
    logger = logging.getLogger("main")
    logger.info("═══════════ Tech News Bot starting ═══════════")

    # 1. Validate configuration
    if not config.validate_config():
        logger.critical("Aborting — fix environment variables first.")
        sys.exit(1)

    # 2. Load previously sent URLs (cross-run deduplication)
    seen_urls = load_sent_urls()

    # 3. Fetch articles from all RSS feeds
    articles = fetch_all_feeds()
    if not articles:
        logger.warning("No articles fetched from any feed.")

    # 4. Filter & rank — skipping already-sent articles
    filtered = filter_articles(articles, seen_urls=seen_urls)

    # 5. If nothing new this cycle, exit gracefully (no spam to group)
    if not filtered:
        logger.info("No new articles this cycle — all already sent or filtered out. Skipping.")
        sys.exit(0)

    # 6. Format into Telegram message
    message = build_message(filtered)

    # 7. Send to Telegram
    success = send_long_message(message)
    if success:
        # 8. Persist sent URLs so next run skips them
        new_urls = [article.link for article in filtered]
        save_sent_urls(seen_urls, new_urls)
        logger.info("Pipeline completed successfully. ✅")
    else:
        logger.error("Pipeline failed — message not delivered. ❌")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    run()

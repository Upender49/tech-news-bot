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
from state import load_state, save_state


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

    # 2. Load previously sent URLs and titles (cross-run deduplication)
    seen_urls, seen_titles = load_state()

    # 3. Fetch articles from all RSS feeds
    articles = fetch_all_feeds()
    if not articles:
        logger.warning("No articles fetched from any feed.")

    # 4. Filter & rank — skipping already-sent articles (URL or title match)
    filtered = filter_articles(articles, seen_urls=seen_urls, seen_titles=seen_titles)

    # 5. If nothing new this cycle, exit gracefully
    if not filtered:
        logger.info("No new articles this cycle — all already sent or filtered out. Skipping.")
        sys.exit(0)

    # 6. Format into Telegram message (HTML mode)
    message, parse_mode = build_message(filtered)

    # 7. Send to Telegram
    success = send_long_message(message, parse_mode=parse_mode)
    if success:
        # 8. Persist state so next run skips these articles
        save_state(seen_urls, seen_titles, filtered)
        logger.info("Pipeline completed successfully. ✅")
    else:
        logger.error("Pipeline failed — message not delivered. ❌")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    run()

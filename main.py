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


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run() -> None:
    """Main pipeline: fetch → filter → format → send."""
    logger = logging.getLogger("main")
    logger.info("═══════════ Tech News Bot starting ═══════════")

    # 1. Validate configuration
    if not config.validate_config():
        logger.critical("Aborting — fix environment variables first.")
        sys.exit(1)

    # 2. Fetch articles from all RSS feeds
    articles = fetch_all_feeds()
    if not articles:
        logger.warning("No articles fetched from any feed. Sending fallback message.")

    # 3. Filter & rank
    filtered = filter_articles(articles)

    # 4. Format into Telegram message
    message = build_message(filtered)

    # 5. Send to Telegram
    success = send_long_message(message)
    if success:
        logger.info("Pipeline completed successfully. ✅")
    else:
        logger.error("Pipeline failed — message not delivered. ❌")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    run()

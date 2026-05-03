"""
test_bot.py -- Quick local smoke-test.
Run:  python3.12 test_bot.py
Does NOT send a real Telegram message. Verifies fetch -> filter -> format pipeline.
"""

import logging
import sys
import os

# Force UTF-8 output on Windows terminals that default to cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Set dummy values so config doesn't abort during tests
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "DUMMY_TOKEN")
os.environ.setdefault("TELEGRAM_CHAT_ID", "DUMMY_CHAT_ID")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

from fetcher import fetch_all_feeds
from filter import filter_articles
from formatter import build_message

print("\n" + "=" * 60)
print("  Tech News Bot - Local Smoke Test")
print("=" * 60 + "\n")

print("[Step 1] Fetching RSS feeds...")
articles = fetch_all_feeds()
print(f"   -> {len(articles)} unique articles fetched.\n")

print("[Step 2] Filtering articles...")
filtered = filter_articles(articles)
print(f"   -> {len(filtered)} articles passed the filter.\n")

print("[Step 3] Formatting message...")
message = build_message(filtered)
print(f"   -> Message length: {len(message)} characters.\n")

print("=" * 60)
print("  PREVIEW (first 2000 chars):")
print("=" * 60)
print(message[:2000])
if len(message) > 2000:
    print(f"\n... ({len(message) - 2000} more characters)")
print("\n[OK] Smoke test complete. Review the output above.")

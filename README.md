# 🤖 Tech & Placement News Bot

> Automated Telegram bot that delivers curated AI/ML, Coding, DSA & Placement
> news to a group every **3 hours** — runs free on GitHub Actions, 24/7.

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Sources** | Google News (AI, Coding, DSA, Placements), Hacker News, Dev.to, TechCrunch, The Verge |
| **Filtering** | Keyword-relevance scoring + clickbait removal |
| **Formatting** | Numbered list with emoji, description, link |
| **Transport** | Telegram Bot API (stdlib `urllib` — zero extra HTTP lib) |
| **Scheduling** | GitHub Actions cron — every 3 hours |
| **Cost** | 100 % free |

---

## 📁 Project Structure

```
Automation/
├── main.py              # Orchestrator — fetch → filter → format → send
├── config.py            # All configuration & environment variable loading
├── fetcher.py           # RSS feed fetching (feedparser)
├── filter.py            # Keyword scoring & clickbait removal
├── formatter.py         # Telegram message builder
├── sender.py            # Telegram Bot API sender (urllib, retries, chunking)
├── test_bot.py          # Local smoke-test (no real Telegram call)
├── requirements.txt     # feedparser==6.0.11
├── .gitignore
└── .github/
    └── workflows/
        └── news_bot.yml # GitHub Actions workflow (cron every 3 h)
```

---

## 🚀 Quick Start (Local Testing)

### 1. Clone & install dependencies

```bash
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
cd <YOUR_REPO>
pip install -r requirements.txt
```

### 2. Run the smoke test (no Telegram needed)

```bash
python test_bot.py
```

You should see a formatted news message printed in the terminal.

### 3. Set environment variables (local)

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN = "123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TELEGRAM_CHAT_ID   = "-1001234567890"
python main.py
```

**Linux / macOS:**
```bash
export TELEGRAM_BOT_TOKEN="123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TELEGRAM_CHAT_ID="-1001234567890"
python main.py
```

---

## 🤖 Telegram Bot Setup (one-time)

### Step 1 — Create a Bot

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Enter a display name (e.g., *Tech News Bot*).
4. Enter a username ending in `bot` (e.g., `my_tech_news_bot`).
5. BotFather will give you a **token** that looks like:
   ```
   123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   → This is your `TELEGRAM_BOT_TOKEN`.

### Step 2 — Add the Bot to Your Group

1. Open your Telegram group (or create a new one).
2. Go to **Group Settings → Administrators → Add Administrator**.
3. Search for your bot username and add it.
4. Give it permission to **Send Messages**.

### Step 3 — Get the Chat ID

Option A — Use the Telegram API:
```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```
Send any message in the group, then look for `"chat":{"id": -100xxxxxxxxxx}`.

Option B — Add **@RawDataBot** to the group temporarily; it will print the chat ID.

> ⚠️ Group chat IDs are **negative** numbers (e.g., `-1001234567890`).

---

## ☁️ GitHub Actions Deployment (Free 24/7)

### Step 1 — Push your code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Tech News Bot"
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git push -u origin main
```

### Step 2 — Add GitHub Secrets

1. Go to your repository on GitHub.
2. Click **Settings → Secrets and variables → Actions → New repository secret**.
3. Add these two secrets:

| Secret Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your group chat ID (negative number) |

### Step 3 — Enable GitHub Actions

The workflow file at `.github/workflows/news_bot.yml` auto-triggers:
- **Every 3 hours** via cron schedule.
- **Manually** — go to Actions → Tech News Bot → Run workflow.

> 💡 GitHub Actions free tier includes **2,000 minutes/month**.
> This bot uses ~1–2 min per run × 8 runs/day × 30 days ≈ **240–480 minutes/month** — well within limits.

---

## ⚙️ Configuration Reference

| Environment Variable | Default | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | *(required)* | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | *(required)* | Target group/channel ID |
| `MAX_ARTICLES_PER_FEED` | `5` | Max articles fetched per RSS feed |
| `MAX_TOTAL_ARTICLES` | `12` | Max articles in one message |
| `FILTER_KEYWORDS` | *(see config.py)* | Comma-separated keyword list |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## 🧩 Adding / Removing RSS Feeds

Edit the `RSS_FEEDS` list in `config.py`:

```python
RSS_FEEDS = [
    {
        "name": "My Custom Feed",
        "url": "https://example.com/rss.xml",
    },
    # … existing feeds …
]
```

---

## 🔮 Future Extensions

| Feature | How to add |
|---|---|
| AI summarisation | Pass `article.description` to Gemini / OpenAI API in `formatter.py` |
| Multiple groups | Loop over a `CHAT_IDS` list in `sender.py` |
| Personalised categories | Add per-category feed groups and separate messages |
| Avoid repeated news | Persist sent URLs in a JSON file / lightweight DB |
| Job/internship channel | Add a `JOBS_CHAT_ID` and a second filtered pipeline |

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `TELEGRAM_BOT_TOKEN missing` | Set the environment variable / GitHub Secret |
| `HTTP 400` from Telegram | Wrong `CHAT_ID` or bot not in the group |
| `HTTP 403 Forbidden` | Bot was removed from the group; re-add it |
| No articles fetched | Feed URLs may be temporarily down; check logs |
| Message not arriving | Run `python test_bot.py` to verify pipeline first |

---

## 📜 License

MIT — free to use, modify, and share.

# 🎓 Aptitude Master Bot

A fully automated **Aptitude Teacher** Telegram bot for B.Tech final-year students targeting **campus placements** and **GATE General Aptitude**. Sends 10 curated, medium-to-hard aptitude questions every 3 hours — 24/7, zero manual effort.

---

## 📊 Topic Coverage (13 Phases)

| Phase | Topic | Importance |
|-------|-------|-----------|
| 1 | Percentages, Ratios & Proportions | 🔴 Must-Do |
| 2 | Averages, Mixtures & Alligation | 🟠 High Priority |
| 3 | Profit, Loss & Discounts | 🔴 Must-Do |
| 4 | Time & Work, Pipes & Cisterns | 🔴 Must-Do |
| 5 | Time, Speed & Distance | 🔴 Must-Do |
| 6 | Simple & Compound Interest | 🟡 Medium |
| 7 | Number System & Divisibility | 🔴 Must-Do |
| 8 | Permutations & Combinations | 🟠 High Priority |
| 9 | Probability | 🟠 High Priority |
| 10 | Logical Reasoning | 🔴 Must-Do |
| 11 | Data Interpretation | 🔴 Must-Do |
| 12 | Verbal Ability & English | 🟠 High Priority |
| 13 | Spatial & Analytical Reasoning | 🟡 Medium |

---

## 🏗️ Project Structure

```
Automation/
├── main.py                        # ← Main orchestrator (entry point)
├── aptitude_engine.py             # ← Question selection + message formatting
├── aptitude_syllabus.py           # ← 13-phase topic tree + weights
├── config.py                      # ← Env variable configuration
├── sender.py                      # ← Telegram Bot API (stdlib only)
├── requirements.txt               # ← No external deps needed
├── aptitude_state.json            # ← Learning progress (auto-updated)
│
├── aptitude_questions/            # ← Question bank (600+ questions)
│   ├── __init__.py                # ← Aggregates all questions
│   ├── quantitative.py            # ← Ph 1-3: %, Ratios, P&L, Avg, Mixtures
│   ├── time_work_speed.py         # ← Ph 4-6: Work, Speed, Interest
│   ├── number_perm_prob.py        # ← Ph 7-10: Numbers, PnC, Prob, Logic
│   └── di_verbal_spatial.py      # ← Ph 11-13: DI, Verbal, Spatial
│
└── .github/
    └── workflows/
        └── news_bot.yml           # ← GitHub Actions (runs every 3 hours)
```

---

## ⚙️ One-Time Setup (5 minutes)

### Step 1: Create a Telegram Bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **Bot Token** (looks like `123456789:ABCdef...`)

### Step 2: Get Your Group Chat ID

1. Add your bot to the Telegram group
2. Give it **Admin** permissions (to send messages)
3. Send any message in the group
4. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Find the `"chat"."id"` value (negative number for groups)

### Step 3: Fork This Repository

1. Push this code to a new **GitHub repository**
2. Go to **Settings → Secrets and variables → Actions**
3. Add two secrets:
   - `TELEGRAM_BOT_TOKEN` → your bot token
   - `TELEGRAM_CHAT_ID` → your group chat ID (with the `-` sign)

### Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repo
2. If prompted, click **"I understand my workflows, enable them"**
3. Click **"Aptitude Master Bot"** workflow → **"Run workflow"** to test

### Step 5: Verify It Works

- Check your Telegram group for a message within 1 minute
- The bot sends **10 questions per session, every 3 hours**

---

## 🔄 How the Bot Works

```
Every 3 Hours (GitHub Actions Cron)
         │
         ▼
 Load aptitude_state.json
         │
         ▼
 Phase rotation picks topic
 (e.g., Session 1: Percentages,
        Session 2: Number System,
        Session 3: Time & Work ...)
         │
         ▼
 Select 10 questions:
 • 7 from primary topic (medium-hard)
 • 2 from same phase (variety)
 • 1 mixed/hard question
         │
         ▼
 Format as Telegram HTML messages
 (Q + Answer + Full Explanation
  + Common Mistake + Key Formula)
         │
         ▼
 Send to Telegram Group
         │
         ▼
 Save updated state to repo
 (auto-commit, next session knows
  what was already sent)
```

---

## 📱 Sample Message Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 APTITUDE MASTER — Session #1
⚙️ Phase 4 — Time & Work, Pipes & Cisterns
📚 Topic: Time & Work
🎯 Priority: 🔴 Must-Do
━━━━━━━━━━━━━━━━━━━━━━━━━

Q1. [NAT · 2M · ⭐⭐⭐ Hard]
📌 Ph-4: Time & Work › LCM Method

A can do a piece of work in 12 days. B is 50% more
efficient than A. In how many days will B alone
complete the same work?

✅ Answer: 8 (NAT)

📌 Concept: Efficiency ratio inversely proportional to time

📖 Solution:
A's time = 12 days → A's efficiency = 1/12 per day
B is 50% more efficient → B's efficiency = (1/12) × 1.5 = 1/8
B's time = 8 days

⚠️ Common Mistake:
Adding 50% to 12 days (getting 18 days). Efficiency
increases → time DECREASES.

💡 Key Formula / Rule:
If B is x% more efficient than A,
Time_B = Time_A / (1 + x/100)
```

---

## 🔧 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Required | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Required | Your group chat ID |
| `QUESTIONS_PER_SESSION` | `10` | Questions per 3-hour session |
| `BOT_MODE` | `aptitude` | Mode: `aptitude` or `gate` |
| `LOG_LEVEL` | `INFO` | Python logging level |

---

## 📈 Smart Features

| Feature | Description |
|---------|-------------|
| **Phase Rotation** | Covers all 13 topics in weighted order |
| **Anti-Repetition** | Never sends the same question twice (FIFO eviction) |
| **Difficulty** | All questions are medium-to-hard (placement/GATE level) |
| **Instant Answer** | Answer + full explanation shown immediately |
| **Common Mistakes** | Highlights trap errors students commonly make |
| **Key Formulas** | Ends each Q with the formula to remember |
| **State Persistence** | Progress saved to repo; survives restarts |
| **Free & Unlimited** | GitHub Actions free tier (2000 min/month) |

---

## ❓ FAQ

**Q: Will the GitHub Actions free tier be enough?**
> Yes. Each run takes ~20 seconds. 8 runs/day × 30 days = 240 runs/month ≈ 80 minutes/month. Well within the 2000 min/month free limit.

**Q: What if a question sends twice?**
> The state file tracks all sent question IDs. It only repeats if you delete `aptitude_state.json`.

**Q: Can I add my own questions?**
> Yes! Add a dict following the question format to any file in `aptitude_questions/` and it will automatically be included.

**Q: How do I test locally?**
> ```bash
> export TELEGRAM_BOT_TOKEN="your_token"
> export TELEGRAM_CHAT_ID="your_chat_id"
> python main.py
> ```

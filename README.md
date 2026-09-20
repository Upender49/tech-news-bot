# 🎯 GATE CSE Personal Teacher Bot

An automated personal teacher and learning companion for **GATE Computer Science & Information Technology (CS)**.

Runs serverless every **3 hours** on GitHub Actions to deliver 10 syllabus-mapped questions with step-by-step solutions, GATE traps, formula takeaways, and spaced repetition tracking directly to Telegram.

---

## 🏛️ System Architecture

```
                               ┌────────────────────────────────┐
                               │     GitHub Actions Cron        │
                               │        (Every 3 Hours)         │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                                         [ main.py ]
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
       [ config.py ]                  [ gate_engine.py ]                 [ sender.py ]
    (Telegram credentials,           (Priority Scoring,             (HTTP POST to Telegram
     Session parameters)              Spaced Repetition,               Bot API with retry)
                                      Adaptive Chunking)
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
              [ gate_syllabus.py ]                            [ gate_state.json ]
          (Official GATE CS Tree &                       (Tracks Day, Phase, Sent IDs,
             Historical Weights)                          Syllabus Coverage, History)
                       │
                       ▼
              [ gate_questions/ ]
         • Engineering Mathematics
         • Discrete Mathematics
         • Digital Logic
         • Computer Organization & Architecture
         • Programming & Data Structures
         • Algorithms
         • Theory of Computation
         • Compiler Design
         • Operating Systems
         • Databases (DBMS)
         • Computer Networks
         • General Aptitude (Verbal, Quant, Analytical, Spatial)
         • Verified Previous Year Questions (PYQs)
```

---

## 📚 Official GATE Syllabus & Priority Engine

The bot uses historical weightage analysis (GATE 2018–2025) and active syllabus tracking to dynamically balance question distribution:

| Subject | Weightage % | Tier |
|:---|:---:|:---|
| **General Aptitude** (Verbal, Quant, Analytical, Spatial) | 15.0% | Tier 0 (Compulsory every session) |
| **Programming & Data Structures** | 9.8% | Tier 1 (High Priority) |
| **Computer Organization & Architecture** | 9.4% | Tier 1 (High Priority) |
| **Operating Systems** | 8.8% | Tier 1 (High Priority) |
| **Discrete Mathematics** | 8.4% | Tier 1 (High Priority) |
| **Computer Networks** | 8.3% | Tier 2 |
| **Theory of Computation** | 8.0% | Tier 2 |
| **Algorithms** | 8.0% | Tier 2 |
| **Databases (DBMS)** | 7.3% | Tier 2 |
| **Engineering Mathematics** (Linear Algebra, Calculus, Probability) | 5.8% | Tier 3 |
| **Compiler Design** | 5.5% | Tier 3 |
| **Digital Logic** | 5.0% | Tier 3 |

---

## 🗓️ 90-Day Learning Plan Progression

Sessions automatically advance across 7 progressive phases:

1. **Phase 1 (Days 1–10):** Foundation & Core Principles across Tier 1 subjects
2. **Phase 2 (Days 11–35):** Deep Dive into High-Weightage Core CS
3. **Phase 3 (Days 36–50):** Comprehensive Syllabus Coverage (Tier 2 & 3)
4. **Phase 4 (Days 51–60):** Verified Previous Year Question (PYQ) Mastery
5. **Phase 5 (Days 61–70):** Weak Area Targeting & Formula Revision
6. **Phase 6 (Days 71–80):** Multi-Subject Integrated Problems
7. **Phase 7 (Days 81–90):** Full Exam Mock Simulations

---

## ⚡ Question Types & Format

Each 3-hour session sends **10 GATE Questions**:
- **MCQ** (Multiple Choice Questions)
- **MSQ** (Multiple Select Questions — Select all correct)
- **NAT** (Numerical Answer Type — Exact numeric calculation)

Every answer includes:
- **📌 Core Concept** tested
- **Detailed Step-by-Step Derivation**
- **⚠️ GATE Trap / Pitfall** to avoid
- **💡 Key Formula / Takeaway**
- **🔗 Reference Link** for long explanations

---

## 🛠️ Configuration & Secrets

Set the following GitHub Repository Secrets under **Settings > Secrets and variables > Actions**:

| Secret Name | Description |
|:---|:---|
| `TELEGRAM_BOT_TOKEN` | Token from `@BotFather` |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat or Channel ID |

### Optional Runtime Environment Variables:
- `QUESTIONS_PER_SESSION`: Number of questions per run (default: `10`)
- `QUIZ_INTERVAL_HOURS`: Schedule interval (default: `3`)
- `STUDY_PLAN_DAYS`: Target completion timeline (default: `90`)
- `LOG_LEVEL`: Logging verbosity (`INFO`, `DEBUG`)

---

## 🧪 Local Verification

Run the test suite locally:
```bash
python test_gate.py
```

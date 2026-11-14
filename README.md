# Autonomous Desi Hip-Hop (DHH) Instagram Media Network

An enterprise-grade, completely automated, local-first media publishing and community management platform engineered specifically for **Desi Hip-Hop (DHH)** culture.

Runs 100% locally on Windows 10/11 with zero mandatory cloud subscriptions, zero paid API dependencies, and official Meta Instagram Graph API compliance.

---

## ⚡ Daily Autonomous Publishing Targets
- **10 Instagram Image / Carousel Posts** (Pillow-rendered high-res 1080x1080 & 1080x1350 meme cards).
- **5 Instagram Reels** (Vertical 9:16 1080x1920 MP4 video, animated slides, safe margins, and royalty-free synthesized 808 trap audio).
- **1+ Instagram Stories** (Interactive 1080x1920 cards: Guess the Rapper, This or That, Complete the Lyric, Trivia).
- **Continuous Comment Classification & Autonomous Hinglish Replies** (Sentiment analysis, spam/abuse filters, witty community responses).
- **Autonomous Trend Radar & DHH News Discovery** (Underground emcees, new releases, diss tracks, studio debates).
- **Weekly Empirical Self-Learning Feedback Loop** (Analyzes share-to-reach and saves-to-reach to re-weight publishing strategies).

---

## 🛠️ Technology Stack (Free & Local First)

- **Backend**: Python 3.11+ / 3.14, FastAPI, SQLAlchemy ORM, SQLite database.
- **Task Scheduling**: APScheduler with Asia/Kolkata (`IST`) timezone distribution.
- **Video Rendering**: FFmpeg with H.264/AAC encoding, safe-zone positioning, and synthetic audio wave generation.
- **Image Generation**: Pillow (PIL) high-precision typography and dark-mode meme layout composition.
- **Local AI Engine**: Native Ollama client (`llama3:latest`, `mistral`, etc.) + deterministic DHH Cultural Knowledge & Template Engine fallback (operates 100% offline even if Ollama is not installed).
- **Frontend Dashboard**: React 18, Vite 5, Tailwind CSS, Lucide icons (served at `http://127.0.0.1:8787`).
- **Official Meta Instagram Graph API**: v21.0 compliance, OAuth 2.0 long-lived token management, container status polling, media delivery abstraction, plus a 100% faithful Mock / Dry-Run Simulation Mode for offline testing.

---

## 📂 Project Structure

```text
dhh_media_network/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI server entrypoint & SPA static mount
│   │   ├── config.py                  # Pydantic environment settings
│   │   ├── database.py                # SQLAlchemy SQLite session factory
│   │   ├── seed.py                    # Initial seed data for DHH topics & posts
│   │   ├── models/                    # 8 SQLAlchemy models (Accounts, Content, Comments, SEO, etc.)
│   │   ├── api/                       # 17 FastAPI REST routers for each dashboard view
│   │   └── services/
│   │       ├── ai_engine.py           # Ollama client + Cultural template fallback + Quality scoring
│   │       ├── dhh_knowledge.py       # Curated artists, producers, slang dictionary, meme presets
│   │       ├── meme_engine.py         # 1080x1080 Pillow meme renderer (Tweet-style, Split comparison)
│   │       ├── reels_engine.py        # 1080x1920 FFmpeg 9:16 vertical video & 808 audio synthesizer
│   │       ├── story_engine.py        # 1080x1920 9:16 interactive Story card generator
│   │       ├── instagram_client.py    # Official Meta Graph API v21.0 client + Mock mode
│   │       ├── comment_engine.py      # NLP classification & autonomous Hinglish reply dispatcher
│   │       ├── seo_engine.py          # Caption optimizer, 3-5 hashtag selector, Bio strategy generator
│   │       ├── scheduler_engine.py    # APScheduler loop distributing daily posts, reels, and stories
│   │       ├── growth_learning_engine.py # Weekly self-learning feedback loop
│   │       ├── reliability_engine.py  # Health watchdog, auto-recovery heuristics & code repair sandbox
│   │       └── backup_engine.py       # Atomic SQLite database snapshots
│   ├── data/
│   │   ├── dhh_media.db               # SQLite relational database
│   │   ├── media/                     # Rendered memes, reels, stories, covers, audio
│   │   └── backups/                   # Pruned database snapshots
│   └── tests/
│       └── test_all_subsystems.py     # Automated pytest test suite (100% pass)
├── frontend/                          # React + Vite + Tailwind CSS dashboard
│   ├── src/
│   │   ├── App.jsx                    # Master shell with 18 responsive sections
│   │   └── views/                     # 18 dedicated interactive dashboard views
│   └── dist/                          # Compiled production assets
├── START.bat                          # One-click start script
├── STOP.bat                           # Clean background process killer
├── healthcheck.bat                    # Diagnostic health-check CLI
├── backup.bat                         # Manual database snapshot CLI
├── restore.bat                        # Database restoration CLI
├── install.bat                        # Dependency installation script
├── requirements.txt                   # Locked Python dependencies
└── README.md                          # Documentation
```

---

## 🚀 Quick Start (One-Click Windows Launch)

### 1. Launch the Network
Simply double-click:
```bat
START.bat
```
This batch script will:
1. Validate Python and virtual environment.
2. Initialize database and cultural seeds if not present.
3. Start the FastAPI server and background scheduler on `http://127.0.0.1:8787`.
4. Open the interactive Control Dashboard in your default browser.

### 2. Stop the Network
Double-click:
```bat
STOP.bat
```
Cleanly terminates background processes on port 8787.

---

## 🖥️ Local Control Dashboard (18 Complete Sections)

Accessible at `http://127.0.0.1:8787`:

1. **Overview**: Live KPIs, today's target progress bars (Posts, Reels, Stories), total reach, emergency stop & pause controls.
2. **Content Generator**: One-click generation of DHH Memes, Video Reels, and Stories with category filters.
3. **Meme Studio**: Visual canvas supporting Twitter/X dark cards and Expectation vs. Reality split comparison templates.
4. **Reels Studio**: 9:16 vertical video player preview, multi-slide scene editor, safe-area overlay, and custom cover creator.
5. **Story Studio**: Interactive 9:16 quiz & trivia creator (Guess the Rapper, This or That, Complete the Lyric).
6. **Publishing Calendar**: Visual timeline of scheduled, published, and queued events aligned to Indian peak hours (IST).
7. **Pending Queue**: Priority queue manager with idempotency hashes and instant "Publish Now" triggers.
8. **Published Content**: Grid and table of published posts with direct Instagram links and reach/engagement counters.
9. **Comment Manager**: Fan comment inbox with automated sentiment classification and Hinglish reply simulator.
10. **SEO Manager**: Search-optimized caption builder (under 125 char hook, 3-5 clustered hashtags, alt text).
11. **Audience Growth**: DHH trend radar, artist directory, collaboration outreach pitch generator, and optimal posting windows.
12. **Analytics & Learning**: Virality matrix (share-to-reach, saves-to-reach) and automated weekly strategy revision reports.
13. **AI Settings**: Ollama local daemon connection test, model selector, temperature threshold, and prompt test bench.
14. **Instagram Connection**: Meta Graph API connection wizard, permission checklist, token validator, and Mock Mode toggle.
15. **Error Logs**: Traceback inspector, auto-recovery routine runner, and isolated code repair sandbox.
16. **System Health**: Real-time diagnostic monitors for DB integrity, FFmpeg video engine, AI daemon, and disk space.
17. **Backup and Restore**: Snapshot manager with one-click database restore.
18. **General Settings**: Configurable daily quotas (Posts: 10, Reels: 5, Stories: 1) and timezone settings.

---

## 🔑 Meta Instagram Graph API Setup Guide

The application comes with **Mock / Dry-Run Mode enabled by default**, allowing 100% full functionality, testing, and UI interactions without connecting an external account.

When ready to connect your live Instagram account:

1. **Convert to Professional Account**:
   Open Instagram on your phone > Settings > Account Type > Switch to Professional Account (Creator or Business).
2. **Link a Facebook Page**:
   Create a Facebook Page (e.g., *Desi Hip Hop Cult*) and link it to your Instagram Professional account in Instagram settings.
3. **Register Meta Developer App**:
   Go to [Meta for Developers](https://developers.facebook.com/) > Create App > Choose **Business** use case.
4. **Add Instagram Graph API**:
   In your Meta App Dashboard, add the **Instagram Graph API** product.
5. **Obtain Permissions**:
   Under App Review or Permissions, ensure the following are enabled:
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_comments`
   - `instagram_manage_insights`
   - `pages_show_list`
   - `pages_read_engagement`
6. **Generate 60-Day Long-Lived Token**:
   Use Meta Graph API Explorer to generate a User Access Token with the above permissions, then exchange it for a long-lived page token via `/oauth/access_token`.
7. **Save in Dashboard**:
   Navigate to the **Instagram Connection** tab in the dashboard, enter your Access Token and Instagram Account ID, and toggle off Mock Mode.

---

## 🤖 Windows Task Scheduler (Automatic Boot on PC Startup)

To have the network start automatically whenever you turn on your PC:
1. Press `Win + R`, type `taskschd.msc`, and hit Enter.
2. Click **Create Basic Task...** and name it `DHH Media Network`.
3. Trigger: Select **When I log on**.
4. Action: Select **Start a program**.
5. Program/script: Browse to `START.bat` in this directory.
6. Start in: Enter the path `C:\Users\rusha\.gemini\antigravity\scratch\dhh_media_network\`.
7. Finish. Now the autonomous publisher will start with your computer silently in the background!

---

## 🛡️ Platform Compliance & Safety

- **No Scraping / No Unofficial Bots**: Communicates solely through official Meta Graph API endpoints.
- **Idempotency**: Every queued item has a cryptographic idempotency hash to prevent duplicate publishing.
- **Copyright Safe**: All Reel audio tracks are synthesized locally using royalty-free 808 trap wave algorithms.
- **Zero Hallucination / Anti-Defamation**: Cultural engine focuses on relatable fan tropes, studio struggles, and public music discographies rather than fabricated rumors.

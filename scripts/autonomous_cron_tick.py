import os
import sys
import json
import base64
import time
import urllib.request
import asyncio
from pathlib import Path
from datetime import datetime, timezone

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings
from backend.app.services.instagram_client import InstagramAPIClient
from backend.app.services.meme_engine import meme_engine
from backend.app.services.story_engine import story_engine
from backend.app.services.reel_engine import reel_engine
from backend.app.services.template_finder import template_finder

GITHUB_TOKEN = os.getenv("PAT_TOKEN") or os.getenv("GITHUB_TOKEN") or ""
REPO = "simplymusicalhindi-cyber/dhh-media-network"
BRANCH = "main"

def push_file_to_github(local_path: Path, repo_path: str, commit_msg: str):
    """Uploads or updates a file in GitHub via the REST API."""
    with open(local_path, "rb") as f:
        content_bytes = f.read()
    b64_content = base64.b64encode(content_bytes).decode("utf-8")
    
    url = f"https://api.github.com/repos/{REPO}/contents/{repo_path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DHH-Autonomous-Bot"
    }
    
    sha = None
    try:
        req = urllib.request.Request(f"{url}?ref={BRANCH}", headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            sha = data.get("sha")
    except Exception:
        pass
        
    payload = {
        "message": commit_msg,
        "content": b64_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha
        
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="PUT"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_latest_post_info():
    """Fetch the latest post timestamp from Instagram Graph API."""
    url = f"https://graph.facebook.com/v19.0/{settings.INSTAGRAM_ACCOUNT_ID}/media?fields=id,timestamp,permalink,caption&limit=1&access_token={settings.ACCESS_TOKEN}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("data", [])
            if items:
                return items[0]
    except Exception as e:
        print("Error fetching latest post:", e)
    return None

async def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] === DHH Autonomous Watchdog Tick ===")
    
    # 1. Ping Render Service and Queue Tick to guarantee it never sleeps and executes due jobs
    for endpoint in ["/health", "/api/queue/tick"]:
        try:
            req = urllib.request.Request(f"https://dhh-media-network.onrender.com{endpoint}", headers={"User-Agent": "DHH-Watchdog/1.0"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                print(f"Render {endpoint} ping: HTTP {resp.status}")
        except Exception as e:
            print(f"Render {endpoint} notice: {e}")

    # 2. Check and run daily template discovery if not yet executed today
    try:
        today_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        import sqlite3
        conn = sqlite3.connect(settings.DATA_DIR / "dhh_media.db")
        c = conn.cursor()
        c.execute("SELECT count(*) FROM reel_templates WHERE created_at LIKE ?", (f"{today_prefix}%",))
        count_today = c.fetchone()[0]
        conn.close()
        if count_today == 0:
            print("[Watchdog] Running autonomous daily template discovery...")
            template_finder.run_daily_discovery()
        else:
            print(f"[Watchdog] Templates discovery already completed today ({count_today} added).")
    except Exception as tpl_err:
        print("[Watchdog] Template check notice:", tpl_err)

    # 3. Check time elapsed since last Instagram post
    latest = get_latest_post_info()
    hours_since_last_post = 999.0
    if latest and latest.get("timestamp"):
        try:
            # Parse ISO timestamp like 2026-11-15T09:26:31+0000
            ts_str = latest["timestamp"].replace("+0000", "+00:00")
            post_time = datetime.fromisoformat(ts_str)
            now = datetime.now(timezone.utc)
            delta = now - post_time
            hours_since_last_post = delta.total_seconds() / 3600.0
            print(f"Latest post ID {latest.get('id')} was published {hours_since_last_post:.2f} hours ago ({latest.get('permalink')})")
        except Exception as e:
            print("Timestamp parse error:", e)

    # Max allowed inactivity threshold: 4.0 hours (between 6 AM and 11 PM IST)
    # 6 AM to 11 PM IST is 00:30 to 17:30 UTC
    now_utc = datetime.now(timezone.utc)
    is_active_hours = 0 <= now_utc.hour <= 18  # Covers prime Indian time

    print(f"Hours since last post: {hours_since_last_post:.2f}h | Active hours: {is_active_hours}")

    if hours_since_last_post >= 3.5 and is_active_hours:
        print("THRESHOLD EXCEEDED: Autonomously generating and publishing fresh DHH post...")
        client = InstagramAPIClient(mock_mode=False)
        import random

        post_type = random.choice(["REEL", "MEME"])

        if post_type == "REEL":
            print("[Watchdog] Generating fresh autonomous DHH Reel using fresh template...")
            reel_hooks = [
                ("POV: Delhi producer sending unmixed 808s at 4 AM saying 'Bhai loop check kar' 💀", "Every single producer-rapper dynamic in DHH 😭 Who is that one producer friend for you? Drop below! 👇\n\n#DesiHipHop #DHH #SeedheMaut #KR$NA #FLStudio #DHHMemes #IndianHipHop"),
                ("When the sub-bass drops on an Umair beat and your earphones start vibrating 🔊🚗💀", "No one: \nUmair in the studio: 🔥🔊 What's your favorite beat drop this year? Drop below! 👇\n\n#DesiHipHop #DHH #Umair #TalhaAnjum #SubBass #DHHMemes #IndianHipHop"),
                ("Hardcore DHH fan explaining how a 12-bar scheme connects to Greek mythology 😭", "Overanalyzing every single KR$NA bar like it's a board exam 💀 Who does this? Drop below 👇\n\n#DesiHipHop #DHH #KR$NA #Awam #Kalamkaar #DHHMemes #IndianHipHop"),
                ("Walking out of a Seedhe Maut moshpit with 1 missing shoe and 100% peace of mind 🧘‍♂️", "TBS4L or nothing ⚔️ Delhi scene hits different in person. Have you survived an SM moshpit? 👇\n\n#DesiHipHop #DHH #SeedheMaut #TBS4L #LunchBreak #DHHMemes #IndianHipHop"),
                ("Underground hip hop fan when their favorite artist crosses 50k monthly listeners 🥺", "Yesterday: 'Bhai underrated god hai!' 🥺 Today: 'Commercial ho gaya skip karo' 💀 #DesiHipHop #DHH #UndergroundHipHop #DHHMemes #IndianHipHop")
            ]
            hook_text, reel_caption = random.choice(reel_hooks)
            reel_res = reel_engine.render_autonomous_reel(hook_text)
            local_path = Path(reel_res["file_path"])
            repo_path = f"backend/data/media/reels/{reel_res['file_name']}"
            push_file_to_github(local_path, repo_path, f"Autonomous watchdog reel {reel_res['file_name']}")
            raw_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{repo_path}"
            
            print(f"Uploading and publishing reel {reel_res['file_name']} (Template: {reel_res.get('template_title')})...")
            pub_res = await client.publish_reel(raw_url, reel_caption)
            print("Reel publish result:", pub_res)
            if pub_res.get("status") == "PUBLISHED":
                print(f"SUCCESS: Autonomous watchdog posted Reel live! Link: {pub_res.get('permalink')}")
        else:
            # Generate clean meme
            templates_pool = [
                ("distracted_boyfriend", "DHH fans choosing what to obsess over after a new track drops:", [
                    {"text": "10-Sec Diss Subliminal", "x_pct": 0.22, "y_pct": 0.60, "box_color": "#EF4444", "text_color": "#FFFFFF"},
                    {"text": "DHH Audience", "x_pct": 0.58, "y_pct": 0.45, "box_color": "#3B82F6", "text_color": "#FFFFFF"},
                    {"text": "Insane Complex Rhyme Scheme", "x_pct": 0.85, "y_pct": 0.62, "box_color": "#10B981", "text_color": "#FFFFFF"}
                ], "Every single time a new project drops in DHH 💀 Complex rhyme schemes vs 10 seconds of subliminal beef. Which one caught your attention first? Drop your thoughts below! 👇\n\n#DesiHipHop #DHH #SeedheMaut #KR$NA #Raftaar #DIVINE #MCStan #DHHMemes #IndianHipHop"),

                ("two_buttons", "DHH audience every time an underground rapper crosses 100k views:", [
                    {"text": "Bhai Underrated God Hai", "x_pct": 0.30, "y_pct": 0.24, "box_color": "#2563EB", "text_color": "#FFFFFF"},
                    {"text": "Commercial Ho Gaya Skip Karo", "x_pct": 0.65, "y_pct": 0.17, "box_color": "#DC2626", "text_color": "#FFFFFF"}
                ], "The classic DHH underground paradox 😭💀 The second an underground artist gets their flowers, people start screaming 'commercial'! Who are you defending forever? Drop them below 👇\n\n#DesiHipHop #DHH #IndianRap #SeedheMaut #KR$NA #DHHMemes #IndianHipHop"),

                ("trade_offer", "POV: Underground Delhi producer sends you an Instagram DM at 3:30 AM", [
                    {"text": "YOU RECEIVE:\nUnfinished MP3 with 6 FL plugins crashing", "x_pct": 0.75, "y_pct": 0.32, "box_color": "#1E293B", "text_color": "#F8FAFC"},
                    {"text": "I RECEIVE:\n1 Story Share & 'Bhai Hard Hai'", "x_pct": 0.25, "y_pct": 0.32, "box_color": "#1E293B", "text_color": "#38BDF8"}
                ], "Every producer-artist relationship in the Indian hip hop scene at 3 AM 🎹💀 Tag that one producer who sends unmixed fire in your DMs! 👇\n\n#DesiHipHop #DHH #FLStudio #ProducerLife #Beatmakers #DHHMemes #IndianHipHop")
            ]

            t_name, t_head, t_overlays, t_caption = random.choice(templates_pool)

            meme_res = meme_engine.create_imgflip_card_meme(
                template_name=t_name,
                header_text=t_head,
                overlays=t_overlays,
                dark_mode=False
            )

            local_path = Path(meme_res["file_path"])
            repo_path = f"backend/data/media/memes/{meme_res['file_name']}"
            push_file_to_github(local_path, repo_path, f"Autonomous watchdog publish {meme_res['file_name']}")
            raw_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{repo_path}"

            print(f"Uploading and publishing {meme_res['file_name']}...")
            pub_res = await client.publish_image_post(raw_url, t_caption)
            print("Publish result:", pub_res)
            if pub_res.get("status") == "PUBLISHED":
                print(f"SUCCESS: Autonomous watchdog posted live! Link: {pub_res.get('permalink')}")
    else:
        print("Schedule is healthy. Next post scheduled within normal window.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as fatal_e:
        print(f"[FAILSAFE RECOVERY] Caught error: {fatal_e}")
        sys.exit(0)

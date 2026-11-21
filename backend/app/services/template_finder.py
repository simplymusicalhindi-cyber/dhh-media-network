import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import uuid
import base64
import urllib.request
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

try:
    import instaloader
except ImportError:
    instaloader = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

import sqlite3

from backend.app.config import settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = settings.DATA_DIR / "dhh_media.db"
TEMPLATES_DIR = settings.DATA_DIR / "media" / "reel_templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

REPO = "simplymusicalhindi-cyber/dhh-media-network"
BRANCH = "main"

class TemplateFinderService:
    """
    Autonomous multi-source reel template discovery service.
    Finds, validates, registers, and syncs fresh meme video templates daily.
    """
    def __init__(self):
        self.db_path = DB_PATH
        self.templates_dir = TEMPLATES_DIR
        self._ensure_table()
        
    def _ensure_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS reel_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_key TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                title TEXT,
                local_path TEXT NOT NULL,
                github_cdn_url TEXT,
                duration REAL,
                use_count INTEGER DEFAULT 0,
                last_used_at TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _push_to_github(self, local_path: Path, filename: str) -> Optional[str]:
        """Uploads downloaded video template to GitHub repository via REST API."""
        github_token = os.getenv("GITHUB_TOKEN") or getattr(settings, "GITHUB_TOKEN", "")
        if not github_token:
            print("[TemplateFinder] GITHUB_TOKEN not set; skipping GitHub push.")
            return None

        repo_path = f"backend/data/media/reel_templates/{filename}"
        url = f"https://api.github.com/repos/{REPO}/contents/{repo_path}"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DHH-Template-Finder"
        }

        try:
            with open(local_path, "rb") as f:
                b64_content = base64.b64encode(f.read()).decode("utf-8")

            # Check if exists to get sha
            sha = None
            try:
                req = urllib.request.Request(f"{url}?ref={BRANCH}", headers=headers)
                with urllib.request.urlopen(req) as resp:
                    sha = json.loads(resp.read().decode()).get("sha")
            except Exception:
                pass

            payload = {
                "message": f"Autonomous daily template sync: {filename}",
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
                data = json.loads(resp.read().decode())
                print(f"[TemplateFinder] Successfully synced {filename} to GitHub CDN.")
                return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{repo_path}"
        except Exception as e:
            print(f"[TemplateFinder] GitHub upload notice for {filename}: {e}")
            return None

    def register_template(self, template_key: str, source: str, title: str, local_path: Path, duration: Optional[float] = None) -> bool:
        """Register newly found template in database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now_str = datetime.now(timezone.utc).isoformat()
        cdn_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/backend/data/media/reel_templates/{local_path.name}"
        
        try:
            c.execute("""
                INSERT INTO reel_templates (template_key, source, title, local_path, github_cdn_url, duration, use_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?)
            """, (template_key, source, title, str(local_path), cdn_url, duration, now_str))
            conn.commit()
            conn.close()
            # Push to GitHub
            self._push_to_github(local_path, local_path.name)
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def discover_from_instagram(self, usernames: Optional[List[str]] = None, limit_per_user: int = 3) -> List[Dict[str, Any]]:
        """Scrape fresh vertical reel templates from curated Instagram accounts."""
        if not instaloader:
            print("[TemplateFinder] instaloader package not available, skipping Instagram scraping.")
            return []

        if usernames is None:
            usernames = ["templatesays", "desihiphopmemes", "thetemplatess", "allmemetemplates"]
            
        loader = instaloader.Instaloader(
            dirname_pattern=str(self.templates_dir),
            filename_pattern="{date_utc}_{shortcode}",
            download_pictures=False,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True
        )

        added = []
        for uname in usernames:
            try:
                print(f"[TemplateFinder] Checking Instagram source: @{uname}...")
                profile = instaloader.Profile.from_username(loader.context, uname)
                count = 0
                for post in profile.get_posts():
                    if not post.is_video:
                        continue
                        
                    key = post.shortcode
                    # Check if already registered
                    conn = sqlite3.connect(self.db_path)
                    exists = conn.execute("SELECT id FROM reel_templates WHERE template_key = ?", (key,)).fetchone()
                    conn.close()
                    if exists:
                        continue

                    title = (post.caption or "").replace("\n", " ")[:70] or f"Instagram Template {key}"
                    print(f"[TemplateFinder] Downloading new reel template from @{uname}: {key} ({title})")
                    loader.download_post(post, target=str(self.templates_dir))
                    
                    # Locate the downloaded mp4
                    matches = list(self.templates_dir.glob(f"*{key}*.mp4"))
                    if matches:
                        mp4_file = matches[0]
                        if self.register_template(key, f"instagram:@{uname}", title, mp4_file):
                            added.append({"key": key, "source": f"instagram:@{uname}", "title": title, "path": str(mp4_file)})
                            count += 1
                            if count >= limit_per_user:
                                break
            except Exception as e:
                print(f"[TemplateFinder] Instagram @{uname} check notice: {e}")
                
        return added

    def discover_from_youtube_shorts(self, queries: Optional[List[str]] = None, limit_per_query: int = 3) -> List[Dict[str, Any]]:
        """Search and download fresh 9:16 vertical meme video templates from YouTube Shorts."""
        if not yt_dlp:
            print("[TemplateFinder] yt_dlp package not available, skipping YouTube scraping.")
            return []

        if queries is None:
            queries = [
                "dhh meme template shorts",
                "seedhe maut meme template shorts",
                "krsna meme template shorts",
                "raftaar meme template shorts",
                "mc stan meme template shorts",
                "arpit bala meme template shorts",
                "samay raina meme template shorts",
                "indian meme template shorts",
                "trending meme template no text shorts"
            ]

        added = []
        for q in queries:
            try:
                print(f"[TemplateFinder] Searching YouTube Shorts: '{q}'...")
                ydl_opts_search = {'quiet': True, 'extract_flat': True}
                with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                    search_res = ydl.extract_info(f"ytsearch8:{q}", download=False)
                    entries = search_res.get("entries", [])

                count = 0
                for entry in entries:
                    vid_id = entry.get("id")
                    title = entry.get("title", "")
                    duration = entry.get("duration") or 0
                    
                    # Only accept short vertical clips (<= 60 seconds)
                    if duration > 60 or duration < 3:
                        continue

                    conn = sqlite3.connect(self.db_path)
                    exists = conn.execute("SELECT id FROM reel_templates WHERE template_key = ?", (vid_id,)).fetchone()
                    conn.close()
                    if exists:
                        continue

                    out_path = self.templates_dir / f"yt_short_{vid_id}.mp4"
                    print(f"[TemplateFinder] Downloading YouTube Short template: {vid_id} - '{title}' ({duration}s)")
                    
                    ydl_opts_dl = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': str(self.templates_dir / f"yt_short_{vid_id}.%(ext)s"),
                        'quiet': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_dl) as dl_ydl:
                        dl_ydl.download([f"https://www.youtube.com/shorts/{vid_id}"])

                    if out_path.exists():
                        if self.register_template(vid_id, "youtube_shorts", title, out_path, float(duration)):
                            added.append({"key": vid_id, "source": "youtube_shorts", "title": title, "path": str(out_path)})
                            count += 1
                            if count >= limit_per_query:
                                break
            except Exception as e:
                print(f"[TemplateFinder] YouTube search '{q}' notice: {e}")

        return added

    def run_daily_discovery(self) -> Dict[str, Any]:
        """Executes full daily multi-source discovery pipeline."""
        print(f"\n=======================================================")
        print(f"[{datetime.now(timezone.utc).isoformat()}] STARTING DAILY REEL TEMPLATE DISCOVERY")
        print(f"=======================================================")
        
        ig_added = self.discover_from_instagram()
        yt_added = self.discover_from_youtube_shorts()
        
        total_new = len(ig_added) + len(yt_added)
        
        conn = sqlite3.connect(self.db_path)
        total_catalog = conn.execute("SELECT count(*) FROM reel_templates").fetchone()[0]
        conn.close()
        
        res = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "new_templates_found": total_new,
            "instagram_templates": ig_added,
            "youtube_templates": yt_added,
            "total_catalog_size": total_catalog
        }
        print(f"[TemplateFinder] Daily discovery complete! Added {total_new} new templates. Total catalog: {total_catalog}\n")
        return res

    def get_fresh_template(self) -> Dict[str, Any]:
        """
        Retrieves the freshest, least-used template from the catalog to ensure maximum content variety.
        Automatically increments its usage count and updates last_used_at.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Select least used templates, randomized among top 5 lowest use counts
        row = c.execute("""
            SELECT * FROM reel_templates 
            ORDER BY use_count ASC, RANDOM() 
            LIMIT 1
        """).fetchone()
        
        if not row:
            # Auto-seed from committed video templates in directory
            mp4_files = list(self.templates_dir.glob("*.mp4"))
            now_str = datetime.now(timezone.utc).isoformat()
            for mp4 in mp4_files:
                key = mp4.stem
                title = f"DHH Template {key}"
                cdn_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/backend/data/media/reel_templates/{mp4.name}"
                try:
                    c.execute("""
                        INSERT INTO reel_templates (template_key, source, title, local_path, github_cdn_url, duration, use_count, created_at)
                        VALUES (?, 'local_seed', ?, ?, ?, 15.0, 0, ?)
                    """, (key, title, str(mp4), cdn_url, now_str))
                except Exception:
                    pass
            conn.commit()
            
            row = c.execute("""
                SELECT * FROM reel_templates 
                ORDER BY use_count ASC, RANDOM() 
                LIMIT 1
            """).fetchone()

        if not row:
            conn.close()
            raise RuntimeError("No templates found in reel_templates catalog.")
            
        tpl_data = dict(row)
        now_str = datetime.now(timezone.utc).isoformat()
        c.execute("""
            UPDATE reel_templates 
            SET use_count = use_count + 1, last_used_at = ? 
            WHERE id = ?
        """, (now_str, tpl_data["id"]))
        conn.commit()
        conn.close()
        
        return tpl_data

template_finder = TemplateFinderService()

if __name__ == "__main__":
    summary = template_finder.run_daily_discovery()
    print("Execution Summary:", json.dumps(summary, indent=2))

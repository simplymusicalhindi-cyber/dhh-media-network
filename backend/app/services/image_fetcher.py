import os
import re
import uuid
import hashlib
import urllib.request
import json
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image
from backend.app.config import settings

class ImageFetcher:
    """Fetches real news pictures, artist press photos, and event images from public sources."""

    def __init__(self):
        self.temp_dir = settings.MEDIA_DIR / "temp"
        self.artists_dir = settings.DATA_DIR / "media" / "artists"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.artists_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DHHPressNetwork/1.0"}

    def download_image(self, image_url: str) -> Optional[str]:
        """Download an image URL into a local file and verify it with PIL."""
        if not image_url or not image_url.startswith("http"):
            return None
        try:
            url_hash = hashlib.md5(image_url.encode()).hexdigest()[:12]
            dest = self.temp_dir / f"news_{url_hash}.jpg"
            if dest.exists() and dest.stat().st_size > 5000:
                return str(dest)

            req = urllib.request.Request(image_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                content = resp.read()

            # Verify with PIL and convert to RGB JPEG
            import io
            with Image.open(io.BytesIO(content)) as im:
                rgb = im.convert("RGB")
                rgb.save(str(dest), "JPEG", quality=90)

            return str(dest)
        except Exception:
            return None

    def extract_og_image(self, page_url: str) -> Optional[str]:
        """Follow an article page URL and extract its og:image tag."""
        if not page_url or not page_url.startswith("http"):
            return None
        try:
            req = urllib.request.Request(page_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=7) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                
                # Check og:image
                m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
                if not m:
                    m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.I)
                if not m:
                    m = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)

                if m:
                    img_url = m.group(1).strip()
                    if img_url.startswith("http"):
                        return self.download_image(img_url)
        except Exception:
            pass
        return None

    def search_wikipedia_image(self, query: str) -> Optional[str]:
        """Search Wikipedia API for an artist / album / festival photo."""
        clean = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()
        tokens = clean.split()
        if not tokens:
            return None
        
        # Try full or top 2 words
        candidate_terms = ["_".join(tokens[:2]), tokens[0]]
        for term in candidate_terms:
            try:
                api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={term}&prop=pageimages&format=json&pithumbsize=960"
                req = urllib.request.Request(api_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                    pages = data.get("query", {}).get("pages", {})
                    for pid, pdata in pages.items():
                        thumb = pdata.get("thumbnail", {}).get("source")
                        if thumb:
                            local_path = self.download_image(thumb)
                            if local_path:
                                return local_path
            except Exception:
                continue
        return None

    def get_real_news_image(
        self,
        headline: str,
        article_url: Optional[str] = None,
        direct_image_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Master method to resolve the real pic for a news post:
        1. Direct news image URL (e.g. from RSS)
        2. Web page og:image scraping
        3. Local verified artist photo library
        4. Wikipedia / Commons search
        """
        # 1. Direct image URL
        if direct_image_url:
            local = self.download_image(direct_image_url)
            if local:
                return local

        # 2. Extract from article URL
        if article_url:
            local = self.extract_og_image(article_url)
            if local:
                return local

        # 3. Check local verified artist photos
        hl_lower = headline.lower()
        artist_map = {
            "seedhe maut": "seedhe_maut.jpg",
            "tbsm": "seedhe_maut.jpg",
            "calm": "seedhe_maut.jpg",
            "encore": "seedhe_maut.jpg",
            "hanumankind": "hanumankind.jpg",
            "big dawgs": "hanumankind.jpg",
            "kalmi": "hanumankind.jpg",
            "divine": "divine.jpg",
            "gully gang": "divine.jpg",
            "59": "divine.jpg",
            "stan": "mc_stan.jpg",
            "p-town": "mc_stan.jpg",
            "raftaar": "raftaar.jpg",
            "kalamkaar": "raftaar.jpg",
            "prabh": "prabh_deep.jpg",
            "brodha": "brodha_v.jpg",
            "emiway": "emiway.jpg"
        }
        for kw, filename in artist_map.items():
            if kw in hl_lower:
                p = self.artists_dir / filename
                if p.exists() and p.stat().st_size > 1000:
                    return str(p)

        # 4. Search online
        online_pic = self.search_wikipedia_image(headline)
        if online_pic:
            return online_pic

        # Fallback to Seedhe Maut or Hanumankind photo as high-quality default DHH press shot
        default_seedhe = self.artists_dir / "seedhe_maut.jpg"
        if default_seedhe.exists():
            return str(default_seedhe)

        return None

image_fetcher = ImageFetcher()

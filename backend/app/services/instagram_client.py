import hmac
import hashlib
import uuid
import time
from pathlib import Path
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.app.config import settings

class InstagramAPIClient:
    """
    Official Meta Instagram Graph API Client.
    Supports both Live Meta Graph API (v21.0) and high-fidelity Mock Mode for offline dry-runs.
    """
    GRAPH_API_VERSION = "v21.0"
    GRAPH_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(self, mock_mode: Optional[bool] = None):
        self.mock_mode = settings.INSTAGRAM_MOCK_MODE if mock_mode is None else mock_mode
        self.access_token = settings.ACCESS_TOKEN
        self.ig_account_id = settings.INSTAGRAM_ACCOUNT_ID
        self.app_id = settings.META_APP_ID
        self.app_secret = settings.META_APP_SECRET

    def _resolve_public_url(self, path_or_url: str, default_folder: str = "memes") -> str:
        """Converts local file paths into publicly accessible URLs for Meta Graph API."""
        if not path_or_url:
            return ""
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        filename = Path(path_or_url).name
        base = settings.PUBLIC_MEDIA_URL_BASE.rstrip("/")
        if "reels" in path_or_url or filename.endswith(".mp4"):
            subfolder = "reels"
        elif "stories" in path_or_url:
            subfolder = "stories"
        elif "covers" in path_or_url:
            subfolder = "covers"
        else:
            subfolder = "memes"
        return f"{base}/{subfolder}/{filename}"

    async def verify_connection(self, access_token: Optional[str] = None, ig_account_id: Optional[str] = None) -> Dict[str, Any]:
        """Test Instagram account connectivity and verify granted permissions."""
        token = access_token or self.access_token
        acc_id = ig_account_id or self.ig_account_id

        if self.mock_mode or not token:
            return {
                "success": True,
                "mode": "MOCK_SIMULATION" if self.mock_mode else "UNCONFIGURED_MOCK",
                "account_id": acc_id or "mock_dhh_1784140001",
                "username": "desihiphop_vibes",
                "account_type": "BUSINESS",
                "profile_picture_url": "https://picsum.photos/seed/dhh/200/200",
                "followers_count": 14250,
                "follows_count": 284,
                "media_count": 158,
                "permissions_status": {
                    "instagram_basic": True,
                    "instagram_content_publish": True,
                    "instagram_manage_comments": True,
                    "instagram_manage_insights": True,
                    "pages_show_list": True,
                    "pages_read_engagement": True
                },
                "token_valid": True,
                "expires_in_days": 58,
                "message": "Connected in Mock / Dry-Run Mode. All Instagram API endpoints faithfully emulated."
            }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Fetch user profile
                url = f"{self.GRAPH_URL}/{acc_id}?fields=id,username,name,profile_picture_url,followers_count,follows_count,media_count&access_token={token}"
                res = await client.get(url)
                if res.status_code != 200:
                    return {
                        "success": False,
                        "mode": "LIVE_GRAPH_API",
                        "error": res.json().get("error", {}).get("message", "Failed to fetch account info")
                    }
                data = res.json()

                # 2. Check token permissions (supports Page Tokens and User Tokens via debug_token)
                granted = []
                debug_url = f"{self.GRAPH_URL}/debug_token?input_token={token}&access_token={token}"
                debug_res = await client.get(debug_url)
                if debug_res.status_code == 200:
                    granted = debug_res.json().get("data", {}).get("scopes", [])

                if not granted:
                    perm_url = f"{self.GRAPH_URL}/me/permissions?access_token={token}"
                    perm_res = await client.get(perm_url)
                    if perm_res.status_code == 200:
                        for p in perm_res.json().get("data", []):
                            if p.get("status") == "granted":
                                granted.append(p.get("permission"))

                required = [
                    "instagram_basic", "instagram_content_publish",
                    "instagram_manage_comments", "instagram_manage_insights"
                ]
                missing = [p for p in required if p not in granted]

                return {
                    "success": True,
                    "mode": "LIVE_GRAPH_API",
                    "account_id": data.get("id"),
                    "username": data.get("username"),
                    "followers_count": data.get("followers_count", 0),
                    "media_count": data.get("media_count", 0),
                    "permissions_granted": granted,
                    "missing_permissions": missing,
                    "token_valid": True,
                    "message": "Connected to Meta Instagram Graph API." if not missing else f"Connected, but missing permissions: {', '.join(missing)}"
                }
        except Exception as e:
            return {
                "success": False,
                "mode": "LIVE_GRAPH_API",
                "error": str(e)
            }

    async def publish_image_post(self, image_url: str, caption: str) -> Dict[str, Any]:
        """Publish a single image post to Instagram."""
        return await self._publish_image_internal(image_url, caption)

    async def publish_image(self, image_url: str, caption: str) -> Dict[str, Any]:
        """Alias for publish_image_post."""
        return await self._publish_image_internal(image_url, caption)

    async def _publish_image_internal(self, image_url: str, caption: str) -> Dict[str, Any]:
        if self.mock_mode or not self.access_token:
            mock_id = f"1789{int(time.time())}{uuid.uuid4().hex[:4]}"
            return {
                "success": True,
                "mode": "MOCK",
                "post_id": mock_id,
                "container_id": f"cont_{mock_id}",
                "permalink": f"https://www.instagram.com/p/{uuid.uuid4().hex[:10]}/",
                "status": "PUBLISHED",
                "published_at": datetime.utcnow().isoformat()
            }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resolved_url = self._resolve_public_url(image_url, "memes")
                # Step 1: Create Media Container
                create_url = f"{self.GRAPH_URL}/{self.ig_account_id}/media"
                payload = {
                    "image_url": resolved_url,
                    "caption": caption,
                    "access_token": self.access_token
                }
                res = await client.post(create_url, data=payload)
                if res.status_code != 200:
                    return {"success": False, "error": res.json().get("error", {})}
                container_id = res.json().get("id")

                # Step 2: Publish Container (Wait 4s for Meta CDN to fetch & encode)
                import asyncio
                await asyncio.sleep(4)
                publish_url = f"{self.GRAPH_URL}/{self.ig_account_id}/media_publish"
                pub_payload = {
                    "creation_id": container_id,
                    "access_token": self.access_token
                }
                pub_res = await client.post(publish_url, data=pub_payload)
                if pub_res.status_code != 200:
                    return {"success": False, "error": pub_res.json().get("error", {})}
                
                post_id = pub_res.json().get("id")

                # Fetch real permalink from Graph API
                permalink = ""
                try:
                    p_res = await client.get(f"{self.GRAPH_URL}/{post_id}?fields=permalink&access_token={self.access_token}")
                    if p_res.status_code == 200:
                        permalink = p_res.json().get("permalink", "")
                except Exception:
                    pass

                return {
                    "success": True,
                    "post_id": post_id,
                    "container_id": container_id,
                    "permalink": permalink,
                    "status": "PUBLISHED",
                    "published_at": datetime.utcnow().isoformat()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def publish_carousel_post(self, image_urls: List[str], caption: str) -> Dict[str, Any]:
        """Publish a multi-image carousel post."""
        if self.mock_mode or not self.access_token:
            mock_id = f"1792{int(time.time())}{uuid.uuid4().hex[:4]}"
            return {
                "success": True,
                "mode": "MOCK",
                "post_id": mock_id,
                "permalink": f"https://www.instagram.com/p/{uuid.uuid4().hex[:10]}/",
                "slides_count": len(image_urls),
                "status": "PUBLISHED"
            }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 1. Create item containers
                child_ids = []
                for img_url in image_urls:
                    item_url = f"{self.GRAPH_URL}/{self.ig_account_id}/media"
                    r = await client.post(item_url, data={
                        "image_url": img_url,
                        "is_carousel_item": "true",
                        "access_token": self.access_token
                    })
                    if r.status_code == 200:
                        child_ids.append(r.json().get("id"))

                # 2. Create Carousel Container
                car_url = f"{self.GRAPH_URL}/{self.ig_account_id}/media"
                c_res = await client.post(car_url, data={
                    "media_type": "CAROUSEL",
                    "children": ",".join(child_ids),
                    "caption": caption,
                    "access_token": self.access_token
                })
                container_id = c_res.json().get("id")

                # 3. Publish
                pub_res = await client.post(f"{self.GRAPH_URL}/{self.ig_account_id}/media_publish", data={
                    "creation_id": container_id,
                    "access_token": self.access_token
                })
                return {
                    "success": True,
                    "post_id": pub_res.json().get("id"),
                    "container_id": container_id,
                    "status": "PUBLISHED"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def publish_reel(self, video_url: str, caption: str, cover_url: Optional[str] = None) -> Dict[str, Any]:
        """Publish a 9:16 vertical video Reel."""
        if self.mock_mode or not self.access_token:
            mock_id = f"1795{int(time.time())}{uuid.uuid4().hex[:4]}"
            return {
                "success": True,
                "mode": "MOCK",
                "post_id": mock_id,
                "permalink": f"https://www.instagram.com/reel/{uuid.uuid4().hex[:10]}/",
                "media_type": "REELS",
                "status": "PUBLISHED"
            }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                resolved_video = self._resolve_public_url(video_url, "reels")
                resolved_cover = self._resolve_public_url(cover_url, "covers") if cover_url else None
                # 1. Create Reels Container
                payload = {
                    "media_type": "REELS",
                    "video_url": resolved_video,
                    "caption": caption,
                    "share_to_feed": "true",
                    "access_token": self.access_token
                }
                if resolved_cover:
                    payload["cover_url"] = resolved_cover

                res = await client.post(f"{self.GRAPH_URL}/{self.ig_account_id}/media", data=payload)
                if res.status_code != 200:
                    return {"success": False, "error": res.json().get("error", {})}
                container_id = res.json().get("id")

                # 2. Poll until upload & encoding finish (Meta needs up to 30s)
                for _ in range(12):
                    time.sleep(3)
                    status_res = await client.get(f"{self.GRAPH_URL}/{container_id}?fields=status_code&access_token={self.access_token}")
                    status_code = status_res.json().get("status_code")
                    if status_code == "FINISHED":
                        break
                    elif status_code == "ERROR":
                        return {"success": False, "error": "Meta Reel processing error"}

                # 3. Publish
                pub_res = await client.post(f"{self.GRAPH_URL}/{self.ig_account_id}/media_publish", data={
                    "creation_id": container_id,
                    "access_token": self.access_token
                })
                return {
                    "success": True,
                    "post_id": pub_res.json().get("id"),
                    "status": "PUBLISHED"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def publish_story(self, image_url: str) -> Dict[str, Any]:
        """Publish a 9:16 Story to Instagram."""
        if self.mock_mode or not self.access_token:
            mock_id = f"1798{int(time.time())}{uuid.uuid4().hex[:4]}"
            return {
                "success": True,
                "mode": "MOCK",
                "post_id": mock_id,
                "media_type": "STORIES",
                "status": "PUBLISHED"
            }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resolved_story = self._resolve_public_url(image_url, "stories")
                payload = {
                    "media_type": "STORIES",
                    "image_url": resolved_story,
                    "access_token": self.access_token
                }
                res = await client.post(f"{self.GRAPH_URL}/{self.ig_account_id}/media", data=payload)
                if res.status_code != 200:
                    return {"success": False, "error": res.json().get("error", {})}
                container_id = res.json().get("id")

                pub_res = await client.post(f"{self.GRAPH_URL}/{self.ig_account_id}/media_publish", data={
                    "creation_id": container_id,
                    "access_token": self.access_token
                })
                return {
                    "success": True,
                    "post_id": pub_res.json().get("id"),
                    "status": "PUBLISHED"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def fetch_media_insights(self, ig_post_id: str, post_type: str = "IMAGE") -> Dict[str, Any]:
        """Fetch reach, impressions, likes, comments, shares, saves from Instagram."""
        if self.mock_mode or not self.access_token:
            import random
            reach = random.randint(3500, 18500)
            shares = int(reach * random.uniform(0.04, 0.12))
            saves = int(reach * random.uniform(0.05, 0.14))
            return {
                "reach": reach,
                "impressions": int(reach * 1.35),
                "likes": int(reach * random.uniform(0.08, 0.22)),
                "comments": random.randint(12, 180),
                "shares": shares,
                "saves": saves,
                "views": reach * 2 if post_type == "REEL" else 0,
                "share_to_reach_ratio": round(shares / max(1, reach), 3),
                "saves_to_reach_ratio": round(saves / max(1, reach), 3)
            }

        try:
            metrics = "impressions,reach,saved"
            if post_type == "REEL":
                metrics = "plays,reach,saved,shares,total_interactions"

            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.GRAPH_URL}/{ig_post_id}/insights?metric={metrics}&access_token={self.access_token}"
                res = await client.get(url)
                if res.status_code != 200:
                    return {"reach": 0, "impressions": 0, "likes": 0, "comments": 0, "shares": 0, "saves": 0}
                data = res.json().get("data", [])
                result = {}
                for item in data:
                    name = item.get("name")
                    val = item.get("values", [{}])[0].get("value", 0)
                    result[name] = val
                return result
        except Exception:
            return {"reach": 0, "impressions": 0, "likes": 0, "comments": 0, "shares": 0, "saves": 0}

    async def post_comment_reply(self, ig_comment_id: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a comment on the page's own post."""
        if self.mock_mode or not self.access_token:
            return {
                "success": True,
                "mode": "MOCK",
                "reply_id": f"rep_{int(time.time())}",
                "status": "SENT"
            }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.GRAPH_URL}/{ig_comment_id}/replies"
                res = await client.post(url, data={
                    "message": reply_text,
                    "access_token": self.access_token
                })
                if res.status_code == 200:
                    return {"success": True, "reply_id": res.json().get("id")}
                return {"success": False, "error": res.json().get("error", {})}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_webhook_signature(self, payload: bytes, signature_header: str) -> bool:
        """Validate Meta webhook X-Hub-Signature-256 HMAC."""
        if not self.app_secret or not signature_header:
            return False
        expected = "sha256=" + hmac.new(
            self.app_secret.encode("utf-8"),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature_header)

instagram_client = InstagramAPIClient()

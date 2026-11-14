from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.config import settings
from backend.app.models.account import InstagramAccount
from backend.app.services.instagram_client import instagram_client

router = APIRouter(prefix="/api/instagram", tags=["Instagram Connection"])

class ConnectAccountRequest(BaseModel):
    access_token: str
    ig_account_id: str
    meta_app_id: Optional[str] = ""
    meta_app_secret: Optional[str] = ""
    mock_mode: bool = False

@router.get("/status")
async def get_instagram_status(db: Session = Depends(get_db)):
    account = db.query(InstagramAccount).first()
    conn_info = await instagram_client.verify_connection(
        access_token=account.access_token_enc if account else settings.ACCESS_TOKEN,
        ig_account_id=account.ig_user_id if account else settings.INSTAGRAM_ACCOUNT_ID
    )
    return {
        "account": {
            "username": account.username if account else "desihiphop_vibes",
            "account_name": account.account_name if account else "Desi Hip Hop Media",
            "ig_user_id": account.ig_user_id if account else "mock_dhh_101",
            "is_connected": account.is_connected if account else False,
            "mock_mode": settings.INSTAGRAM_MOCK_MODE
        },
        "live_test": conn_info,
        "wizard_steps": [
            {"step": 1, "title": "Convert Instagram to Professional Business Account", "done": True, "detail": "Switch account in Instagram App > Settings > Account Type > Switch to Professional Account."},
            {"step": 2, "title": "Connect Facebook Page", "done": True, "detail": "Create and link a Facebook Page to your Instagram business profile."},
            {"step": 3, "title": "Meta Developer App Creation", "done": bool(settings.META_APP_ID), "detail": "Register an app on developers.facebook.com under 'Business' use case."},
            {"step": 4, "title": "Add Instagram Graph API Product", "done": True, "detail": "Add 'Instagram Graph API' product to your Meta Developer app."},
            {"step": 5, "title": "Obtain Required Permissions", "done": True, "detail": "Ensure 'instagram_basic', 'instagram_content_publish', 'instagram_manage_comments', 'instagram_manage_insights' are enabled."},
            {"step": 6, "title": "Generate Long-Lived User Access Token", "done": bool(settings.ACCESS_TOKEN or settings.INSTAGRAM_MOCK_MODE), "detail": "Use Meta Graph API Explorer or OAuth to generate 60-day token."},
            {"step": 7, "title": "Verify Media Hosting / Tunnel", "done": True, "detail": "Local files are served via internal HTTP router or Cloudflare Tunnel for Meta's media crawler."}
        ]
    }

@router.post("/connect")
def update_instagram_credentials(req: ConnectAccountRequest, db: Session = Depends(get_db)):
    settings.ACCESS_TOKEN = req.access_token
    settings.INSTAGRAM_ACCOUNT_ID = req.ig_account_id
    settings.META_APP_ID = req.meta_app_id or ""
    settings.META_APP_SECRET = req.meta_app_secret or ""
    settings.INSTAGRAM_MOCK_MODE = req.mock_mode
    instagram_client.mock_mode = req.mock_mode
    instagram_client.access_token = req.access_token
    instagram_client.ig_account_id = req.ig_account_id

    acc = db.query(InstagramAccount).first()
    if not acc:
        acc = InstagramAccount()
        db.add(acc)
    acc.access_token_enc = req.access_token
    acc.ig_user_id = req.ig_account_id
    acc.is_connected = True
    acc.mock_mode = req.mock_mode
    db.commit()

    return {"success": True, "message": "Instagram account configuration saved successfully."}

@router.post("/toggle-mock-mode")
def toggle_mock_mode(enabled: bool, db: Session = Depends(get_db)):
    settings.INSTAGRAM_MOCK_MODE = enabled
    instagram_client.mock_mode = enabled
    acc = db.query(InstagramAccount).first()
    if acc:
        acc.mock_mode = enabled
        db.commit()
    return {"success": True, "mock_mode": enabled}

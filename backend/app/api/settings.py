from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.app.config import settings
from backend.app.services.scheduler_engine import scheduler_engine

router = APIRouter(prefix="/api/settings", tags=["General Settings"])

class UpdateSettingsRequest(BaseModel):
    daily_image_target: Optional[int] = None
    daily_reels_target: Optional[int] = None
    daily_stories_target: Optional[int] = None
    timezone: Optional[str] = None
    auto_publish: Optional[bool] = None
    allow_remote: Optional[bool] = None

@router.get("")
def get_settings():
    return {
        "daily_image_target": scheduler_engine.daily_image_target,
        "daily_reels_target": scheduler_engine.daily_reels_target,
        "daily_stories_target": scheduler_engine.daily_stories_target,
        "timezone": settings.TIMEZONE,
        "auto_publish_enabled": scheduler_engine.auto_publish,
        "emergency_stop": scheduler_engine.emergency_stop,
        "host": settings.HOST,
        "port": settings.PORT,
        "allow_remote_access": settings.ALLOW_REMOTE_ACCESS,
        "media_storage_path": str(settings.MEDIA_DIR),
        "database_url": settings.DATABASE_URL
    }

@router.post("")
def update_settings(req: UpdateSettingsRequest):
    if req.daily_image_target is not None:
        scheduler_engine.daily_image_target = req.daily_image_target
        settings.DAILY_IMAGE_POSTS_TARGET = req.daily_image_target
    if req.daily_reels_target is not None:
        scheduler_engine.daily_reels_target = req.daily_reels_target
        settings.DAILY_REELS_TARGET = req.daily_reels_target
    if req.daily_stories_target is not None:
        scheduler_engine.daily_stories_target = req.daily_stories_target
        settings.DAILY_STORIES_TARGET = req.daily_stories_target
    if req.auto_publish is not None:
        scheduler_engine.auto_publish = req.auto_publish
    if req.timezone:
        settings.TIMEZONE = req.timezone
    return {"success": True, "message": "Settings updated successfully."}

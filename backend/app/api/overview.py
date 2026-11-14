import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.content import PublishedPost, PublishingQueue, GeneratedContent
from backend.app.models.comments import CommentRecord, ReplyRecord
from backend.app.services.scheduler_engine import scheduler_engine
from backend.app.services.ai_engine import ai_engine
from backend.app.services.instagram_client import instagram_client

router = APIRouter(prefix="/api/overview", tags=["Overview"])

@router.get("")
async def get_overview_dashboard(db: Session = Depends(get_db)):
    """Fetch high-level KPIs, system health status, and live feeds."""
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Today's counts
    published_today_posts = db.query(PublishedPost).filter(
        PublishedPost.published_at >= today_start,
        PublishedPost.post_type == "IMAGE"
    ).count()

    published_today_reels = db.query(PublishedPost).filter(
        PublishedPost.published_at >= today_start,
        PublishedPost.post_type == "REEL"
    ).count()

    published_today_stories = db.query(PublishedPost).filter(
        PublishedPost.published_at >= today_start,
        PublishedPost.post_type == "STORY"
    ).count()

    total_published_all = db.query(PublishedPost).count()
    pending_queue_count = db.query(PublishingQueue).filter(PublishingQueue.status == "QUEUED").count()
    failed_jobs_count = db.query(PublishingQueue).filter(PublishingQueue.status == "FAILED").count()

    # Aggregate reach & engagement
    all_published = db.query(PublishedPost).all()
    total_reach = sum(p.reach or 0 for p in all_published)
    total_likes = sum(p.likes or 0 for p in all_published)
    total_comments = sum(p.comments or 0 for p in all_published)
    total_shares = sum(p.shares or 0 for p in all_published)
    total_saves = sum(p.saves or 0 for p in all_published)

    # Recent Comments & Replies
    recent_comments = db.query(CommentRecord).order_by(CommentRecord.created_at.desc()).limit(5).all()
    recent_replies = db.query(ReplyRecord).order_by(ReplyRecord.sent_at.desc()).limit(5).all()

    # System Statuses
    ai_status = await ai_engine.check_ollama_status()
    ig_status = await instagram_client.verify_connection()

    return {
        "today_stats": {
            "posts_published": published_today_posts,
            "posts_target": scheduler_engine.daily_image_target,
            "reels_published": published_today_reels,
            "reels_target": scheduler_engine.daily_reels_target,
            "stories_published": published_today_stories,
            "stories_target": scheduler_engine.daily_stories_target
        },
        "totals": {
            "published_all": total_published_all,
            "pending_queue": pending_queue_count,
            "failed_jobs": failed_jobs_count,
            "total_reach": total_reach,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_saves": total_saves
        },
        "system_status": {
            "automation_active": scheduler_engine.auto_publish and not scheduler_engine.emergency_stop,
            "emergency_stopped": scheduler_engine.emergency_stop,
            "scheduler_running": scheduler_engine.is_running,
            "ai_engine": ai_status,
            "instagram_api": ig_status
        },
        "recent_comments": [
            {
                "id": c.id,
                "username": c.username,
                "text": c.text,
                "classification": c.classification,
                "sentiment": c.sentiment,
                "is_replied": c.is_replied,
                "created_at": c.created_at.isoformat()
            } for c in recent_comments
        ],
        "recent_replies": [
            {
                "id": r.id,
                "reply_text": r.reply_text,
                "status": r.status,
                "sent_at": r.sent_at.isoformat()
            } for r in recent_replies
        ]
    }

@router.post("/start")
async def start_automation():
    scheduler_engine.resume()
    return {"success": True, "message": "Automation resumed."}

@router.post("/pause")
async def pause_automation():
    scheduler_engine.pause()
    return {"success": True, "message": "Automation paused."}

@router.post("/emergency-stop")
async def emergency_stop():
    scheduler_engine.trigger_emergency_stop()
    return {"success": True, "message": "EMERGENCY STOP ACTIVATED. All publishing halted immediately."}

@router.post("/generate-now")
async def generate_now():
    """Trigger immediate generation cycle."""
    scheduler_engine.autonomous_content_generation_loop()
    return {"success": True, "message": "Generation cycle triggered."}

import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from backend.app.database import get_db
from backend.app.models.content import PublishingQueue, GeneratedContent, PublishedPost
from backend.app.services.instagram_client import instagram_client

router = APIRouter(prefix="/api/queue", tags=["Publishing Queue & Calendar"])

class RescheduleRequest(BaseModel):
    scheduled_for: datetime.datetime
    priority: Optional[int] = 1

@router.get("")
def get_queue(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PublishingQueue)
    if status:
        query = query.filter(PublishingQueue.status == status)
    jobs = query.order_by(PublishingQueue.scheduled_for.asc()).all()

    result = []
    for j in jobs:
        content = db.query(GeneratedContent).filter(GeneratedContent.id == j.content_id).first()
        result.append({
            "id": j.id,
            "content_id": j.content_id,
            "scheduled_for": j.scheduled_for.isoformat(),
            "priority": j.priority,
            "retry_count": j.retry_count,
            "status": j.status,
            "last_error": j.last_error,
            "content": {
                "title": content.title if content else "Untitled",
                "content_type": content.content_type if content else "IMAGE",
                "caption": content.caption if content else "",
                "media_path": content.media_path if content else ""
            } if content else None
        })
    return result

@router.get("/calendar")
def get_calendar_events(db: Session = Depends(get_db)):
    """Return scheduled, published, and failed events formatted for calendar visualization."""
    queued = db.query(PublishingQueue).all()
    published = db.query(PublishedPost).all()

    events = []
    for q in queued:
        content = db.query(GeneratedContent).filter(GeneratedContent.id == q.content_id).first()
        events.append({
            "id": f"queue_{q.id}",
            "title": f"[{content.content_type if content else 'POST'}] {content.title if content else 'Queued Item'}",
            "start": q.scheduled_for.isoformat(),
            "status": q.status,
            "type": "QUEUE",
            "content_type": content.content_type if content else "IMAGE"
        })

    for p in published:
        events.append({
            "id": f"pub_{p.id}",
            "title": f"✓ [{p.post_type}] {p.caption[:30]}...",
            "start": p.published_at.isoformat(),
            "status": "PUBLISHED",
            "type": "PUBLISHED",
            "content_type": p.post_type
        })

    return events

@router.post("/{job_id}/publish-now")
async def publish_job_now(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PublishingQueue).filter(PublishingQueue.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Queue item not found")

    content = db.query(GeneratedContent).filter(GeneratedContent.id == job.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    res = None
    if content.content_type == "IMAGE":
        res = await instagram_client.publish_image_post(content.media_path, content.caption)
    elif content.content_type == "REEL":
        res = await instagram_client.publish_reel(content.media_path, content.caption, content.cover_path)
    elif content.content_type == "STORY":
        res = await instagram_client.publish_story(content.media_path)

    if res and res.get("success"):
        job.status = "PUBLISHED"
        job.executed_at = datetime.datetime.utcnow()
        content.status = "PUBLISHED"
        content.published_at = datetime.datetime.utcnow()
        content.post_id = res.get("post_id")

        pub = PublishedPost(
            content_id=content.id,
            ig_post_id=res.get("post_id"),
            post_type=content.content_type,
            permalink=res.get("permalink", ""),
            caption=content.caption,
            published_at=datetime.datetime.utcnow()
        )
        db.add(pub)
        db.commit()
        return {"success": True, "post_id": res.get("post_id")}
    else:
        job.status = "FAILED"
        job.last_error = str(res.get("error", "Failed") if res else "No response")
        db.commit()
        return {"success": False, "error": job.last_error}

@router.delete("/{job_id}")
def cancel_queue_item(job_id: int, db: Session = Depends(get_db)):
    job = db.query(PublishingQueue).filter(PublishingQueue.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    job.status = "CANCELLED"
    db.commit()
    return {"success": True}

@router.api_route("/tick", methods=["GET", "POST"])
def autonomous_cron_tick(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Heartbeat and autonomous execution endpoint called by cloud cron (GitHub Actions / Uptime pinger).
    1. Responds immediately (< 5ms) with HTTP 200 to prevent any timeout.
    2. Runs due queue processing and buffer replenishment asynchronously in background tasks.
    """
    from backend.app.services.scheduler_engine import scheduler_engine
    
    now = datetime.datetime.utcnow()
    pending = db.query(PublishingQueue).filter(PublishingQueue.status == "QUEUED").count()
    due = db.query(PublishingQueue).filter(
        PublishingQueue.status == "QUEUED",
        PublishingQueue.scheduled_for <= now
    ).count()
    
    # Schedule background jobs without blocking HTTP response
    from backend.app.services.scheduler_engine import trim_process_memory
    background_tasks.add_task(scheduler_engine.process_due_queue_jobs)
    background_tasks.add_task(scheduler_engine.autonomous_content_generation_loop)
    background_tasks.add_task(trim_process_memory)
    
    return {
        "status": "OK",
        "action": "AUTONOMOUS_TICK_EXECUTED",
        "timestamp": now.isoformat(),
        "pending_in_queue": pending,
        "due_count": due
    }

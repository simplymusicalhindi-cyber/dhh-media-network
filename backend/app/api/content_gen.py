import datetime
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.content import GeneratedContent, ContentIdea
from backend.app.services.scheduler_engine import scheduler_engine
from backend.app.services.ai_engine import ai_engine

router = APIRouter(prefix="/api/content", tags=["Content Generator"])

class GenerateMemeRequest(BaseModel):
    category: Optional[str] = None
    topic: Optional[str] = None
    auto_enqueue: bool = True

class GenerateReelRequest(BaseModel):
    topic: Optional[str] = None
    auto_enqueue: bool = True

class GenerateStoryRequest(BaseModel):
    auto_enqueue: bool = True

@router.post("/generate-meme")
async def generate_meme_endpoint(req: GenerateMemeRequest, db: Session = Depends(get_db)):
    content = await scheduler_engine.autonomous_generate_meme(db, category=req.category)
    if req.auto_enqueue:
        sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        scheduler_engine.enqueue_content(db, content.id, sched_time)
    return {
        "success": True,
        "content_id": content.id,
        "title": content.title,
        "caption": content.caption,
        "media_path": content.media_path,
        "quality_score": content.quality_score,
        "status": content.status
    }

@router.post("/generate-reel")
async def generate_reel_endpoint(req: GenerateReelRequest, db: Session = Depends(get_db)):
    content = await scheduler_engine.autonomous_generate_reel(db, topic=req.topic)
    if req.auto_enqueue:
        sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        scheduler_engine.enqueue_content(db, content.id, sched_time)
    return {
        "success": True,
        "content_id": content.id,
        "title": content.title,
        "caption": content.caption,
        "media_path": content.media_path,
        "cover_path": content.cover_path,
        "quality_score": content.quality_score,
        "status": content.status
    }

@router.post("/generate-story")
async def generate_story_endpoint(req: GenerateStoryRequest, db: Session = Depends(get_db)):
    content = await scheduler_engine.autonomous_generate_story(db)
    if req.auto_enqueue:
        sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        scheduler_engine.enqueue_content(db, content.id, sched_time)
    return {
        "success": True,
        "content_id": content.id,
        "title": content.title,
        "media_path": content.media_path,
        "quality_score": content.quality_score,
        "status": content.status
    }

@router.get("/list")
def list_generated_content(
    content_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = 30,
    db: Session = Depends(get_db)
):
    query = db.query(GeneratedContent)
    if content_type:
        query = query.filter(GeneratedContent.content_type == content_type)
    if status:
        query = query.filter(GeneratedContent.status == status)
    items = query.order_by(GeneratedContent.created_at.desc()).limit(limit).all()
    return items

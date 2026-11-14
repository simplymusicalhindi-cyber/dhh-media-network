from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.research import TopicRecord, ArtistRecord, CollabOutreachDraft
from backend.app.services.research_engine import research_engine
from backend.app.services.growth_learning_engine import growth_learning_engine

router = APIRouter(prefix="/api/growth", tags=["Audience Growth"])

class OutreachRequest(BaseModel):
    artist_name: str
    artist_handle: str

@router.get("/topics")
def get_topics(db: Session = Depends(get_db)):
    return research_engine.discover_fresh_topics(db)

@router.get("/artists")
def get_artists(db: Session = Depends(get_db)):
    research_engine.seed_initial_topics(db)
    return db.query(ArtistRecord).all()

@router.get("/posting-windows")
def get_posting_windows():
    return growth_learning_engine.OPTIMAL_POSTING_WINDOWS_IST

@router.get("/outreach-drafts")
def get_outreach_drafts(db: Session = Depends(get_db)):
    return db.query(CollabOutreachDraft).order_by(CollabOutreachDraft.created_at.desc()).all()

@router.post("/outreach")
def create_outreach(req: OutreachRequest, db: Session = Depends(get_db)):
    draft = research_engine.generate_collab_outreach(db, req.artist_name, req.artist_handle)
    return {"success": True, "draft": draft}

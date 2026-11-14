from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.seo_engine import seo_engine
from backend.app.models.seo import BioProfileRecommendation

router = APIRouter(prefix="/api/seo", tags=["SEO Manager"])

class OptimizeCaptionRequest(BaseModel):
    hook: str
    body: str
    cta: Optional[str] = "Tag your friends and follow for more DHH memes!"
    category: Optional[str] = "MEMES_HUMOR"

class SaveBioRequest(BaseModel):
    username_suggestion: str
    display_name: str
    bio_text: str
    category_tag: str
    call_to_action: str

@router.post("/optimize-caption")
def optimize_caption(req: OptimizeCaptionRequest):
    return seo_engine.generate_optimized_caption(
        hook=req.hook,
        body=req.body,
        cta=req.cta or "",
        category=req.category or "MEMES_HUMOR"
    )

@router.get("/keywords")
def get_keywords():
    return {
        "primary": seo_engine.PRIMARY_DHH_KEYWORDS,
        "clusters": seo_engine.HASHTAG_CLUSTERS
    }

@router.get("/bios")
def get_bios(db: Session = Depends(get_db)):
    bios = db.query(BioProfileRecommendation).all()
    if not bios:
        presets = seo_engine.generate_bio_recommendations()
        for p in presets:
            b = BioProfileRecommendation(
                username_suggestion=p["username_suggestion"],
                display_name=p["display_name"],
                bio_text=p["bio_text"],
                category_tag=p["category"],
                call_to_action=p["cta"],
                strategy_notes=p["strategy_notes"]
            )
            db.add(b)
        db.commit()
        bios = db.query(BioProfileRecommendation).all()
    return bios

@router.post("/bios/save")
def save_bio(req: SaveBioRequest, db: Session = Depends(get_db)):
    bio = BioProfileRecommendation(
        username_suggestion=req.username_suggestion,
        display_name=req.display_name,
        bio_text=req.bio_text,
        category_tag=req.category_tag,
        call_to_action=req.call_to_action,
        strategy_notes="User custom profile strategy",
        is_active=True
    )
    db.add(bio)
    db.commit()
    db.refresh(bio)
    return {"success": True, "bio_id": bio.id}

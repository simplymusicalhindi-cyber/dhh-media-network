from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.meme_engine import meme_engine
from backend.app.services.dhh_knowledge import DHH_MEME_PRESETS

router = APIRouter(prefix="/api/memes", tags=["Meme Studio"])

class CustomMemeRequest(BaseModel):
    template: str = "TWEET_CARD_STYLE"  # TWEET_CARD_STYLE or SPLIT_COMPARISON
    hook: str
    body_text: str
    punchline: Optional[str] = ""
    category: str = "DHH_MEME"

@router.get("/templates")
def get_meme_templates():
    return [
        {
            "id": "TWEET_CARD_STYLE",
            "name": "Twitter / X Dark Card (1:1)",
            "description": "High engagement tweet card with handle @desihiphop_vibes, verified badge, and punchline footer."
        },
        {
            "id": "SPLIT_COMPARISON",
            "name": "Split Comparison (Expectation vs Reality)",
            "description": "2-panel comparison card comparing rapper/producer plans against DHH reality."
        }
    ]

@router.get("/presets")
def get_meme_presets():
    return DHH_MEME_PRESETS

@router.post("/render")
def render_custom_meme(req: CustomMemeRequest):
    if req.template == "SPLIT_COMPARISON":
        parts = req.body_text.split("---")
        top = parts[0].strip() if len(parts) > 0 else req.body_text
        bottom = parts[1].strip() if len(parts) > 1 else "Bhai sab change ho gaya."
        res = meme_engine.create_split_comparison_meme(
            title=req.hook,
            top_situation=top,
            bottom_situation=bottom,
            punchline=req.punchline or "DHH is unpredictable 💀"
        )
    else:
        res = meme_engine.create_tweet_card_meme(
            hook=req.hook,
            content_text=req.body_text,
            punchline=req.punchline,
            category=req.category
        )
    return {"success": True, "result": res}

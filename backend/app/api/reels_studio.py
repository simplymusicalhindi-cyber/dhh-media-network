from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.app.services.reels_engine import reels_engine
from backend.app.services.dhh_knowledge import DHH_REEL_SCRIPTS

router = APIRouter(prefix="/api/reels", tags=["Reels Studio"])

class CustomReelRequest(BaseModel):
    title: str
    hook: str
    scenes: List[Dict[str, Any]]
    punchline: str

@router.get("/templates")
def get_reel_templates():
    return [
        {"id": "POV_COMEDY", "name": "POV Comedy Skit (9:16)", "description": "3-act relatable situation breakdown with countdown punchline."},
        {"id": "PRODUCER_STRUGGLE", "name": "Producer vs Rapper Dynamic", "description": "Audio stem disaster breakdown with 808 beat drop."},
        {"id": "FAN_EVOLUTION", "name": "Fan Evolution Stages", "description": "Progression stages from casual listener to hardcore DHH connoisseur."}
    ]

@router.get("/presets")
def get_reel_presets():
    return DHH_REEL_SCRIPTS

@router.post("/render")
def render_custom_reel(req: CustomReelRequest):
    res = reels_engine.render_reel(
        title=req.title,
        hook=req.hook,
        scenes=req.scenes,
        punchline=req.punchline
    )
    return {"success": True, "result": res}

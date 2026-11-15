from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sqlite3

from backend.app.services.reels_engine import reels_engine
from backend.app.services.reel_engine import reel_engine
from backend.app.services.template_finder import template_finder
from backend.app.services.dhh_knowledge import DHH_REEL_SCRIPTS
from backend.app.config import settings

router = APIRouter(prefix="/api/reels", tags=["Reels Studio"])

class CustomReelRequest(BaseModel):
    title: str
    hook: str
    scenes: List[Dict[str, Any]]
    punchline: str

class AutonomousReelRequest(BaseModel):
    meme_text: str
    custom_name: Optional[str] = None

@router.get("/templates/catalog")
def get_template_catalog():
    """Retrieve full catalog of dynamically discovered reel video templates."""
    conn = sqlite3.connect(settings.DATA_DIR / "dhh_media.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("SELECT * FROM reel_templates ORDER BY use_count ASC, id DESC").fetchall()
    conn.close()
    return {"total": len(rows), "templates": [dict(r) for r in rows]}

@router.post("/templates/discover")
def trigger_daily_template_discovery(background_tasks: BackgroundTasks):
    """Trigger autonomous multi-source template discovery (Instagram + YouTube Shorts)."""
    background_tasks.add_task(template_finder.run_daily_discovery)
    return {
        "status": "QUEUED",
        "message": "Autonomous template discovery started in background. New templates will be added to catalog and synced automatically."
    }

@router.post("/render-autonomous")
def render_autonomous_fresh_reel(req: AutonomousReelRequest):
    """Render a clean meme reel using the freshest, least-used template from the catalog."""
    res = reel_engine.render_autonomous_reel(meme_text=req.meme_text, custom_out_name=req.custom_name)
    return {"success": True, "result": res}

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

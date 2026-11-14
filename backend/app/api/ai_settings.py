from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.app.config import settings
from backend.app.services.ai_engine import ai_engine

router = APIRouter(prefix="/api/ai", tags=["AI Settings"])

class AIConfigRequest(BaseModel):
    ollama_base_url: Optional[str] = None
    ollama_model: Optional[str] = None
    min_quality_score: Optional[float] = None

class TestInferenceRequest(BaseModel):
    prompt: str = "Seedhe Maut TBSM vibe meme"

@router.get("/status")
async def get_ai_status():
    status = await ai_engine.check_ollama_status()
    return {
        "ollama": status,
        "config": {
            "base_url": settings.OLLAMA_BASE_URL,
            "model": settings.OLLAMA_MODEL,
            "min_quality_score": settings.MIN_QUALITY_SCORE,
            "template_fallback_enabled": settings.AI_FALLBACK_TO_TEMPLATES
        }
    }

@router.post("/config")
def update_ai_config(req: AIConfigRequest):
    if req.ollama_base_url:
        settings.OLLAMA_BASE_URL = req.ollama_base_url
        ai_engine.base_url = req.ollama_base_url
    if req.ollama_model:
        settings.OLLAMA_MODEL = req.ollama_model
        ai_engine.model = req.ollama_model
    if req.min_quality_score is not None:
        settings.MIN_QUALITY_SCORE = req.min_quality_score
        ai_engine.min_quality_score = req.min_quality_score
    return {"success": True, "message": "AI settings updated successfully."}

@router.post("/test-inference")
async def test_inference(req: TestInferenceRequest):
    result = await ai_engine.generate_meme_idea(topic=req.prompt)
    return {"success": True, "result": result}

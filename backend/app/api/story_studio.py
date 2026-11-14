from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.app.services.story_engine import story_engine
from backend.app.services.dhh_knowledge import DHH_STORY_TEMPLATES

router = APIRouter(prefix="/api/stories", tags=["Story Studio"])

class CustomStoryRequest(BaseModel):
    story_type: str = "GUESS_THE_RAPPER"
    title: str
    clue: str
    options: List[str]
    call_to_action: str

@router.get("/templates")
def get_story_templates():
    return [
        {"id": "GUESS_THE_RAPPER", "name": "Guess the Rapper from Bars"},
        {"id": "THIS_OR_THAT", "name": "This or That DHH Showdown"},
        {"id": "COMPLETE_THE_LYRICS", "name": "Complete the Lyrics Challenge"},
        {"id": "PRODUCER_TRIVIA", "name": "DHH Producer Trivia"}
    ]

@router.get("/presets")
def get_story_presets():
    return DHH_STORY_TEMPLATES

@router.post("/render")
def render_custom_story(req: CustomStoryRequest):
    res = story_engine.create_story_graphic(
        story_type=req.story_type,
        title=req.title,
        clue=req.clue,
        options=req.options,
        call_to_action=req.call_to_action
    )
    return {"success": True, "result": res}

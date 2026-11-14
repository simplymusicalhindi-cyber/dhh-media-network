from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.comments import CommentRecord, ReplyRecord
from backend.app.services.comment_engine import comment_engine

router = APIRouter(prefix="/api/comments", tags=["Comment Manager"])

class ManualReplyRequest(BaseModel):
    reply_text: str

class SimulateCommentRequest(BaseModel):
    post_id: str = "mock_post_101"
    username: str = "underground_emcee"
    comment_text: str = "Bhai seedhe maut wala meme literally meri life hai 😭"

@router.get("")
def list_comments(limit: int = 50, db: Session = Depends(get_db)):
    comments = db.query(CommentRecord).order_by(CommentRecord.created_at.desc()).limit(limit).all()
    result = []
    for c in comments:
        replies = db.query(ReplyRecord).filter(ReplyRecord.comment_id == c.id).all()
        result.append({
            "id": c.id,
            "ig_comment_id": c.ig_comment_id,
            "post_id": c.post_id,
            "username": c.username,
            "text": c.text,
            "classification": c.classification,
            "sentiment": c.sentiment,
            "is_replied": c.is_replied,
            "created_at": c.created_at.isoformat(),
            "replies": [{"text": r.reply_text, "status": r.status, "sent_at": r.sent_at.isoformat()} for r in replies]
        })
    return result

@router.post("/{comment_id}/reply")
async def send_reply(comment_id: int, req: ManualReplyRequest, db: Session = Depends(get_db)):
    res = await comment_engine.process_manual_reply(db, comment_id, req.reply_text)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@router.post("/toggle-auto-reply")
def toggle_auto(enabled: bool):
    comment_engine.toggle_auto_reply(enabled)
    return {"success": True, "auto_reply_enabled": comment_engine.auto_reply_enabled}

@router.post("/simulate-incoming")
async def simulate_comment(req: SimulateCommentRequest, db: Session = Depends(get_db)):
    import uuid
    mock_id = f"c_{uuid.uuid4().hex[:8]}"
    record = await comment_engine.ingest_comment(
        db=db,
        ig_comment_id=mock_id,
        post_id=req.post_id,
        username=req.username,
        text=req.comment_text
    )
    return {"success": True, "comment_id": record.id, "classification": record.classification, "is_replied": record.is_replied}

import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.models.comments import CommentRecord, ReplyRecord
from backend.app.services.ai_engine import ai_engine
from backend.app.services.instagram_client import instagram_client

class CommentEngine:
    def __init__(self):
        self.auto_reply_enabled = True

    def toggle_auto_reply(self, enabled: bool):
        self.auto_reply_enabled = enabled

    async def ingest_comment(
        self,
        db: Session,
        ig_comment_id: str,
        post_id: str,
        username: str,
        text: str
    ) -> CommentRecord:
        """Ingest incoming Instagram comment, classify it, and determine reply eligibility."""
        existing = db.query(CommentRecord).filter(CommentRecord.ig_comment_id == ig_comment_id).first()
        if existing:
            return existing

        classification_res = await ai_engine.classify_and_reply_comment(text)

        record = CommentRecord(
            ig_comment_id=ig_comment_id,
            post_id=post_id,
            username=username,
            text=text,
            sentiment=classification_res["sentiment"],
            classification=classification_res["classification"],
            confidence=0.92,
            is_replied=False,
            created_at=datetime.datetime.utcnow()
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # Autonomous reply if enabled and eligible
        if self.auto_reply_enabled and classification_res["should_reply"] and not settings.EMERGENCY_STOP:
            # Check hourly limit
            one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
            replies_in_last_hour = db.query(ReplyRecord).filter(ReplyRecord.sent_at >= one_hour_ago).count()

            if replies_in_last_hour < settings.MAX_AUTO_REPLIES_PER_HOUR:
                reply_text = classification_res["reply_text"]
                res = await instagram_client.post_comment_reply(ig_comment_id, reply_text)

                reply_record = ReplyRecord(
                    comment_id=record.id,
                    ig_reply_id=res.get("reply_id"),
                    reply_text=reply_text,
                    status="SENT" if res.get("success") else "FAILED",
                    error_message=str(res.get("error", "")),
                    sent_at=datetime.datetime.utcnow()
                )
                db.add(reply_record)
                record.is_replied = True
                db.commit()

        return record

    async def process_manual_reply(self, db: Session, comment_id: int, custom_reply_text: str) -> Dict[str, Any]:
        """Manually send a reply to any comment from the dashboard."""
        comment = db.query(CommentRecord).filter(CommentRecord.id == comment_id).first()
        if not comment:
            return {"success": False, "error": "Comment not found"}

        res = await instagram_client.post_comment_reply(comment.ig_comment_id, custom_reply_text)
        reply_record = ReplyRecord(
            comment_id=comment.id,
            ig_reply_id=res.get("reply_id"),
            reply_text=custom_reply_text,
            status="SENT" if res.get("success") else "FAILED",
            error_message=str(res.get("error", "")),
            sent_at=datetime.datetime.utcnow()
        )
        db.add(reply_record)
        comment.is_replied = True
        db.commit()
        return {"success": True, "reply_id": res.get("reply_id")}

comment_engine = CommentEngine()

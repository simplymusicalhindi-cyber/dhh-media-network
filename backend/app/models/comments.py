from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from backend.app.database import Base

class CommentRecord(Base):
    __tablename__ = "comment_records"

    id = Column(Integer, primary_key=True, index=True)
    ig_comment_id = Column(String(100), unique=True, index=True)
    post_id = Column(String(100), index=True)
    username = Column(String(150), default="dhh_fan")
    text = Column(Text, nullable=False)
    sentiment = Column(String(50), default="POSITIVE")  # POSITIVE, NEUTRAL, NEGATIVE
    classification = Column(String(100), default="FUNNY")
    # POSITIVE, FUNNY, QUESTION, ARTIST_DISCUSSION, MUSIC_REC, SPAM, ABUSE, SENSITIVE, TROLL
    confidence = Column(Float, default=0.9)
    is_replied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReplyRecord(Base):
    __tablename__ = "reply_records"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, index=True)
    ig_reply_id = Column(String(100), nullable=True)
    reply_text = Column(Text, nullable=False)
    status = Column(String(50), default="SENT")  # GENERATED, SENT, FAILED, SKIPPED
    error_message = Column(Text, default="")
    sent_at = Column(DateTime, default=datetime.utcnow)

class AutoReplyRule(Base):
    __tablename__ = "auto_reply_rules"

    id = Column(Integer, primary_key=True, index=True)
    trigger_keyword = Column(String(100), nullable=False)
    classification_filter = Column(String(100), default="ALL")
    reply_template = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)

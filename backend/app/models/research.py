from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from backend.app.database import Base

class TopicRecord(Base):
    __tablename__ = "topic_records"

    id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(255), nullable=False)
    category = Column(String(100), default="CURRENT_RELEASES")
    source = Column(String(100), default="RADAR_RSS")
    relevance_score = Column(Float, default=9.0)
    popularity_score = Column(Float, default=8.5)
    summary = Column(Text, default="")
    content_ideas_json = Column(Text, default="[]")
    verification_status = Column(String(50), default="VERIFIED")  # VERIFIED, UNVERIFIED, EXPIRED
    discovered_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

class ArtistRecord(Base):
    __tablename__ = "artist_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    alias = Column(String(150), default="")
    scene = Column(String(100), default="DELHI")  # DELHI, MUMBAI, PUNJAB, SOUTH, UNDERGROUND, PRODUCER
    tags = Column(String(255), default="bars,hardcore,lyrical")
    discography_highlights = Column(Text, default="")
    collab_potential_score = Column(Float, default=8.0)
    notes = Column(Text, default="")

class CollabOutreachDraft(Base):
    __tablename__ = "collab_outreach_drafts"

    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(150), nullable=False)
    artist_handle = Column(String(100), default="")
    outreach_pitch = Column(Text, nullable=False)
    personalized_hook = Column(Text, nullable=False)
    angle = Column(String(100), default="BEHIND_THE_BARS")
    status = Column(String(50), default="DRAFT")  # DRAFT, APPROVED, SENT
    created_at = Column(DateTime, default=datetime.utcnow)

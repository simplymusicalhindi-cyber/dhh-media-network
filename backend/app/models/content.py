from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class ContentIdea(Base):
    __tablename__ = "content_ideas"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, nullable=True)
    category = Column(String(100), default="PRODUCER_STRUGGLES")
    # Categories: RELATABLE_MEME, RAPPER_MEME, PRODUCER_MEME, STUDIO_LIFE, INDEPENDENT_STRUGGLE,
    # FAN_WARS, DHH_REFERENCES, RELEASES_TRENDS, YOUTH_HUMOUR, POV_MEMES, UNDERGROUND_JOKES, MUSIC_INDUSTRY_SATIRE
    hook = Column(String(255), nullable=False)
    punchline = Column(Text, nullable=False)
    context = Column(Text, default="")
    quality_score = Column(Float, default=8.0)
    originality_score = Column(Float, default=8.5)
    humour_score = Column(Float, default=8.0)
    relatability_score = Column(Float, default=9.0)
    dhh_tags = Column(String(255), default="dhh,producer,beats")
    format_target = Column(String(50), default="IMAGE")  # IMAGE, CAROUSEL, REEL, STORY
    status = Column(String(50), default="DRAFT")  # DRAFT, APPROVED, REJECTED, USED
    created_at = Column(DateTime, default=datetime.utcnow)

class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), nullable=False)
    media_type = Column(String(50), default="IMAGE")  # IMAGE, VIDEO, AUDIO
    width = Column(Integer, default=1080)
    height = Column(Integer, default=1080)
    duration = Column(Float, default=0.0)
    file_size = Column(Integer, default=0)
    public_url = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("content_ideas.id"), nullable=True)
    content_type = Column(String(50), default="IMAGE")  # IMAGE, CAROUSEL, REEL, STORY
    title = Column(String(255), nullable=False)
    caption = Column(Text, nullable=False)
    hashtags = Column(Text, default="#DHH #DesiHipHop #IndianHipHop")
    alt_text = Column(Text, default="")
    seo_score = Column(Float, default=9.0)
    media_path = Column(String(500), default="")
    cover_path = Column(String(500), default="")
    media_ids_json = Column(Text, default="[]")
    quality_score = Column(Float, default=8.5)
    status = Column(String(50), default="READY")  # READY, QUEUED, PUBLISHED, FAILED
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    post_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PublishingQueue(Base):
    __tablename__ = "publishing_queue"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_contents.id"), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    priority = Column(Integer, default=1)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    last_error = Column(Text, default="")
    status = Column(String(50), default="QUEUED")  # QUEUED, PROCESSING, PUBLISHED, FAILED, CANCELLED
    idempotency_key = Column(String(150), unique=True, index=True)
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PublishedPost(Base):
    __tablename__ = "published_posts"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("generated_contents.id"), nullable=False)
    ig_post_id = Column(String(100), unique=True, index=True)
    post_type = Column(String(50), default="IMAGE")  # IMAGE, CAROUSEL, REEL, STORY
    permalink = Column(String(500), default="")
    caption = Column(Text, default="")
    published_at = Column(DateTime, default=datetime.utcnow)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    views = Column(Integer, default=0)
    retention_score = Column(Float, default=0.0)
    last_synced_at = Column(DateTime, default=datetime.utcnow)

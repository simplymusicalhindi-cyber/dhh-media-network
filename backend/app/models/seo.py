from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from backend.app.database import Base

class SEOMetadata(Base):
    __tablename__ = "seo_metadata"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, index=True)
    primary_keywords = Column(Text, default="Desi Hip Hop, Indian Rap, DHH Memes")
    secondary_keywords = Column(Text, default="Underground Rap, Indian Beatmakers, Gully Rap")
    hashtags = Column(Text, default="#DHH #IndianHipHop #DesiHipHop #SeedheMaut #KR$NA")
    alt_text = Column(Text, default="")
    hook_strength_score = Column(Float, default=8.8)
    created_at = Column(DateTime, default=datetime.utcnow)

class KeywordRecord(Base):
    __tablename__ = "keyword_records"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(150), unique=True, index=True)
    category = Column(String(100), default="CORE_DHH")
    monthly_search_volume_est = Column(Integer, default=50000)
    relevance_score = Column(Float, default=9.5)
    last_used_at = Column(DateTime, nullable=True)

class BioProfileRecommendation(Base):
    __tablename__ = "bio_profile_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    username_suggestion = Column(String(100), default="dhh_bars_daily")
    display_name = Column(String(150), default="Desi Hip Hop Cult | DHH Memes & Culture")
    bio_text = Column(Text, default="⚡ The raw heartbeat of Indian Hip-Hop.\n🎤 Relatable memes, producer pain & underground bars.\n👇 Drop your heat in DMs!")
    category_tag = Column(String(100), default="Musician/Band / Media News")
    call_to_action = Column(String(200), default="Stream underground DHH tracks via link below")
    strategy_notes = Column(Text, default="Optimized for Instagram search terms: 'Desi Hip Hop', 'DHH', 'Indian Rap'")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

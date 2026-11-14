from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Date
from backend.app.database import Base

class DailyMetrics(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(Date, unique=True, index=True)
    total_posts = Column(Integer, default=0)
    total_reels = Column(Integer, default=0)
    total_stories = Column(Integer, default=0)
    total_reach = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_saves = Column(Integer, default=0)
    net_followers_gain = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class CategoryPerformance(Base):
    __tablename__ = "category_performance"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), unique=True, index=True)
    count_published = Column(Integer, default=0)
    avg_reach = Column(Float, default=0.0)
    avg_shares = Column(Float, default=0.0)
    avg_saves = Column(Float, default=0.0)
    share_to_reach_ratio = Column(Float, default=0.0)
    saves_to_reach_ratio = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

class WeeklyLearningReport(Base):
    __tablename__ = "weekly_learning_reports"

    id = Column(Integer, primary_key=True, index=True)
    week_start = Column(Date, nullable=False)
    summary = Column(Text, nullable=False)
    top_performing_formats = Column(Text, default="[]")
    top_topics = Column(Text, default="[]")
    recommended_strategy_shifts = Column(Text, default="[]")
    applied = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

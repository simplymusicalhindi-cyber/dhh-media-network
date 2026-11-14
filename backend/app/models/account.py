from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from backend.app.database import Base

class InstagramAccount(Base):
    __tablename__ = "instagram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), default="desihiphop_vibes")
    account_name = Column(String(150), default="Desi Hip Hop Media")
    ig_user_id = Column(String(100), default="mock_ig_user_101")
    page_id = Column(String(100), default="mock_fb_page_202")
    access_token_enc = Column(Text, default="")
    token_type = Column(String(50), default="BEARER")
    expires_at = Column(DateTime, nullable=True)
    is_business = Column(Boolean, default=True)
    is_connected = Column(Boolean, default=False)
    permissions_granted = Column(Text, default="instagram_basic,instagram_content_publish,instagram_manage_comments,instagram_manage_insights,pages_show_list,pages_read_engagement")
    last_tested_at = Column(DateTime, nullable=True)
    mock_mode = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

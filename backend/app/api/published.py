from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database import get_db
from backend.app.models.content import PublishedPost, GeneratedContent

router = APIRouter(prefix="/api/published", tags=["Published Content"])

@router.get("")
def get_published_content(post_type: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(PublishedPost)
    if post_type:
        query = query.filter(PublishedPost.post_type == post_type)
    posts = query.order_by(PublishedPost.published_at.desc()).limit(limit).all()

    result = []
    for p in posts:
        content = db.query(GeneratedContent).filter(GeneratedContent.id == p.content_id).first()
        result.append({
            "id": p.id,
            "ig_post_id": p.ig_post_id,
            "post_type": p.post_type,
            "permalink": p.permalink,
            "caption": p.caption,
            "published_at": p.published_at.isoformat(),
            "reach": p.reach,
            "impressions": p.impressions,
            "likes": p.likes,
            "comments": p.comments,
            "shares": p.shares,
            "saves": p.saves,
            "media_path": content.media_path if content else ""
        })
    return result

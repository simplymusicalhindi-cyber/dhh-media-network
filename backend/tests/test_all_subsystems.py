import pytest
import datetime
from pathlib import Path
from backend.app.database import SessionLocal, Base, engine
from backend.app.models import (
    InstagramAccount, GeneratedContent, PublishingQueue,
    PublishedPost, CommentRecord, ReplyRecord
)
from backend.app.services.ai_engine import ai_engine
from backend.app.services.meme_engine import meme_engine
from backend.app.services.story_engine import story_engine
from backend.app.services.reels_engine import reels_engine
from backend.app.services.instagram_client import instagram_client
from backend.app.services.comment_engine import comment_engine
from backend.app.services.seo_engine import seo_engine
from backend.app.services.growth_learning_engine import growth_learning_engine
from backend.app.services.reliability_engine import reliability_engine
from backend.app.services.backup_engine import backup_engine

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_database_connection(db):
    account = db.query(InstagramAccount).first()
    assert account is not None
    assert account.username == "desihiphop_vibes"

@pytest.mark.asyncio
async def test_ai_engine_and_quality_scoring():
    meme_idea = await ai_engine.generate_meme_idea()
    assert "hook" in meme_idea
    assert "top_text" in meme_idea
    assert "quality_score" in meme_idea
    assert meme_idea["quality_score"] >= 7.0

def test_meme_rendering():
    res = meme_engine.create_tweet_card_meme(
        hook="Test DHH Hook 💀",
        content_text="Rapper recorded on EarPods.\nProducer crying in 32-bit float.",
        punchline="Mix master ho gaya lala",
        category="PRODUCER_MEME"
    )
    assert Path(res["file_path"]).exists()
    assert res["width"] == 1080
    assert res["height"] == 1080

def test_story_rendering():
    res = story_engine.create_story_graphic(
        story_type="GUESS_THE_RAPPER",
        title="GUESS THE RAPPER",
        clue="Kaanch ke ghar mein baith ke...",
        options=["A) KR$NA", "B) Karma"],
        call_to_action="Drop answer in DM!"
    )
    assert Path(res["file_path"]).exists()
    assert res["width"] == 1080
    assert res["height"] == 1920

def test_reels_rendering():
    scenes = [
        {"duration": 1.5, "text": "Part 1: Scene setup"},
        {"duration": 1.5, "text": "Part 2: Twist"}
    ]
    res = reels_engine.render_reel(
        title="Test Reel",
        hook="When 808 hits",
        scenes=scenes,
        punchline="Speakers destroyed 💀"
    )
    assert Path(res["video_path"]).exists()
    assert Path(res["cover_path"]).exists()
    assert res["width"] == 1080
    assert res["height"] == 1920
    assert res["file_size"] > 1000

@pytest.mark.asyncio
async def test_mock_instagram_api():
    conn = await instagram_client.verify_connection()
    assert conn["success"] is True

    pub_img = await instagram_client.publish_image_post("dummy_url", "Test caption")
    assert pub_img["success"] is True
    assert "post_id" in pub_img

    pub_reel = await instagram_client.publish_reel("dummy_video", "Test reel", "dummy_cover")
    assert pub_reel["success"] is True

    pub_story = await instagram_client.publish_story("dummy_story")
    assert pub_story["success"] is True

    insights = await instagram_client.fetch_media_insights(pub_img["post_id"])
    assert insights["reach"] > 0

@pytest.mark.asyncio
async def test_comment_engine(db):
    test_comment = "Bhai literally meri life hai ye meme haha 😂"
    rec = await comment_engine.ingest_comment(
        db=db,
        ig_comment_id="test_comm_101",
        post_id="test_post_202",
        username="dhh_fan_boy",
        text=test_comment
    )
    assert rec.classification == "FUNNY"
    assert rec.sentiment == "POSITIVE"

def test_seo_and_growth_engine(db):
    caption = seo_engine.generate_optimized_caption("Top 808 Trap Drops", "Breakdown of the scene", "Tag your friends", "PRODUCER")
    assert "caption" in caption
    assert len(caption["hashtags"].split()) >= 3

    report = growth_learning_engine.generate_weekly_learning_report(db)
    assert report is not None
    assert "Weekly Performance Review" in report.summary

def test_reliability_and_backup(db):
    health = reliability_engine.check_all_subsystems(db)
    assert health["overall_status"] in ["HEALTHY", "DEGRADED"]
    assert "database" in health["subsystems"]

    backup = backup_engine.create_database_backup(db, "Test backup snapshot")
    assert Path(backup.backup_path).exists()
    assert backup.file_size_bytes > 0

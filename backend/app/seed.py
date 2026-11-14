import datetime
import random
from backend.app.database import SessionLocal, Base, engine
from backend.app.models import (
    InstagramAccount, ContentIdea, GeneratedContent, PublishingQueue,
    PublishedPost, CommentRecord, ReplyRecord, TopicRecord, ArtistRecord,
    CategoryPerformance, WeeklyLearningReport, DailyMetrics
)
from backend.app.services.dhh_knowledge import DHH_ARTISTS, DHH_MEME_PRESETS, DHH_REEL_SCRIPTS
from backend.app.services.meme_engine import meme_engine
from backend.app.services.story_engine import story_engine
from backend.app.services.growth_learning_engine import growth_learning_engine

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Instagram Account
        acc = db.query(InstagramAccount).first()
        if not acc:
            acc = InstagramAccount(
                username="desihiphop_vibes",
                account_name="Desi Hip Hop Media Cult",
                ig_user_id="mock_dhh_101",
                page_id="mock_fb_page_202",
                is_business=True,
                is_connected=True,
                mock_mode=True,
                permissions_granted="instagram_basic,instagram_content_publish,instagram_manage_comments,instagram_manage_insights,pages_show_list,pages_read_engagement",
                last_tested_at=datetime.datetime.utcnow()
            )
            db.add(acc)
            db.commit()

        # 2. Pre-generate some memes and publish them
        if db.query(PublishedPost).count() == 0:
            print("Seeding initial published posts, memes, and reels...")
            categories = ["PRODUCER_MEMES", "STUDIO_LIFE", "RELATABLE_DHH", "RAPPER_MEMES", "POV_MEMES"]

            for i, cat in enumerate(categories):
                preset = random.choice(DHH_MEME_PRESETS)
                meme_res = meme_engine.create_tweet_card_meme(
                    hook=preset["hook"],
                    content_text=f"{preset['top_text']}\n\n{preset['bottom_text']}",
                    punchline=preset.get("punchline"),
                    category=cat
                )

                content = GeneratedContent(
                    content_type="IMAGE",
                    title=f"{cat}: {preset['hook'][:35]}",
                    caption=preset["caption"],
                    hashtags="#DHH #DesiHipHop #IndianHipHop",
                    alt_text=f"Desi Hip-Hop meme: {preset['hook']}",
                    seo_score=9.3,
                    media_path=meme_res["file_path"],
                    quality_score=9.1,
                    status="PUBLISHED",
                    published_at=datetime.datetime.utcnow() - datetime.timedelta(days=i, hours=2),
                    post_id=f"179{100000000 + i}"
                )
                db.add(content)
                db.commit()

                # Add published post
                reach = random.randint(4500, 19500)
                shares = int(reach * random.uniform(0.06, 0.15))
                saves = int(reach * random.uniform(0.05, 0.13))
                pub = PublishedPost(
                    content_id=content.id,
                    ig_post_id=content.post_id,
                    post_type="IMAGE",
                    permalink=f"https://www.instagram.com/p/C{1000 + i}/",
                    caption=content.caption,
                    published_at=content.published_at,
                    reach=reach,
                    impressions=int(reach * 1.4),
                    likes=int(reach * 0.16),
                    comments=random.randint(24, 160),
                    shares=shares,
                    saves=saves,
                    views=0
                )
                db.add(pub)
                db.commit()

            # Seed a sample Story
            story_res = story_engine.create_story_graphic(
                story_type="GUESS_THE_RAPPER",
                title="GUESS THE RAPPER 🔍",
                clue="Bars: 'Kaanch ke ghar mein baith ke patthar mat phenko'\nKnown for cold punchlines & multi-syllabic rhymes.",
                options=["A) KR$NA", "B) Karma", "C) Seedhe Maut", "D) Brodha V"],
                call_to_action="Drop A, B, C or D in DMs! 🔥"
            )
            story_content = GeneratedContent(
                content_type="STORY",
                title="STORY: Guess The Rapper #1",
                caption="Daily DHH Trivia Story",
                hashtags="#DHHStory",
                alt_text="Interactive story card",
                seo_score=9.0,
                media_path=story_res["file_path"],
                quality_score=9.2,
                status="PUBLISHED",
                published_at=datetime.datetime.utcnow() - datetime.timedelta(hours=4),
                post_id="story_mock_991"
            )
            db.add(story_content)
            db.commit()

            story_pub = PublishedPost(
                content_id=story_content.id,
                ig_post_id="story_mock_991",
                post_type="STORY",
                permalink="https://www.instagram.com/stories/desihiphop_vibes/",
                caption=story_content.caption,
                published_at=story_content.published_at,
                reach=3200,
                impressions=3800,
                likes=420,
                comments=85,
                shares=110,
                saves=45
            )
            db.add(story_pub)
            db.commit()

        # 3. Seed sample fan comments
        if db.query(CommentRecord).count() == 0:
            sample_comments = [
                ("dhh_enthusiast", "Bhai literally meri life hai 😭 FL Studio 10 bar crash hua aaj", "FUNNY", "Bhai tu hi toh iss meme ka real inspiration hai 😂🙌"),
                ("producer_karan", "Exposure se mera electricity bill nahi bharata lala 💀", "FUNNY", "Shoutout se ration nahi aata lala 😭 Tag karo aise artists ko!"),
                ("underground_bars", "Underground scene deserves more attention and real support.", "ARTIST_DISCUSSION", "Facts bhai, underground is where the real hunger lives 🔥 Keep supporting the scene!"),
                ("beatmaker_sam", "Which audio interface is best for 808 sub mixing?", "QUESTION", "Focusrite Scarlett or Motu M2 are solid starters for clean low-end monitoring! 🎧"),
                ("tbsm_fan4life", "TBSM on top forever! Rawest energy in Asia.", "POSITIVE", "TBSM4L! Terko Bhi Sab Milega fam ⚡")
            ]
            for user, txt, cls, reply_txt in sample_comments:
                import uuid
                c = CommentRecord(
                    ig_comment_id=f"c_{uuid.uuid4().hex[:8]}",
                    post_id="179100000000",
                    username=user,
                    text=txt,
                    sentiment="POSITIVE",
                    classification=cls,
                    confidence=0.95,
                    is_replied=True,
                    created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(1, 12))
                )
                db.add(c)
                db.commit()

                r = ReplyRecord(
                    comment_id=c.id,
                    ig_reply_id=f"r_{uuid.uuid4().hex[:8]}",
                    reply_text=reply_txt,
                    status="SENT",
                    sent_at=c.created_at + datetime.timedelta(minutes=3)
                )
                db.add(r)
                db.commit()

        # 4. Aggregate learning metrics
        growth_learning_engine.aggregate_category_performance(db)
        growth_learning_engine.generate_weekly_learning_report(db)

        # 5. Populate Daily Metrics for charts
        today = datetime.date.today()
        for d in range(14, -1, -1):
            day_date = today - datetime.timedelta(days=d)
            if not db.query(DailyMetrics).filter(DailyMetrics.metric_date == day_date).first():
                base_reach = 8000 + (14 - d) * 600 + random.randint(-500, 1200)
                metric = DailyMetrics(
                    metric_date=day_date,
                    total_posts=random.randint(8, 12),
                    total_reels=random.randint(4, 6),
                    total_stories=random.randint(1, 3),
                    total_reach=base_reach,
                    total_impressions=int(base_reach * 1.38),
                    total_likes=int(base_reach * 0.14),
                    total_comments=random.randint(45, 180),
                    total_shares=int(base_reach * 0.08),
                    total_saves=int(base_reach * 0.07),
                    net_followers_gain=random.randint(35, 140),
                    avg_engagement_rate=round(random.uniform(7.8, 11.5), 1)
                )
                db.add(metric)
        db.commit()
        print("Database seeded with sample DHH content, comments, and analytics!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

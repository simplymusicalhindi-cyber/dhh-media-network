import datetime
import uuid
import os
import gc
import ctypes
from typing import Dict, Any, List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.database import SessionLocal
from backend.app.models.content import ContentIdea, GeneratedContent, PublishingQueue, PublishedPost
from backend.app.models.analytics import DailyMetrics
from backend.app.services.ai_engine import ai_engine
from backend.app.services.meme_engine import meme_engine
from backend.app.services.reel_engine import reel_engine
from backend.app.services.story_engine import story_engine
from backend.app.services.seo_engine import seo_engine
from backend.app.services.instagram_client import instagram_client
from backend.app.services.reliability_engine import reliability_engine
from backend.app.services.review_engine import review_engine

def trim_process_memory():
    """Explicitly triggers Python garbage collection and returns free heap memory back to the OS."""
    gc.collect()
    try:
        if hasattr(ctypes, "CDLL"):
            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
    except Exception:
        pass

class SchedulerEngine:
    def __init__(self):
        try:
            self.scheduler = BackgroundScheduler(timezone=settings.TIMEZONE)
        except Exception:
            self.scheduler = BackgroundScheduler(timezone="UTC")
        self.is_running = False
        self.daily_image_target = settings.DAILY_IMAGE_POSTS_TARGET
        self.daily_reels_target = settings.DAILY_REELS_TARGET
        self.daily_stories_target = settings.DAILY_STORIES_TARGET
        self.auto_publish = settings.AUTO_PUBLISH_ENABLED
        self.emergency_stop = settings.EMERGENCY_STOP

    def start(self):
        """Start the persistent autonomous scheduler."""
        if not self.is_running:
            # 1. Check queue and publish due jobs every 60 seconds
            self.scheduler.add_job(
                self.process_due_queue_jobs,
                trigger=IntervalTrigger(seconds=60),
                id="dhh_queue_processor",
                replace_existing=True
            )
            # 2. Autonomous generation check (runs every 15 minutes only on non-Render workers)
            is_render = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or os.getenv("IS_RENDER"))
            if not is_render:
                self.scheduler.add_job(
                    self.autonomous_content_generation_loop,
                    trigger=IntervalTrigger(minutes=15),
                    id="dhh_content_generator",
                    replace_existing=True
                )
            else:
                print("[Scheduler] Running on Render: in-container generation loop disabled to guarantee <120MB RAM stability. Publishing queue is active.", flush=True)
            # 3. Insights and metrics sync (every 2 hours)
            self.scheduler.add_job(
                self.sync_insights,
                trigger=IntervalTrigger(hours=2),
                id="dhh_insights_sync",
                replace_existing=True
            )
            self.scheduler.start()
            self.is_running = True

    def pause(self):
        """Pause automated publishing."""
        self.auto_publish = False

    def resume(self):
        """Resume automated publishing."""
        self.auto_publish = True
        self.emergency_stop = False

    def trigger_emergency_stop(self):
        """Immediate full stop of all publishing operations."""
        self.auto_publish = False
        self.emergency_stop = True

    def update_targets(self, image_target: int, reels_target: int, stories_target: int):
        self.daily_image_target = image_target
        self.daily_reels_target = reels_target
        self.daily_stories_target = stories_target

    async def autonomous_generate_meme(self, db: Session, category: Optional[str] = None) -> GeneratedContent:
        """Autonomously research, create visual, optimize SEO, and store a DHH meme post."""
        idea_dict = await ai_engine.generate_meme_idea(category=category)

        # Render visual using authentic human visual meme templates
        layout = meme_engine.create_human_meme(
            hook=idea_dict["hook"],
            content_text=f"{idea_dict['top_text']}\n\n{idea_dict['bottom_text']}",
            punchline=idea_dict.get("punchline"),
            category=idea_dict["category"]
        )

        # Optimize SEO & Caption
        seo_res = seo_engine.generate_optimized_caption(
            hook=idea_dict["hook"],
            body=f"{idea_dict['top_text']}\n{idea_dict['bottom_text']}\n{idea_dict.get('punchline', '')}",
            cta="Tag that one friend who relates 💀👇 Follow @azpadhai for daily DHH culture!",
            category=idea_dict["category"]
        )

        # Pre-publish human-grade quality review
        review = review_engine.review_content(
            title=idea_dict["hook"],
            text=f"{idea_dict['top_text']} {idea_dict['bottom_text']} {idea_dict.get('punchline', '')}",
            media_path=layout["file_path"],
            content_type="IMAGE"
        )

        content = GeneratedContent(
            content_type="IMAGE",
            title=f"{idea_dict['category']}: {idea_dict['hook'][:40]}",
            caption=seo_res["caption"],
            hashtags=seo_res["hashtags"],
            alt_text=idea_dict.get("alt_text", "Desi Hip-Hop meme"),
            seo_score=seo_res["seo_score"],
            media_path=layout["file_path"],
            quality_score=review["overall_score"],
            status="READY",
            created_at=datetime.datetime.utcnow()
        )
        db.add(content)
        db.commit()
        db.refresh(content)
        return content

    async def autonomous_generate_reel(self, db: Session, topic: Optional[str] = None) -> Optional[GeneratedContent]:
        """Autonomously script, select authentic DHH template, render 9:16 vertical video with non-overlapping text, and store Reel."""
        is_render = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or os.getenv("IS_RENDER"))
        if is_render:
            print("[Render Web Tier] Skipping in-container FFmpeg reel generation to maintain <150MB memory footprint. Reels are rendered by GitHub Actions runner (7GB RAM).", flush=True)
            return None

        reel_dict = await ai_engine.generate_reel_concept(topic=topic)
        hook_text = reel_dict.get("hook", "When the DHH beat drops at 3 AM")

        # Render MP4 video via authentic DHH template engine
        render_res = reel_engine.render_autonomous_reel(meme_text=hook_text)

        # SEO Caption
        seo_res = seo_engine.generate_optimized_caption(
            hook=hook_text,
            body=f"{reel_dict.get('title', 'DHH Culture Reel')}\nWatch till the end for the real breakdown 🤯",
            cta="Do you agree? Drop your thoughts below! 👇🔥 #DesiHipHop",
            category="REELS"
        )

        content = GeneratedContent(
            content_type="REEL",
            title=f"REEL: {reel_dict.get('title', hook_text[:35])}",
            caption=seo_res["caption"],
            hashtags=seo_res["hashtags"],
            alt_text=f"Desi Hip-Hop vertical reel: {hook_text}",
            seo_score=seo_res["seo_score"],
            media_path=render_res["file_path"],
            cover_path=None,
            quality_score=reel_dict.get("quality_score", 9.0),
            status="READY",
            created_at=datetime.datetime.utcnow()
        )
        db.add(content)
        db.commit()
        db.refresh(content)
        trim_process_memory()
        return content

    async def autonomous_generate_story(self, db: Session) -> GeneratedContent:
        """Autonomously render and store interactive 9:16 Story card."""
        story_dict = await ai_engine.generate_story_concept()

        render_res = story_engine.create_story_graphic(
            story_type=story_dict["type"],
            title=story_dict["title"],
            clue=story_dict["clue"],
            options=story_dict.get("options", []),
            call_to_action=story_dict["call_to_action"]
        )

        content = GeneratedContent(
            content_type="STORY",
            title=f"STORY: {story_dict['title']}",
            caption=f"{story_dict['title']} - Daily DHH Quiz",
            hashtags="#DHHStory",
            alt_text="Interactive Desi Hip-Hop story card",
            seo_score=9.0,
            media_path=render_res["file_path"],
            quality_score=9.2,
            status="READY",
            created_at=datetime.datetime.utcnow()
        )
        db.add(content)
        db.commit()
        db.refresh(content)
        return content

    def enqueue_content(self, db: Session, content_id: int, scheduled_for: datetime.datetime) -> PublishingQueue:
        """Add ready content to the persistent publishing queue with idempotency token."""
        idem_key = f"pub_{content_id}_{int(scheduled_for.timestamp())}_{uuid.uuid4().hex[:6]}"
        queue_item = PublishingQueue(
            content_id=content_id,
            scheduled_for=scheduled_for,
            priority=1,
            retry_count=0,
            status="QUEUED",
            idempotency_key=idem_key,
            created_at=datetime.datetime.utcnow()
        )
        db.add(queue_item)
        content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if content:
            content.status = "QUEUED"
            content.scheduled_at = scheduled_for
        db.commit()
        db.refresh(queue_item)
        return queue_item

    def autonomous_content_generation_loop(self):
        """Periodically check queue buffer and autonomously create content to meet targets."""
        if self.emergency_stop:
            return

        is_render = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or os.getenv("IS_RENDER"))
        db = SessionLocal()
        try:
            today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + datetime.timedelta(days=1)

            queued_images = db.query(PublishingQueue).join(GeneratedContent).filter(
                GeneratedContent.content_type == "IMAGE",
                PublishingQueue.scheduled_for >= today_start,
                PublishingQueue.scheduled_for < today_end,
                PublishingQueue.status.in_(["QUEUED", "PUBLISHED"])
            ).count()

            queued_reels = db.query(PublishingQueue).join(GeneratedContent).filter(
                GeneratedContent.content_type == "REEL",
                PublishingQueue.scheduled_for >= today_start,
                PublishingQueue.scheduled_for < today_end,
                PublishingQueue.status.in_(["QUEUED", "PUBLISHED"])
            ).count()

            queued_stories = db.query(PublishingQueue).join(GeneratedContent).filter(
                GeneratedContent.content_type == "STORY",
                PublishingQueue.scheduled_for >= today_start,
                PublishingQueue.scheduled_for < today_end,
                PublishingQueue.status.in_(["QUEUED", "PUBLISHED"])
            ).count()

            import asyncio
            # Fill missing images (Lightweight Pillow generation: safe on all environments)
            if queued_images < self.daily_image_target:
                diff = min(2, self.daily_image_target - queued_images)
                for i in range(diff):
                    sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=i * 2 + 1)
                    content = asyncio.run(self.autonomous_generate_meme(db))
                    self.enqueue_content(db, content.id, sched_time)
                    trim_process_memory()

            # Fill missing reels (On Render: omit in-container FFmpeg to prevent 512MB RAM OOM)
            if not is_render:
                if queued_reels < self.daily_reels_target:
                    diff = min(2, self.daily_reels_target - queued_reels)
                    for i in range(diff):
                        sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=i * 3 + 2)
                        content = asyncio.run(self.autonomous_generate_reel(db))
                        if content:
                            self.enqueue_content(db, content.id, sched_time)
                        trim_process_memory()
            else:
                print("[Render Scheduler] Free tier memory safeguard active: reels generated via GitHub Actions runner.", flush=True)

            # Fill missing stories
            if queued_stories < self.daily_stories_target:
                sched_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                content = asyncio.run(self.autonomous_generate_story(db))
                self.enqueue_content(db, content.id, sched_time)
                trim_process_memory()

        except Exception as e:
            reliability_engine.record_error_and_recover(db, "SchedulerContentGen", e)
        finally:
            db.close()
            trim_process_memory()

    def process_due_queue_jobs(self):
        """Check for scheduled jobs that are due and publish them."""
        if self.emergency_stop or not self.auto_publish:
            return

        db = SessionLocal()
        try:
            now = datetime.datetime.utcnow()
            due_jobs = db.query(PublishingQueue).filter(
                PublishingQueue.status == "QUEUED",
                PublishingQueue.scheduled_for <= now
            ).order_by(PublishingQueue.scheduled_for.asc()).limit(3).all()

            import asyncio
            for job in due_jobs:
                job.status = "PROCESSING"
                db.commit()

                content = db.query(GeneratedContent).filter(GeneratedContent.id == job.content_id).first()
                if not content:
                    job.status = "FAILED"
                    job.last_error = "Content record not found"
                    db.commit()
                    continue

                # Publish via Instagram API client
                pub_result = None
                if content.content_type == "IMAGE":
                    pub_result = asyncio.run(instagram_client.publish_image_post(
                        image_url=content.media_path,
                        caption=content.caption
                    ))
                elif content.content_type == "REEL":
                    pub_result = asyncio.run(instagram_client.publish_reel(
                        video_url=content.media_path,
                        caption=content.caption,
                        cover_url=content.cover_path
                    ))
                elif content.content_type == "STORY":
                    pub_result = asyncio.run(instagram_client.publish_story(
                        image_url=content.media_path
                    ))

                if pub_result and pub_result.get("success"):
                    job.status = "PUBLISHED"
                    job.executed_at = datetime.datetime.utcnow()
                    content.status = "PUBLISHED"
                    content.published_at = datetime.datetime.utcnow()
                    content.post_id = pub_result.get("post_id")

                    # Record published post
                    published_post = PublishedPost(
                        content_id=content.id,
                        ig_post_id=pub_result.get("post_id"),
                        post_type=content.content_type,
                        permalink=pub_result.get("permalink", f"https://www.instagram.com/p/{pub_result.get('post_id')}/"),
                        caption=content.caption,
                        published_at=datetime.datetime.utcnow()
                    )
                    db.add(published_post)
                    db.commit()
                else:
                    job.retry_count += 1
                    err_msg = str(pub_result.get("error", "Publish failed") if pub_result else "No result")
                    job.last_error = err_msg
                    if job.retry_count >= job.max_retries:
                        job.status = "FAILED"
                    else:
                        job.status = "QUEUED"
                        job.scheduled_for = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                    db.commit()
                trim_process_memory()

        except Exception as e:
            reliability_engine.record_error_and_recover(db, "SchedulerQueueProcessor", e)
        finally:
            db.close()
            trim_process_memory()

    def sync_insights(self):
        """Fetch updated performance metrics for published content."""
        db = SessionLocal()
        try:
            recent_posts = db.query(PublishedPost).order_by(PublishedPost.published_at.desc()).limit(20).all()
            import asyncio
            for p in recent_posts:
                insights = asyncio.run(instagram_client.fetch_media_insights(p.ig_post_id, p.post_type))
                p.reach = insights.get("reach", p.reach)
                p.impressions = insights.get("impressions", p.impressions)
                p.likes = insights.get("likes", p.likes)
                p.comments = insights.get("comments", p.comments)
                p.shares = insights.get("shares", p.shares)
                p.saves = insights.get("saves", p.saves)
                p.last_synced_at = datetime.datetime.utcnow()

            db.commit()
        except Exception as e:
            reliability_engine.record_error_and_recover(db, "SchedulerInsightsSync", e)
        finally:
            db.close()
            trim_process_memory()

scheduler_engine = SchedulerEngine()

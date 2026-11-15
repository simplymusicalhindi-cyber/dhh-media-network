import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.models import *
from backend.app.services.scheduler_engine import scheduler_engine
from backend.app.services.research_engine import research_engine
from backend.app.services.growth_learning_engine import growth_learning_engine

# Import Routers
from backend.app.api.overview import router as overview_router
from backend.app.api.content_gen import router as content_gen_router
from backend.app.api.meme_studio import router as meme_studio_router
from backend.app.api.reels_studio import router as reels_studio_router
from backend.app.api.story_studio import router as story_studio_router
from backend.app.api.calendar_queue import router as calendar_queue_router
from backend.app.api.published import router as published_router
from backend.app.api.comments import router as comments_router
from backend.app.api.seo import router as seo_router
from backend.app.api.growth import router as growth_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.ai_settings import router as ai_settings_router
from backend.app.api.instagram import router as instagram_router
from backend.app.api.health import router as health_router
from backend.app.api.errors_recovery import router as errors_recovery_router
from backend.app.api.backups import router as backups_router
from backend.app.api.settings import router as settings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and start background scheduler quickly
    Base.metadata.create_all(bind=engine)
    scheduler_engine.start()

    # Run heavy seeding and reports asynchronously in background so port binds instantly (<0.2s)
    import asyncio
    async def run_background_init():
        loop = asyncio.get_running_loop()
        def _sync_init():
            db = SessionLocal()
            try:
                research_engine.seed_initial_topics(db)
                growth_learning_engine.generate_weekly_learning_report(db)
            except Exception as e:
                print(f"Background init warning: {e}", flush=True)
            finally:
                db.close()
        await loop.run_in_executor(None, _sync_init)

    asyncio.create_task(run_background_init())
    yield
    # Shutdown
    if scheduler_engine.scheduler.running:
        scheduler_engine.scheduler.shutdown(wait=False)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

@app.get("/health")
@app.get("/healthz")
def root_health():
    return {"status": "ok", "service": "dhh-media-network"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media directory for direct browser viewing & previewing
app.mount("/media", StaticFiles(directory=str(settings.MEDIA_DIR)), name="media")

# Include all API Routers
app.include_router(overview_router)
app.include_router(content_gen_router)
app.include_router(meme_studio_router)
app.include_router(reels_studio_router)
app.include_router(story_studio_router)
app.include_router(calendar_queue_router)
app.include_router(published_router)
app.include_router(comments_router)
app.include_router(seo_router)
app.include_router(growth_router)
app.include_router(analytics_router)
app.include_router(ai_settings_router)
app.include_router(instagram_router)
app.include_router(health_router)
app.include_router(errors_recovery_router)
app.include_router(backups_router)
app.include_router(settings_router)

# Mount frontend build static files if present
FRONTEND_DIST = settings.PROJECT_ROOT / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/")
    def index_root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "ONLINE",
            "docs_url": "/docs",
            "dashboard_note": "Frontend is running on Vite or can be compiled to frontend/dist"
        }

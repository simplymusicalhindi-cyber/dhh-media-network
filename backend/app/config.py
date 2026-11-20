import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

class Settings(BaseSettings):
    APP_NAME: str = "DHH Autonomous Instagram Media Network"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8787

    # Storage paths
    BASE_DIR: Path = BASE_DIR
    PROJECT_ROOT: Path = PROJECT_ROOT
    DATA_DIR: Path = BASE_DIR / "data"
    MEDIA_DIR: Path = BASE_DIR / "data" / "media"
    BACKUP_DIR: Path = BASE_DIR / "data" / "backups"
    SANDBOX_DIR: Path = BASE_DIR / "data" / "sandbox"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'data' / 'dhh_media.db'}"

    # Timezone
    TIMEZONE: str = "Asia/Kolkata"

    # AI Settings (Local first)
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3:latest"
    OLLAMA_TIMEOUT: float = 30.0
    AI_FALLBACK_TO_TEMPLATES: bool = True
    MIN_QUALITY_SCORE: float = 7.5

    # Publishing targets
    DAILY_IMAGE_POSTS_TARGET: int = 10
    DAILY_REELS_TARGET: int = 5
    DAILY_STORIES_TARGET: int = 1
    AUTO_PUBLISH_ENABLED: bool = True
    EMERGENCY_STOP: bool = False

    # Instagram API & Environment
    INSTAGRAM_MOCK_MODE: bool = False  # Set to False now that live official credentials are connected!
    META_APP_ID: str = "1137904655695388"
    META_APP_SECRET: str = "4ca6d73193a671f0c1893622ec5aa4f0"
    INSTAGRAM_ACCOUNT_ID: str = "17841419945554575"
    ACCESS_TOKEN: str = "EAAQK6xLKfhwBS1ZBpwXNGhAiRUkaSlwYNhwOdRguKeiuyfTAQPsxIIXNeyPn91uJr5RknnnaR9gGb7gwRZA7CzevT71qIB0xMlAjXMd1TUrr6GvFT0TdgKszZBsaEwBEsCVZAzb2gP0VuyzSYWV9zxEs6sL4F0ZBZBd9gxQRLQnx69akihLNY4zZA2xG7Y8mL0LxwNKeDz9"
    TOKEN_EXPIRES_AT: str = "NEVER_EXPIRES"
    # Public media URL base (Auto-detects Render.com public domain if running in cloud)
    PUBLIC_MEDIA_URL_BASE: str = os.getenv("RENDER_EXTERNAL_URL", "http://127.0.0.1:8787") + "/media" if os.getenv("RENDER_EXTERNAL_URL") else "http://127.0.0.1:8787/media"
    WEBHOOK_VERIFY_TOKEN: str = "dhh_meme_network_secure_token"

    # Security & Protection
    SECRET_KEY: str = "dhh-autonomous-super-secret-key-2026"
    MAX_AUTO_REPLIES_PER_HOUR: int = 50
    ALLOW_REMOTE_ACCESS: bool = False

    class Config:
        env_file = str(PROJECT_ROOT / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
for path in [settings.DATA_DIR, settings.MEDIA_DIR, settings.BACKUP_DIR, settings.SANDBOX_DIR]:
    path.mkdir(parents=True, exist_ok=True)
for sub in ["memes", "reels", "stories", "covers", "audio", "temp"]:
    (settings.MEDIA_DIR / sub).mkdir(parents=True, exist_ok=True)

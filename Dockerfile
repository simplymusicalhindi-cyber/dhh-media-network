FROM python:3.11-slim

# Install system dependencies: FFmpeg, tzdata, and fonts for Pillow typography
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tzdata \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app
ENV PORT=10000

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code, entrypoint, and pre-compiled frontend
COPY backend/ ./backend/
COPY frontend/dist/ ./frontend/dist/
COPY pytest.ini ./
COPY run.py ./

# Ensure data and media directories exist with write permissions
RUN mkdir -p /app/backend/data/media/memes \
             /app/backend/data/media/reels \
             /app/backend/data/media/stories \
             /app/backend/data/media/covers \
             /app/backend/data/media/audio \
             /app/backend/data/media/temp \
             /app/backend/data/backups \
             /app/backend/data/sandbox

EXPOSE 10000

# Run the 24/7 autonomous media engine
CMD ["python", "run.py"]

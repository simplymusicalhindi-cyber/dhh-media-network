# Multi-stage Dockerfile for 24/7 Autonomous Cloud Operation
# Stage 1: Build the React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend with FFmpeg
FROM python:3.11-slim

# Install system dependencies: FFmpeg and fonts for Pillow typography
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code and entrypoint
COPY backend/ ./backend/
COPY pytest.ini ./
COPY run.py ./

# Copy compiled frontend from Stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure data and media directories exist with write permissions
RUN mkdir -p /app/backend/data/media/memes \
             /app/backend/data/media/reels \
             /app/backend/data/media/stories \
             /app/backend/data/media/covers \
             /app/backend/data/media/audio \
             /app/backend/data/media/temp \
             /app/backend/data/backups \
             /app/backend/data/sandbox

# Seed initial cultural database on first build
RUN python -m backend.app.seed || true

EXPOSE 8787

# Run the 24/7 autonomous media engine
CMD ["python", "run.py"]

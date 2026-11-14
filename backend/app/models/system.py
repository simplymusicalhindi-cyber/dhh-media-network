from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from backend.app.database import Base

class SystemHealthLog(Base):
    __tablename__ = "system_health_logs"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String(100), nullable=False)
    status = Column(String(50), default="HEALTHY")  # HEALTHY, DEGRADED, DOWN
    message = Column(Text, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    module = Column(String(100), nullable=False)
    exception_type = Column(String(150), nullable=False)
    traceback = Column(Text, nullable=False)
    recovery_attempted = Column(Boolean, default=False)
    recovery_successful = Column(Boolean, default=False)
    recovery_action = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class BackupRecord(Base):
    __tablename__ = "backup_records"

    id = Column(Integer, primary_key=True, index=True)
    backup_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    backup_type = Column(String(50), default="SQLITE_SNAPSHOT")
    status = Column(String(50), default="SUCCESS")
    created_at = Column(DateTime, default=datetime.utcnow)

class ScheduledJobRecord(Base):
    __tablename__ = "scheduled_job_records"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, index=True)
    name = Column(String(150), nullable=False)
    next_run_time = Column(DateTime, nullable=True)
    last_status = Column(String(50), default="IDLE")
    last_run_time = Column(DateTime, nullable=True)

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, index=True)
    setting_val_json = Column(Text, default="")
    description = Column(String(255), default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

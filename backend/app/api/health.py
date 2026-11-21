from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.reliability_engine import reliability_engine

router = APIRouter(prefix="/api/health", tags=["System Health"])

@router.get("")
def get_system_health(db: Session = Depends(get_db)):
    """Run full diagnostic health check on all subsystems."""
    return reliability_engine.check_all_subsystems(db)

@router.get("/status")
def health_status():
    """Lightweight 200 OK health check for cloud uptime monitors and load balancers."""
    return {"status": "HEALTHY", "service": "dhh-media-network"}

@router.get("/memory")
def health_memory():
    """Real-time process memory telemetry and garbage collection trigger."""
    import os
    import gc
    import ctypes
    
    gc.collect()
    try:
        if hasattr(ctypes, "CDLL"):
            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
    except Exception:
        pass

    rss_mb = 0.0
    try:
        # On Linux (Docker/Render)
        with open("/proc/self/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    rss_kb = int(line.split()[1])
                    rss_mb = round(rss_kb / 1024.0, 2)
                    break
    except Exception:
        # Fallback
        try:
            import resource
            rss_mb = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 2)
        except Exception:
            pass

    return {
        "status": "HEALTHY",
        "rss_memory_mb": rss_mb,
        "memory_limit_mb": 512,
        "is_safe": rss_mb < 250,
        "environment": "RENDER" if os.getenv("RENDER") else "LOCAL"
    }

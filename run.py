import os
import sys
import traceback
import uvicorn

if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 8787))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"Starting DHH Autonomous Media Network on {host}:{port}...", flush=True)
        uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)
    except Exception as e:
        print("Fatal error in run.py:", e, file=sys.stderr, flush=True)
        traceback.print_exc()
        sys.exit(1)

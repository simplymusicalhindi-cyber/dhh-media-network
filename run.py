import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8787))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Starting DHH Autonomous Media Network on {host}:{port}...")
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)

"""Compatibility entrypoint — import the refactored FastAPI app from src."""
import uvicorn
import sys
import os

# ensure backend/fastapi is on path so imports from src work
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.main import app  # type: ignore
except Exception as e:
    print("Error importing refactored app:", e)
    raise

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

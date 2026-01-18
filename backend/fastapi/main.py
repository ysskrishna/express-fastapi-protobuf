import uvicorn
import sys
import os
from src.config import settings

# ensure backend/fastapi is on path so imports from src work
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.main import app  # type: ignore
except Exception as e:
    print("Error importing refactored app:", e)
    raise

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FASTAPI_HOST, port=settings.FASTAPI_PORT)

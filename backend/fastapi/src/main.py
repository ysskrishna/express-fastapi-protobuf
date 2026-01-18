import sys
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Ensure parent folder (backend/fastapi) is on sys.path so `proto` package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from .controllers import quotes as quotes_controller  # noqa: E402
from .controllers import tags as tags_controller      # noqa: E402
from .repos.quotes_repo import load_quotes            # noqa: E402

app = FastAPI(title="Quote Recommender API")

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Load dataset on startup
    await load_quotes()
    yield

app.router.lifespan_context = lifespan

# include routers
app.include_router(quotes_controller.router)
app.include_router(tags_controller.router)


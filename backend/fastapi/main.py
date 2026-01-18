import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config import settings
from src.controllers import quotes as quotes_controller
from src.controllers import tags as tags_controller
from src.repos.quotes_repo import load_quotes

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

if __name__ == "__main__":
    uvicorn.run(app, host=settings.FASTAPI_HOST, port=settings.FASTAPI_PORT)

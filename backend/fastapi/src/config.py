from pydantic import BaseSettings


class Settings(BaseSettings):
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    # Add other environment-driven settings here as needed

    class Config:
        env_file = ".env"


settings = Settings()


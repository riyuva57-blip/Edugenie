from functools import lru_cache
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-3.8-flash", validation_alias="GEMINI_MODEL")
    explanation_model: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M", validation_alias="EXPLANATION_MODEL"
    )
    explanation_backend: str = Field(default="local", validation_alias="EXPLANATION_BACKEND")
    local_model_enabled: bool = Field(default=True, validation_alias="LOCAL_MODEL_ENABLED")
    host: str = Field(default="127.0.0.1", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")
    cors_origins: str = Field(
        default="http://127.0.0.1:8000,http://localhost:8000", validation_alias="CORS_ORIGINS"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings.model_validate({key: value for key, value in os.environ.items() if key in {
        "GEMINI_API_KEY", "GEMINI_MODEL", "EXPLANATION_MODEL", "EXPLANATION_BACKEND",
        "LOCAL_MODEL_ENABLED", "HOST", "PORT", "CORS_ORIGINS"
    }})

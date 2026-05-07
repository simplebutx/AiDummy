from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Study API"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    model_artifact_path: str = "artifacts/classification_pipeline.joblib"
    model_metadata_path: str = "artifacts/classification_metadata.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def resolved_model_artifact_path(self) -> Path:
        return Path(self.model_artifact_path).resolve()

    @property
    def resolved_model_metadata_path(self) -> Path:
        return Path(self.model_metadata_path).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()

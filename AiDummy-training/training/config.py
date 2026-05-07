from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_artifact_path: str = "artifacts/classification_pipeline.joblib"
    model_metadata_path: str = "artifacts/classification_metadata.json"
    tuning_results_path: str = "artifacts/tuning_results.json"

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

    @property
    def resolved_tuning_results_path(self) -> Path:
        return Path(self.tuning_results_path).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()


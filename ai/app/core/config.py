from functools import lru_cache   # 함수 결과를 기억해두는데 쓰는 도구 
# (get_settings()여러번 불러도 Settings()를 매번 새로 만들지 않게 하기 위해
from pathlib import Path  # 파일 경로를 쉽게 다루는 도구

#.env파일이나 환경변수에서 설정값을 읽기 위한 라이브러리
from pydantic_settings import BaseSettings, SettingsConfigDict   

# 설정값 모아두는 클래스
class Settings(BaseSettings):
    app_name: str = "AI Study API"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    model_artifact_path: str = "artifacts/classification_pipeline.joblib" # 모델 경로

    # 설정 클래스를 어떻게 읽을지 
    model_config = SettingsConfigDict(
        env_file=".env",  # .env 파일에서 설정값 읽기
        env_file_encoding="utf-8",
        case_sensitive=False,  # 환경변수 대소문자 구분을 엄격하게 안 함
    )

    # model_artifact_path는 원래 문자열임. 이걸 실제 절대경로 Path 객체로 바꿔서 반환하는 편의용 속성임
    @property
    def resolved_model_artifact_path(self) -> Path:
        return Path(self.model_artifact_path).resolve()

# 설정 객체 꺼내오는 함수 
@lru_cache  # 처음한번만 Settings()를 생성하고 그 다음부터는 같은 객체 재사용
def get_settings() -> Settings:
    return Settings()

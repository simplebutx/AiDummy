from fastapi import FastAPI

from app.api.routes.classification import router as classification_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings


settings = get_settings()

#FastAPI 앱 객체 생성 (title은 앱이름)
app = FastAPI(title=settings.app_name)

# 각 파일에 있는 API들을 이 앱에 등록 (/api/v1 은 공통 앞주소)
app.include_router(health_router, prefix="/api/v1")
app.include_router(classification_router, prefix="/api/v1")


# 라우터 왜씀? 분류 API를 파일별로 나누게, 나중에 요약, 추천이런거 추가할때도 편하게
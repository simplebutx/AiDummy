# 컨트롤러 역할

from fastapi import APIRouter

from app.schemas.classification import (
    ClassificationPredictionRequest,
    ClassificationPredictionResponse,
)
from app.services.classification_service import ClassificationService


router = APIRouter(prefix="/classification", tags=["classification"])


@router.post("/predict", response_model=ClassificationPredictionResponse)  # response_model: 응답 형태
def predict_category(
    request: ClassificationPredictionRequest,  # 요청값 형식
) -> ClassificationPredictionResponse:  # 응답값 형식
    return ClassificationService().predict(request)

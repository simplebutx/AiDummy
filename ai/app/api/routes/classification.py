# 컨트롤러 역할

from fastapi import APIRouter

from app.schemas.classification import (
    ClassificationLabelListResponse,
    ClassificationModelInfoResponse,
    ClassificationPredictionRequest,
    ClassificationPredictionResponse,
)
from app.services.classification_service import ClassificationService


router = APIRouter(prefix="/classification", tags=["classification"])


@router.get("/labels", response_model=ClassificationLabelListResponse)
def get_labels() -> ClassificationLabelListResponse:
    return ClassificationLabelListResponse(
        labels=ClassificationService.supported_labels()
    )


@router.get("/model-info", response_model=ClassificationModelInfoResponse)
def get_model_info() -> ClassificationModelInfoResponse:
    return ClassificationService().get_model_info()


@router.post("/predict", response_model=ClassificationPredictionResponse)  # response_model: 응답 형태
def predict_category(
    request: ClassificationPredictionRequest,  # 요청값 형식
) -> ClassificationPredictionResponse:  # 응답값 형식
    return ClassificationService().predict(request)

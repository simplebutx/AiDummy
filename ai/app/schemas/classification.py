# BaseModel: 데이터 모양을 정의하는 틀(dto)
from pydantic import BaseModel, Field


class ClassificationPredictionRequest(BaseModel):
    text: str = Field(min_length=5, max_length=2000)


class ClassificationPredictionResponse(BaseModel):
    text: str
    predicted_label: str  # 모델이 고른 라벨값
    label_description: str  # 그 라벨을 사람이 읽기 쉽게 설명한 값
    confidence: float


class ClassificationModelInfoResponse(BaseModel):
    trained_samples: int
    test_samples: int
    accuracy: float
    labels: list[str]
    trained_at: str
    model_version: str


class ClassificationLabelListResponse(BaseModel):
    labels: list[str]

# BaseModel: 데이터 모양을 정의하는 틀(dto)
from pydantic import BaseModel, Field


class ClassificationPredictionRequest(BaseModel):
    # 사용자가 보낸 문의 문장
    text: str = Field(min_length=5, max_length=2000)


class ClassificationPredictionResponse(BaseModel):
    # 원본 입력 문장
    text: str
    # 모델이 예측한 라벨값
    predicted_label: str
    # 라벨을 사람이 읽기 쉬운 설명으로 바꾼 값
    label_description: str
    # 예측 확률
    confidence: float

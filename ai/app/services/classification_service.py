import joblib # 머신러닝 모델을 파일로 저장하고 다시 불러올 때 쓰는 라이브러리
import numpy as np
from fastapi import HTTPException
from sklearn.pipeline import Pipeline  # 저장된 sklearn 파이프라인 타입 표시용

from app.core.config import get_settings
from app.data.label_descriptions import LABEL_DESCRIPTIONS
from app.schemas.classification import (
    ClassificationPredictionRequest,
    ClassificationPredictionResponse,
)


class ClassificationService:
    # 한 번 불러온 모델을 메모리에 보관해서 매 요청마다 파일을 다시 읽지 않게 함
    _model: Pipeline | None = None

    # 실제 예측 처리 함수
    def predict(self, request: ClassificationPredictionRequest) -> ClassificationPredictionResponse:
        model = self._load_model()  # 저장된 모델 파일 불러오기

        predicted_label = str(model.predict([request.text])[0])  # 실제 예측 라벨
        probabilities = model.predict_proba([request.text])[0]  # 각 라벨별 확률
        class_names = model.classes_  # 모델이 알고있는 라벨 목록을 순서대로 꺼냄
        # ["account_access", "billing_payment", "delivery", "return_refund", "technical_issue"]

        # 확률만 꺼내기
        confidence = self._extract_confidence(class_names, probabilities, predicted_label)

        # FastAPI 응답 형태로 변환
        return ClassificationPredictionResponse(
            text=request.text,
            predicted_label=predicted_label,  # 선택된 라벨
            label_description=LABEL_DESCRIPTIONS[predicted_label],  # 선택된 라벨을 한국어로
            confidence=round(confidence, 4),  # 선택된 라벨의 확률
        )

    # joblib로 저장된 모델 파일을 읽어오는 함수
    def _load_model(self) -> Pipeline:
        if self.__class__._model is not None:
            return self.__class__._model

        settings = get_settings()
        model_path = settings.resolved_model_artifact_path

        if not model_path.exists():
            raise HTTPException(
                status_code=503,
                detail="학습된 모델 파일이 없습니다. AiDummy-training 프로젝트에서 모델을 만든 뒤 artifacts를 반영하세요.",
            )

        self.__class__._model = joblib.load(model_path)
        return self.__class__._model

    # 예측된 라벨에 해당하는 확률만 꺼내는 함수
    @staticmethod
    def _extract_confidence(
        class_names,
        probabilities: np.ndarray,
        predicted_label: str,
    ) -> float:
        for index, class_name in enumerate(class_names):
            if class_name == predicted_label:
                return float(probabilities[index])
        return 0.0

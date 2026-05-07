import json
from collections.abc import Sequence

import joblib
import numpy as np
from fastapi import HTTPException
from sklearn.pipeline import Pipeline

from app.core.config import get_settings
from app.data.dummy_inquiries import LABEL_DESCRIPTIONS
from app.schemas.classification import (
    ClassificationModelInfoResponse,
    ClassificationPredictionRequest,
    ClassificationPredictionResponse,
)


class ClassificationService:
    _model: Pipeline | None = None
    _labels: list[str] = sorted(LABEL_DESCRIPTIONS.keys())
    _metadata: dict | None = None

    # 라벨 목록 돌려주는 함수
    @classmethod
    def supported_labels(cls) -> list[str]:
        return cls._labels

    # Colab에서 학습한 모델 정보와 메타데이터를 FastAPI가 불러오는 함수
    def get_model_info(self) -> ClassificationModelInfoResponse:
        metadata = self._load_metadata()
        return ClassificationModelInfoResponse(
            trained_samples=int(metadata["trained_samples"]),
            test_samples=int(metadata["test_samples"]),
            accuracy=float(metadata["accuracy"]),
            labels=list(metadata["labels"]),
            trained_at=str(metadata["trained_at"]),
            model_version=str(metadata["model_version"]),
        )

    # 예측
    def predict(self, request: ClassificationPredictionRequest) -> ClassificationPredictionResponse:
        model = self._load_model()  # Colab에서 학습한 모델을 불러오기

        predicted_label = str(model.predict([request.text])[0])  # 실제 예측
        probabilities = model.predict_proba([request.text])[0]  # 확률값 계산
        class_names = model.classes_  # 확률 배열이 어떤 라벨 순서인지 가져옴
        # ["account_access", "billing_payment", "delivery", "return_refund", "technical_issue"]

        confidence = self._extract_confidence(class_names, probabilities, predicted_label)  # 예측된 라벨에 해당하는 확률만 꺼냄

        # 응답 만들기
        return ClassificationPredictionResponse(
            text=request.text,
            predicted_label=predicted_label,
            label_description=LABEL_DESCRIPTIONS[predicted_label],
            confidence=round(confidence, 4),
        )

    # Colab에서 학습한 모델을 joblib 파일로 저장해둔 뒤에 불러오기
    def _load_model(self) -> Pipeline:
        if self.__class__._model is not None:
            return self.__class__._model

        settings = get_settings()
        model_path = settings.resolved_model_artifact_path

        if not model_path.exists():
            raise HTTPException(
                status_code=503,
                detail="학습된 모델 파일이 없습니다. Colab 또는 로컬에서 train_model.py를 먼저 실행하세요.",
            )

        self.__class__._model = joblib.load(model_path)
        return self.__class__._model

    # Colab에서 학습 결과 메타데이터를 json 파일로 저장해둔 뒤에 불러오기
    def _load_metadata(self) -> dict:
        if self.__class__._metadata is not None:
            return self.__class__._metadata

        settings = get_settings()
        metadata_path = settings.resolved_model_metadata_path

        if not metadata_path.exists():
            raise HTTPException(
                status_code=503,
                detail="학습된 모델 메타데이터가 없습니다. Colab 또는 로컬에서 train_model.py를 먼저 실행하세요.",
            )

        self.__class__._metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        return self.__class__._metadata

    # 예측된 라벨의 점수만 골라내는 함수
    @staticmethod
    def _extract_confidence(
        class_names: Sequence[str],  # ["account_access", "billing_payment", "delivery", "return_refund", "technical_issue"]
        probabilities: np.ndarray,  # [0.10, 0.18, 0.3047, 0.22, 0.19]
        predicted_label: str,  # 예측된 라벨 ex) "delivery"
    ) -> float:
        for index, class_name in enumerate(class_names):
            if class_name == predicted_label:
                return float(probabilities[index])  # ex) 0.3047
        return 0.0

import json
from datetime import datetime, timezone

import joblib
from sklearn.metrics import accuracy_score  # 예측 결과가 실제 정답과 얼마나 맞았는지 계산하는 함수
from sklearn.model_selection import train_test_split   # 데이터를 학습용과 테스트용으로 나누는 함수

from training.config import get_settings
from training.data.dummy_inquiries import DUMMY_INQUIRIES, LABEL_DESCRIPTIONS
from training.ml.pipeline import build_text_classification_pipeline  # 파이프라인 만들어주는 함수


def main() -> None:
    settings = get_settings()

    texts = [item["text"] for item in DUMMY_INQUIRIES]
    labels = [item["label"] for item in DUMMY_INQUIRIES]

    if len(texts) < 10:
        raise RuntimeError("학습 데이터가 충분하지 않습니다.")

    #---------------------------------------------------------

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = build_text_classification_pipeline()
    model.fit(x_train, y_train)  # 모델 학습시킴

    predictions = model.predict(x_test)  # x_test에 있는 테스트용 문장들을 모델이 예측
    accuracy = accuracy_score(y_test, predictions)  # 정확도 계산

    #---------------------------------------------------------

    # 오답 표시
    wrong_count = 0
    for text, actual, predicted in zip(x_test, y_test, predictions):
        if actual != predicted:
            wrong_count += 1
            print(f"[오답 {wrong_count}]")
            print("문장:", text)
            print("실제:", actual)
            print("예측:", predicted)
            print("-" * 50)

    if wrong_count == 0:
        print("오답 없음")

    #---------------------------------------------------------

    model_path = settings.resolved_model_artifact_path  # 모델을 저장할 경로
    metadata_path = settings.resolved_model_metadata_path  # 메타데이터를 저장할 경로
    model_path.parent.mkdir(parents=True, exist_ok=True)  # model_path의 부모 폴더를 만들겠다
    metadata_path.parent.mkdir(parents=True, exist_ok=True) # 메타데이터파일의 부모 폴더를 만들겠다

    joblib.dump(model, model_path)  # 학습된 모델을 저장하는 코드

    metadata = {
        "trained_samples": len(x_train),
        "test_samples": len(x_test),
        "accuracy": round(float(accuracy), 4),
        "labels": sorted(LABEL_DESCRIPTIONS.keys()),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "model_version": "classification-v1",
    }
    metadata_path.write_text(  # 딕셔너리를 JSON 파일로 저장
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Model saved:", model_path)
    print("Metadata saved:", metadata_path)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))

    #----------------------------------------------------------

    

# 파일을 직접 실행했을 때만 main()을 돌려라
if __name__ == "__main__":
    main()


import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from app.core.config import get_settings
from app.data.dummy_inquiries import DUMMY_INQUIRIES, LABEL_DESCRIPTIONS
from app.ml.pipeline import build_text_classification_pipeline


def main() -> None:
    settings = get_settings()

    texts = [item["text"] for item in DUMMY_INQUIRIES]
    labels = [item["label"] for item in DUMMY_INQUIRIES]

    if len(texts) < 10:
        raise RuntimeError("학습 데이터가 충분하지 않습니다.")

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = build_text_classification_pipeline()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    model_path = settings.resolved_model_artifact_path
    metadata_path = settings.resolved_model_metadata_path
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    metadata = {
        "trained_samples": len(x_train),
        "test_samples": len(x_test),
        "accuracy": round(float(accuracy), 4),
        "labels": sorted(LABEL_DESCRIPTIONS.keys()),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "model_version": "classification-v1",
    }
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Model saved:", model_path)
    print("Metadata saved:", metadata_path)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

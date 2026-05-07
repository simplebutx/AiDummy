import json
from datetime import datetime, timezone

from sklearn.model_selection import GridSearchCV, train_test_split

from training.config import get_settings
from training.data.dummy_inquiries import DUMMY_INQUIRIES
from training.ml.pipeline import build_text_classification_pipeline


def main() -> None:
    settings = get_settings()

    texts = [item["text"] for item in DUMMY_INQUIRIES]
    labels = [item["label"] for item in DUMMY_INQUIRIES]

    if len(texts) < 10:
        raise RuntimeError("튜닝용 데이터가 충분하지 않습니다.")

    x_train, _, y_train, _ = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    model = build_text_classification_pipeline()

    param_grid = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__min_df": [1, 2],
        "classifier__C": [0.5, 1.0, 2.0, 5.0],
    }

    search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=3,
        n_jobs=-1,
        scoring="accuracy",
    )
    search.fit(x_train, y_train)

    results_path = settings.resolved_tuning_results_path
    results_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "best_score": round(float(search.best_score_), 4),
        "best_params": search.best_params_,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }
    results_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Tuning results saved:", results_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


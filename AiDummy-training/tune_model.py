import json
from datetime import datetime, timezone

# GridSearchCV: 하이퍼파라미터 조합을 전부 다 돌려보면서 가장 좋은 조합을 찾는 도구
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

    # 가능한 조합을 모두 돌려봄
    param_grid = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__min_df": [1, 2],
        "classifier__C": [0.5, 1.0, 2.0, 5.0],
    }

    search = GridSearchCV(
        estimator=model,  # 튜닝할 대상 모델
        param_grid=param_grid,  # 조합표 넣기
        cv=3,   # 3번 나눠가며 평가
        n_jobs=-1,  # 가능한 CPU 코어를 다 써서 병렬 처리하라는 뜻
        scoring="accuracy",  # 어떤 기준으로 좋은 모델인지 판단할지 정하는 옵션
    )
    search.fit(x_train, y_train)   # 튜닝 실행

    # -----------------------------------------------------------
    
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


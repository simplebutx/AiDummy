# AiDummy Training

AiDummy 서비스에서 사용하는 텍스트 분류 모델을 학습하고 튜닝하는 전용 프로젝트입니다.

현재 역할:

- 더미 문의 데이터셋 관리
- 로컬 또는 Colab에서 모델 학습
- 하이퍼파라미터 튜닝 실험
- 학습 결과물 생성

서비스 프로젝트와의 관계:

- 이 프로젝트는 학습과 튜닝만 담당합니다.
- 최종 결과물인 `classification_pipeline.joblib`, `classification_metadata.json`만 서비스 프로젝트의 `ai/artifacts`로 복사해서 사용합니다.

## 폴더 구조

```text
AiDummy-training
├─ training
│  ├─ config.py
│  ├─ data
│  └─ ml
├─ artifacts
├─ tests
├─ .env.example
├─ requirements.txt
├─ train_model.py
├─ tune_model.py
└─ README.md
```

## 실행 예시

```bash
pip install -r requirements.txt
python train_model.py
python tune_model.py
```

## 학습 결과물

학습이 끝나면 아래 파일이 생성됩니다.

- `artifacts/classification_pipeline.joblib`
- `artifacts/classification_metadata.json`

튜닝이 끝나면 아래 파일이 생성됩니다.

- `artifacts/tuning_results.json`

## 서비스 프로젝트에 반영

학습이 완료되면 아래 파일 2개를 서비스 프로젝트로 복사하면 됩니다.

- `AiDummy-training/artifacts/classification_pipeline.joblib`
- `AiDummy-training/artifacts/classification_metadata.json`

복사 대상:

- `AiDummy/ai/artifacts/classification_pipeline.joblib`
- `AiDummy/ai/artifacts/classification_metadata.json`

## Colab 흐름

1. 이 저장소를 GitHub에 올립니다.
2. Colab에서 `git clone`으로 가져옵니다.
3. `pip install -r requirements.txt`를 실행합니다.
4. `python train_model.py` 또는 `python tune_model.py`를 실행합니다.
5. `artifacts` 결과물을 다운로드해서 서비스 프로젝트에 반영합니다.


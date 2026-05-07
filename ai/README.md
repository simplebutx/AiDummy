# AI Study FastAPI

학습용 분류 예제를 위한 FastAPI 서버입니다.

현재 역할:

- AI 예측 전용 API 서버
- 메인 백엔드는 `Backend`의 Spring Boot 서버
- 프론트엔드는 루트 `frontend` 폴더에서 별도 관리
- 학습/튜닝은 Colab 또는 별도 환경에서 수행

현재 구현 범위:

- 고객 문의 텍스트 분류
- 파일 기반 더미 데이터 사용
- TF-IDF + Logistic Regression 예측
- 예측 / 모델 정보 API

## 폴더 구조

```text
ai
├─ app
│  ├─ api
│  ├─ core
│  ├─ data
│  ├─ ml
│  ├─ schemas
│  └─ services
├─ artifacts
├─ .env.example
├─ requirements.txt
├─ train_model.py
└─ README.md
```

## 실행 예시

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Colab 또는 로컬 학습

학습은 `train_model.py`에서 수행합니다.

```bash
python train_model.py
```

실행 후 아래 파일이 생성됩니다.

- `artifacts/classification_pipeline.joblib`
- `artifacts/classification_metadata.json`

FastAPI 서버는 위 파일을 읽어서 예측만 수행합니다.

## 주요 엔드포인트

- `GET /api/v1/health`
- `GET /api/v1/classification/labels`
- `GET /api/v1/classification/model-info`
- `POST /api/v1/classification/predict`

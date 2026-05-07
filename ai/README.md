# AI Study FastAPI

학습이 끝난 모델 파일을 읽어서 예측 API를 제공하는 FastAPI 서버입니다.

현재 역할:

- AI 예측 전용 API 서버
- 메인 백엔드는 `Backend`의 Spring Boot 서버
- 프론트엔드는 루트 `frontend` 폴더에서 별도 관리
- 학습/튜닝은 별도 `AiDummy-training` 프로젝트에서 수행

현재 구현 범위:

- 고객 문의 텍스트 분류 예측

## 폴더 구조

```text
ai
├─ app
│  ├─ api
│  ├─ core
│  ├─ data
│  ├─ schemas
│  └─ services
├─ artifacts
├─ .env.example
├─ requirements.txt
└─ README.md
```

## 실행 예시

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 모델 반영

학습이 끝난 뒤 아래 파일을 `AiDummy-training` 프로젝트에서 복사해서 사용합니다.

- `artifacts/classification_pipeline.joblib`

FastAPI 서버는 위 파일을 읽어서 예측만 수행합니다.

## 주요 엔드포인트

- `GET /api/v1/health`
- `POST /api/v1/classification/predict`

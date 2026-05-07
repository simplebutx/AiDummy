import { useState } from "react";

const EXAMPLE_SENTENCES = [
  "결제는 되었는데 주문 내역에 보이지 않습니다.",
  "상품이 배송 완료로 표시되는데 아직 받지 못했어요.",
  "반품 신청했는데 환불이 언제 처리되는지 궁금합니다.",
  "로그인 인증번호 문자가 오지 않아서 접속을 못 하고 있습니다.",
  "앱에서 상품 상세 페이지를 열면 오류가 발생합니다."
];

const LABEL_KO = {
  delivery: "배송",
  return_refund: "반품/환불",
  billing_payment: "결제",
  technical_issue: "기술 문제",
  account_access: "계정/접근"
};

function normalizePrediction(data) {
  const predictedLabel = data.predictedLabel ?? data.predicted_label ?? "";
  const labelDescription = data.labelDescription ?? data.label_description ?? "";
  const confidence = data.confidence ?? "";

  return {
    predictedLabel,
    predictedLabelKo: LABEL_KO[predictedLabel] ?? predictedLabel,
    labelDescription,
    confidence
  };
}

function App() {
  const [backendBaseUrl, setBackendBaseUrl] = useState("http://localhost:8080");
  const [status, setStatus] = useState("대기 중");
  const [resultText, setResultText] = useState("아직 실행 결과가 없습니다.");
  const [inputText, setInputText] = useState("");
  const [prediction, setPrediction] = useState(null);

  const requestJson = async (path, options = {}) => {
    const response = await fetch(`${backendBaseUrl.replace(/\/$/, "")}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      ...options
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      const message =
        typeof data === "string"
          ? data
          : data.detail || data.message || "요청 처리 중 오류가 발생했습니다.";
      throw new Error(message);
    }

    return data;
  };

  const handleLoadLabels = async () => {
    try {
      setStatus("라벨 조회 중");
      const data = await requestJson("/api/ai/classification/labels");
      setResultText(JSON.stringify(data, null, 2));
      setStatus("라벨 조회 완료");
    } catch (error) {
      setStatus("실패");
      setResultText(error.message);
    }
  };

  const handleLoadModelInfo = async () => {
    try {
      setStatus("모델 정보 조회 중");
      const data = await requestJson("/api/ai/classification/model-info");
      setResultText(JSON.stringify(data, null, 2));
      setStatus("모델 정보 조회 완료");
    } catch (error) {
      setStatus("실패");
      setResultText(error.message);
    }
  };

  const handlePredict = async (event) => {
    event.preventDefault();

    if (!inputText.trim()) {
      setStatus("입력이 필요합니다");
      return;
    }

    try {
      setStatus("문장 분류 중");
      const data = await requestJson("/api/ai/classification/predict", {
        method: "POST",
        body: JSON.stringify({ text: inputText.trim() })
      });
      setPrediction(normalizePrediction(data));
      setStatus("분류 완료");
    } catch (error) {
      setPrediction({
        predictedLabel: "error",
        predictedLabelKo: "오류",
        confidence: "",
        labelDescription: error.message
      });
      setStatus("실패");
    }
  };

  const handleFillExample = () => {
    const randomIndex = Math.floor(Math.random() * EXAMPLE_SENTENCES.length);
    setInputText(EXAMPLE_SENTENCES[randomIndex]);
  };

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">React Frontend</p>
        <h1>고객 문의 분류 확인 페이지</h1>
        <p className="hero-text">
          이 화면은 루트 <code>frontend</code> 폴더의 React 앱입니다.
          브라우저는 FastAPI를 직접 호출하지 않고 Spring Boot 메인 서버의
          <code> /api/ai/** </code>
          엔드포인트만 호출합니다.
        </p>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>연결 설정</h2>
          <span className="status-badge">{status}</span>
        </div>
        <div className="server-config">
          <label htmlFor="backend-base-url">Backend Base URL</label>
          <input
            id="backend-base-url"
            type="text"
            value={backendBaseUrl}
            onChange={(event) => setBackendBaseUrl(event.target.value)}
          />
        </div>
      </section>

      <section className="panel actions-panel">
        <div className="panel-header">
          <h2>AI 작업</h2>
          <span className="hint">Spring Boot가 AI 서버로 프록시 요청합니다</span>
        </div>
        <div className="action-grid">
          <button className="action-button secondary" onClick={handleLoadLabels}>
            라벨 목록 보기
          </button>
          <button className="action-button primary" onClick={handleLoadModelInfo}>
            모델 정보 보기
          </button>
        </div>
        <pre className="result-box muted">{resultText}</pre>
      </section>

      <section className="content-grid">
        <section className="panel">
          <div className="panel-header">
            <h2>문장 분류</h2>
            <span className="hint">Backend /api/ai/classification/predict 호출</span>
          </div>
          <form className="predict-form" onSubmit={handlePredict}>
            <textarea
              rows="7"
              placeholder="예: 주문은 했는데 배송조회 번호가 안 보여요."
              value={inputText}
              onChange={(event) => setInputText(event.target.value)}
            />
            <div className="form-actions">
              <button
                type="button"
                className="action-button ghost"
                onClick={handleFillExample}
              >
                예시 문장 넣기
              </button>
              <button type="submit" className="action-button primary">
                분류하기
              </button>
            </div>
          </form>

          {prediction && (
            <div className="prediction-card">
              <div className="prediction-label-row">
                <span className="prediction-label">
                  {prediction.predictedLabelKo}
                  {prediction.predictedLabel ? ` (${prediction.predictedLabel})` : ""}
                </span>
                <span className="prediction-confidence">
                  {prediction.confidence !== "" ? `confidence ${prediction.confidence}` : ""}
                </span>
              </div>
              <p className="prediction-description">{prediction.labelDescription}</p>
            </div>
          )}
        </section>

        <section className="panel">
          <div className="panel-header">
            <h2>학습 안내</h2>
            <span className="hint">학습은 Colab 또는 별도 환경에서 진행합니다</span>
          </div>
          <div className="info-stack">
            <div className="dataset-item">
              <span className="dataset-item-label">train</span>
              <p className="dataset-item-text">
                모델 학습과 튜닝은 FastAPI 서버 밖에서 진행하고, 결과 모델만 저장합니다.
              </p>
            </div>
            <div className="dataset-item">
              <span className="dataset-item-label">predict</span>
              <p className="dataset-item-text">
                FastAPI 서버는 저장된 모델을 불러와 예측만 수행합니다.
              </p>
            </div>
            <div className="dataset-item">
              <span className="dataset-item-label">proxy</span>
              <p className="dataset-item-text">
                브라우저는 Python 서버를 직접 호출하지 않고 Spring Boot 서버를 통해 요청합니다.
              </p>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}

export default App;

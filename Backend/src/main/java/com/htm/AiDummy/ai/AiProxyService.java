package com.htm.AiDummy.ai;

import com.htm.AiDummy.ai.dto.AiLabelListResponse;
import com.htm.AiDummy.ai.dto.AiModelInfoResponse;
import com.htm.AiDummy.ai.dto.AiPredictionForwardRequest;
import com.htm.AiDummy.ai.dto.AiPredictionRequest;
import com.htm.AiDummy.ai.dto.AiPredictionResponse;
import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class AiProxyService {

    private final RestClient aiRestClient;

    public AiProxyService(RestClient aiRestClient) {
        this.aiRestClient = aiRestClient;
    }

    public AiModelInfoResponse getModelInfo() {
        return aiRestClient.get()
                .uri("/api/v1/classification/model-info")
                .retrieve()
                .body(AiModelInfoResponse.class);
    }

    public AiPredictionResponse predict(AiPredictionRequest request) {
        Map<String, Object> response = aiRestClient.post()
                .uri("/api/v1/classification/predict")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON)
                .body(new AiPredictionForwardRequest(request.text()))
                .retrieve()
                .body(Map.class);

        if (response == null) {
            throw new IllegalStateException("AI prediction response is empty.");
        }

        Object confidenceValue = response.get("confidence");
        double confidence = confidenceValue instanceof Number number
                ? number.doubleValue()
                : 0.0;

        return new AiPredictionResponse(
                (String) response.get("text"),
                (String) response.get("predicted_label"),
                (String) response.get("label_description"),
                confidence
        );
    }

    public AiLabelListResponse getLabels() {
        return aiRestClient.get()
                .uri("/api/v1/classification/labels")
                .retrieve()
                .body(AiLabelListResponse.class);
    }
}

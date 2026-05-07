package com.htm.AiDummy.ai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record AiPredictionResponse(
        String text,
        @JsonProperty("predicted_label")
        String predictedLabel,
        @JsonProperty("label_description")
        String labelDescription,
        double confidence
) {
}

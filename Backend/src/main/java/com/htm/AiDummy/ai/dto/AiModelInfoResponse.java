package com.htm.AiDummy.ai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public record AiModelInfoResponse(
        @JsonProperty("trained_samples")
        int trainedSamples,
        @JsonProperty("test_samples")
        int testSamples,
        double accuracy,
        List<String> labels,
        @JsonProperty("trained_at")
        String trainedAt,
        @JsonProperty("model_version")
        String modelVersion
) {
}

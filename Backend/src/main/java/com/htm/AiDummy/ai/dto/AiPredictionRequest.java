package com.htm.AiDummy.ai.dto;

import jakarta.validation.constraints.NotBlank;

public record AiPredictionRequest(
        @NotBlank String text
) {
}

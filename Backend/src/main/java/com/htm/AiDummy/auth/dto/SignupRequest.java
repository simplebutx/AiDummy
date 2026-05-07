package com.htm.AiDummy.auth.dto;

import jakarta.validation.constraints.NotBlank;

public record SignupRequest(
        @NotBlank String userName,
        @NotBlank String password,
        @NotBlank String displayName
) {
}

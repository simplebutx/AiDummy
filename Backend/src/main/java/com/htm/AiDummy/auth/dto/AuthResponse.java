package com.htm.AiDummy.auth.dto;

public record AuthResponse(
        String accessToken,
        String tokenType,
        String userName,
        String displayName
) {
}

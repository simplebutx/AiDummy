package com.htm.AiDummy.auth.dto;

public record UserResponse(
        Long id,
        String userName,
        String displayName
) {
}

package com.htm.AiDummy.ai;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.service")
public record AiProperties(
        String baseUrl
) {
}

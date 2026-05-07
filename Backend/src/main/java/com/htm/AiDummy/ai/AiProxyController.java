package com.htm.AiDummy.ai;

import com.htm.AiDummy.ai.dto.AiPredictionRequest;
import com.htm.AiDummy.ai.dto.AiPredictionResponse;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/ai")
public class AiProxyController {

    private final AiProxyService aiProxyService;

    public AiProxyController(AiProxyService aiProxyService) {
        this.aiProxyService = aiProxyService;
    }

    @PostMapping("/classification/predict")
    public AiPredictionResponse predict(
            @Valid @RequestBody AiPredictionRequest request
    ) {
        return aiProxyService.predict(request);
    }
}

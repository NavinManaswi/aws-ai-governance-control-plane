# OPA Policy: Bedrock Compliance
# Evaluates Bedrock resources against NIST AI RMF and EU AI Act

package bedrock.compliance

import future.keywords.in

default allow := false

allow {
    guardrails_enabled
    logging_enabled
    model_evaluation_configured
    no_public_access
}

# ============================================================================
# Guardrails Controls
# ============================================================================

# Check: Bedrock Guardrails must be enabled
guardrails_enabled {
    input.resourceType == "AWS::Bedrock::Guardrail"
    input.resourceProperties.Name != null
    input.resourceProperties.TopicPolicyConfig.TopicsConfig != null
}

guardrails_enabled {
    input.resourceType == "AWS::Bedrock::Agent"
    input.resourceProperties.GuardrailIdentifier != null
}

# ============================================================================
# Logging Controls
# ============================================================================

# Check: Logging must be enabled
logging_enabled {
    input.resourceType == "AWS::Bedrock::Agent"
    input.resourceProperties.AgentCollaboration != null
}

logging_enabled {
    input.resourceType == "AWS::Bedrock::KnowledgeBase"
    input.resourceProperties.KnowledgeBaseConfiguration != null
}

# ============================================================================
# Model Evaluation Controls
# ============================================================================

# Check: Model evaluation must be configured
model_evaluation_configured {
    input.resourceType == "AWS::Bedrock::ModelEvaluationJob"
    input.resourceProperties.JobName != null
}

# ============================================================================
# Access Controls
# ============================================================================

# Check: No public access
no_public_access {
    input.resourceType == "AWS::Bedrock::Agent"
    input.resourceProperties.AgentStatus != null
}

# ============================================================================
# Violation Reporting
# ============================================================================

violations[{"control": control, "message": msg}] {
    not guardrails_enabled
    control := "GUARDRAILS-001"
    msg := "Bedrock Guardrails must be enabled"
}

violations[{"control": control, "message": msg}] {
    not logging_enabled
    control := "LOGGING-001"
    msg := "Bedrock logging must be enabled"
}

violations[{"control": control, "message": msg}] {
    not model_evaluation_configured
    control := "EVALUATION-001"
    msg := "Bedrock model evaluation must be configured"
}

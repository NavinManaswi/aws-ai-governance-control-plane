# OPA Policy: SageMaker Compliance
# Evaluates SageMaker resources against NIST AI RMF, EU AI Act, and AWS AI Security Best Practices

package sagemaker.compliance

import future.keywords.in

# Default decision: allow if all checks pass
default allow := false

# Main entry point: evaluate all compliance checks
allow {
    encryption_enabled
    vpc_placement
    model_monitoring_enabled
    bias_mitigation_configured
    no_public_access
}

# ============================================================================
# Encryption Controls
# ============================================================================

# Check: Notebook instances must have encryption enabled
encryption_enabled {
    input.resourceType == "AWS::SageMaker::NotebookInstance"
    input.resourceProperties.VolumeEncryptionKeyId != null
}

encryption_enabled {
    input.resourceType == "AWS::SageMaker::Endpoint"
    input.resourceProperties.DataCaptureConfig.EnableCapture == true
}

# Check: Training jobs must use encrypted storage
encryption_enabled {
    input.resourceType == "AWS::SageMaker::TrainingJob"
    input.resourceProperties.OutputDataConfig.S3OutputPath != null
}

# ============================================================================
# Network Controls
# ============================================================================

# Check: Resources must be deployed within VPC
vpc_placement {
    input.resourceType == "AWS::SageMaker::NotebookInstance"
    input.resourceProperties.SubnetId != null
    input.resourceProperties.SecurityGroupIds != null
}

vpc_placement {
    input.resourceType == "AWS::SageMaker::Endpoint"
    input.resourceProperties.SubnetIds != null
    input.resourceProperties.SecurityGroupIds != null
}

# ============================================================================
# Monitoring Controls
# ============================================================================

# Check: Model monitoring must be enabled
model_monitoring_enabled {
    input.resourceType == "AWS::SageMaker::Endpoint"
    input.resourceProperties.DataCaptureConfig.EnableCapture == true
    input.resourceProperties.DataCaptureConfig.InitialSamplingPercentage > 0
}

# ============================================================================
# Bias Mitigation Controls
# ============================================================================

# Check: Bias mitigation must be configured
bias_mitigation_configured {
    input.resourceType == "AWS::SageMaker::Endpoint"
    input.resourceProperties.DataCaptureConfig.EnableCapture == true
    input.resourceProperties.DataCaptureConfig.InitialSamplingPercentage > 0
}

# ============================================================================
# Access Controls
# ============================================================================

# Check: No public access
no_public_access {
    input.resourceType == "AWS::SageMaker::NotebookInstance"
    input.resourceProperties.DirectInternetAccess == "Disabled"
}

# ============================================================================
# Violation Reporting
# ============================================================================

# Generate violation details
violations[{"control": control, "message": msg}] {
    not encryption_enabled
    control := "ENCRYPTION-001"
    msg := "SageMaker resource must have encryption enabled"
}

violations[{"control": control, "message": msg}] {
    not vpc_placement
    control := "NETWORK-001"
    msg := "SageMaker resource must be deployed within VPC"
}

violations[{"control": control, "message": msg}] {
    not model_monitoring_enabled
    control := "MONITORING-001"
    msg := "SageMaker model monitoring must be enabled"
}

violations[{"control": control, "message": msg}] {
    not bias_mitigation_configured
    control := "FAIRNESS-001"
    msg := "SageMaker bias mitigation must be configured"
}

violations[{"control": control, "message": msg}] {
    not no_public_access
    control := "ACCESS-001"
    msg := "SageMaker resource must not have public access"
}

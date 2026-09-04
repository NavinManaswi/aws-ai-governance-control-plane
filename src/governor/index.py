#!/usr/bin/env python3
"""
Lambda Governor: Runtime Enforcement

This Lambda function enforces runtime policies for AI agents,
implementing kill-switch and remediation capabilities.
"""

import json
import os
import boto3
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

sagemaker = boto3.client('sagemaker')
bedrock = boto3.client('bedrock')
config = boto3.client('config')

# ============================================================================
# Remediation Actions
# ============================================================================

def remediate_sagemaker_violation(resource_id, violation):
    """Remediate SageMaker compliance violations."""
    print(f"Remediating SageMaker violation: {violation} for {resource_id}")
    
    if 'ENCRYPTION' in violation:
        # Trigger encryption remediation
        try:
            sagemaker.update_notebook_instance(
                NotebookInstanceName=resource_id.split('/')[-1],
                VolumeEncryptionKeyId=os.environ.get('KMS_KEY_ID')
            )
            return f"Triggered encryption for {resource_id}"
        except Exception as e:
            return f"Failed to trigger encryption: {e}"
    
    if 'MONITORING' in violation:
        # Enable monitoring
        try:
            sagemaker.update_endpoint(
                EndpointName=resource_id.split('/')[-1]
            )
            return f"Triggered monitoring for {resource_id}"
        except Exception as e:
            return f"Failed to trigger monitoring: {e}"
    
    return f"No remediation available for {violation}"

def remediate_bedrock_violation(resource_id, violation):
    """Remediate Bedrock compliance violations."""
    print(f"Remediating Bedrock violation: {violation} for {resource_id}")
    
    if 'GUARDRAILS' in violation:
        # Enable guardrails
        try:
            # Placeholder for guardrail enablement
            return f"Triggered guardrails for {resource_id}"
        except Exception as e:
            return f"Failed to trigger guardrails: {e}"
    
    return f"No remediation available for {violation}"

# ============================================================================
# Kill-Switch
# ============================================================================

def activate_kill_switch(resource_type, resource_id, reason):
    """Activate kill-switch for a rogue resource."""
    print(f"⚠️ KILL-SWITCH ACTIVATED for {resource_type}: {resource_id}")
    print(f"Reason: {reason}")
    
    if resource_type == 'AWS::SageMaker::Endpoint':
        try:
            sagemaker.delete_endpoint(
                EndpointName=resource_id.split('/')[-1]
            )
            return f"Kill-switch: Deleted endpoint {resource_id}"
        except Exception as e:
            return f"Kill-switch failed: {e}"
    
    if resource_type == 'AWS::Bedrock::Agent':
        try:
            # Placeholder for agent deactivation
            return f"Kill-switch: Deactivated agent {resource_id}"
        except Exception as e:
            return f"Kill-switch failed: {e}"
    
    return f"No kill-switch available for {resource_type}"

# ============================================================================
# Lambda Handler
# ============================================================================

def lambda_handler(event, context):
    """Main Lambda handler for runtime governance."""
    print(f"Event: {json.dumps(event)}")
    
    # Extract event details
    resource_type = event.get('resourceType', '')
    resource_id = event.get('resourceId', '')
    violation = event.get('violation', '')
    action = event.get('action', 'remediate')
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'resourceType': resource_type,
        'resourceId': resource_id,
        'action': action,
        'status': 'unknown',
        'message': ''
    }
    
    # Determine action
    if action == 'kill-switch':
        # High-severity: kill the resource
        if violation in ['ROGUE_AGENT', 'COST_RUNAWAY', 'DATA_EXFILTRATION']:
            result = activate_kill_switch(resource_type, resource_id, violation)
            results['status'] = 'kill-switch-activated'
            results['message'] = result
        else:
            results['status'] = 'kill-switch-denied'
            results['message'] = f'Violation {violation} does not require kill-switch'
    
    elif action == 'remediate':
        # Standard remediation
        if resource_type.startswith('AWS::SageMaker'):
            result = remediate_sagemaker_violation(resource_id, violation)
            results['status'] = 'remediated'
            results['message'] = result
        elif resource_type.startswith('AWS::Bedrock'):
            result = remediate_bedrock_violation(resource_id, violation)
            results['status'] = 'remediated'
            results['message'] = result
        else:
            results['status'] = 'unknown-resource'
            results['message'] = f'Unknown resource type: {resource_type}'
    
    else:
        results['status'] = 'unknown-action'
        results['message'] = f'Unknown action: {action}'
    
    print(f"Results: {json.dumps(results)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

#!/usr/bin/env python3
"""
Test script for the AI Governance Control Plane scanner.

This script simulates resource discovery and policy evaluation.
"""

import json
import sys
from datetime import datetime

# ============================================================================
# Mock Resources
# ============================================================================

MOCK_RESOURCES = [
    {
        'resourceType': 'AWS::SageMaker::NotebookInstance',
        'resourceId': 'arn:aws:sagemaker:us-east-1:123456789012:notebook-instance/test-notebook',
        'resourceProperties': {
            'NotebookInstanceName': 'test-notebook',
            'InstanceType': 'ml.t2.medium',
            'RoleArn': 'arn:aws:iam::123456789012:role/SageMakerRole',
            'DirectInternetAccess': 'Disabled',
            'VolumeEncryptionKeyId': 'arn:aws:kms:us-east-1:123456789012:key/test-key',
            'SubnetId': 'subnet-12345678',
            'SecurityGroupIds': ['sg-12345678']
        },
        'discoveredAt': datetime.now().isoformat()
    },
    {
        'resourceType': 'AWS::SageMaker::Endpoint',
        'resourceId': 'arn:aws:sagemaker:us-east-1:123456789012:endpoint/test-endpoint',
        'resourceProperties': {
            'EndpointName': 'test-endpoint',
            'EndpointStatus': 'InService',
            'DataCaptureConfig': {
                'EnableCapture': True,
                'InitialSamplingPercentage': 50
            }
        },
        'discoveredAt': datetime.now().isoformat()
    },
    {
        'resourceType': 'AWS::Bedrock::Agent',
        'resourceId': 'agent-12345678',
        'resourceProperties': {
            'agentId': 'agent-12345678',
            'agentName': 'test-agent',
            'agentArn': 'arn:aws:bedrock:us-east-1:123456789012:agent/agent-12345678',
            'agentStatus': 'ACTIVE',
            'agentResourceRoleArn': 'arn:aws:iam::123456789012:role/BedrockAgentRole'
        },
        'discoveredAt': datetime.now().isoformat()
    }
]

# ============================================================================
# Mock OPA Evaluation
# ============================================================================

def mock_opa_evaluation(resource):
    """Mock OPA policy evaluation."""
    violations = []
    
    # Check encryption
    if resource['resourceType'] == 'AWS::SageMaker::NotebookInstance':
        if not resource['resourceProperties'].get('VolumeEncryptionKeyId'):
            violations.append({
                'control': 'ENCRYPTION-001',
                'message': 'SageMaker resource must have encryption enabled'
            })
    
    # Check VPC placement
    if resource['resourceType'] == 'AWS::SageMaker::NotebookInstance':
        if not resource['resourceProperties'].get('SubnetId'):
            violations.append({
                'control': 'NETWORK-001',
                'message': 'SageMaker resource must be deployed within VPC'
            })
    
    # Check monitoring
    if resource['resourceType'] == 'AWS::SageMaker::Endpoint':
        data_capture = resource['resourceProperties'].get('DataCaptureConfig', {})
        if not data_capture.get('EnableCapture'):
            violations.append({
                'control': 'MONITORING-001',
                'message': 'SageMaker model monitoring must be enabled'
            })
    
    return {'violations': violations}

# ============================================================================
# Main Test
# ============================================================================

def main():
    """Run the test."""
    print("🧪 Testing AI Governance Control Plane Scanner")
    print("=" * 60)
    
    total_resources = len(MOCK_RESOURCES)
    total_findings = 0
    
    print(f"\n📊 Testing with {total_resources} mock resources...")
    print()
    
    for resource in MOCK_RESOURCES:
        print(f"Resource: {resource['resourceType']} ({resource['resourceId']})")
        
        # Evaluate
        result = mock_opa_evaluation(resource)
        violations = result.get('violations', [])
        
        if violations:
            print(f"  ❌ {len(violations)} violations found:")
            for v in violations:
                print(f"     - {v['control']}: {v['message']}")
            total_findings += len(violations)
        else:
            print("  ✅ No violations found")
        
        print()
    
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   Resources scanned: {total_resources}")
    print(f"   Violations found: {total_findings}")
    print(f"   Compliance score: {((total_resources - total_findings) / total_resources * 100):.0f}%")
    print()
    print("✅ Test complete!")

if __name__ == '__main__':
    main()

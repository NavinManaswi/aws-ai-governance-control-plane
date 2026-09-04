#!/usr/bin/env python3
"""
Lambda Scanner: AI Governance Control Plane Scanner

This Lambda function scans AWS AI/ML resources (SageMaker, Bedrock, AgentCore)
and evaluates them against OPA policies and AWS Config rules.
"""

import json
import os
import boto3
import requests
from datetime import datetime

# ============================================================================
# Configuration
# ============================================================================

OPA_ENDPOINT = os.environ.get('OPA_ENDPOINT', 'http://localhost:8181')
SECURITY_HUB_ARN = os.environ.get('SECURITY_HUB_ARN', '')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

sagemaker = boto3.client('sagemaker')
bedrock = boto3.client('bedrock')
config = boto3.client('config')
securityhub = boto3.client('securityhub')
sns = boto3.client('sns')

# ============================================================================
# Resource Discovery
# ============================================================================

def discover_sagemaker_resources():
    """Discover SageMaker resources."""
    resources = []
    
    # Notebook instances
    try:
        response = sagemaker.list_notebook_instances()
        for instance in response.get('NotebookInstances', []):
            resources.append({
                'resourceType': 'AWS::SageMaker::NotebookInstance',
                'resourceId': instance.get('NotebookInstanceArn'),
                'resourceProperties': instance,
                'discoveredAt': datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error discovering SageMaker notebook instances: {e}")
    
    # Endpoints
    try:
        response = sagemaker.list_endpoints()
        for endpoint in response.get('Endpoints', []):
            resources.append({
                'resourceType': 'AWS::SageMaker::Endpoint',
                'resourceId': endpoint.get('EndpointArn'),
                'resourceProperties': endpoint,
                'discoveredAt': datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error discovering SageMaker endpoints: {e}")
    
    return resources

def discover_bedrock_resources():
    """Discover Bedrock resources."""
    resources = []
    
    # Agents
    try:
        response = bedrock.list_agents()
        for agent in response.get('agentSummaries', []):
            resources.append({
                'resourceType': 'AWS::Bedrock::Agent',
                'resourceId': agent.get('agentId'),
                'resourceProperties': agent,
                'discoveredAt': datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error discovering Bedrock agents: {e}")
    
    # Knowledge bases
    try:
        response = bedrock.list_knowledge_bases()
        for kb in response.get('knowledgeBaseSummaries', []):
            resources.append({
                'resourceType': 'AWS::Bedrock::KnowledgeBase',
                'resourceId': kb.get('knowledgeBaseId'),
                'resourceProperties': kb,
                'discoveredAt': datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error discovering Bedrock knowledge bases: {e}")
    
    return resources

# ============================================================================
# Policy Evaluation
# ============================================================================

def evaluate_with_opa(resource, policy_type):
    """Evaluate resource against OPA policy."""
    try:
        payload = {
            'input': {
                'resourceType': resource['resourceType'],
                'resourceId': resource['resourceId'],
                'resourceProperties': resource['resourceProperties']
            }
        }
        
        response = requests.post(
            f"{OPA_ENDPOINT}/v1/data/{policy_type}/compliance",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('result', {})
        else:
            print(f"OPA evaluation failed: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error evaluating with OPA: {e}")
        return {}

# ============================================================================
# Compliance Reporting
# ============================================================================

def send_to_security_hub(findings):
    """Send compliance findings to Security Hub."""
    for finding in findings:
        try:
            securityhub.batch_import_findings(
                Findings=[{
                    'AwsAccountId': boto3.client('sts').get_caller_identity()['Account'],
                    'CreatedAt': datetime.now().isoformat(),
                    'Description': finding.get('message'),
                    'Id': f"ai-governance/{finding.get('control')}/{datetime.now().timestamp()}",
                    'ProductArn': SECURITY_HUB_ARN,
                    'RecordState': 'ACTIVE',
                    'Severity': {
                        'Label': 'MEDIUM' if 'warning' in finding.get('control', '').lower() else 'HIGH'
                    },
                    'Title': f"AI Governance Violation: {finding.get('control')}",
                    'Types': ['Software and Configuration Checks/AWS Security Best Practices'],
                    'Resources': [{
                        'Type': finding.get('resourceType', 'AWS::Unknown'),
                        'Id': finding.get('resourceId', 'unknown')
                    }],
                    'Compliance': {
                        'Status': 'FAILED'
                    }
                }]
            )
        except Exception as e:
            print(f"Error sending to Security Hub: {e}")

def send_to_sns(findings):
    """Send compliance findings to SNS."""
    if not SNS_TOPIC_ARN or not findings:
        return
    
    try:
        message = f"AI Governance Violations Detected\n\n"
        for finding in findings:
            message += f"- {finding.get('control')}: {finding.get('message')}\n"
            message += f"  Resource: {finding.get('resourceId')}\n\n"
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='AI Governance Violation Alert',
            Message=message
        )
    except Exception as e:
        print(f"Error sending to SNS: {e}")

# ============================================================================
# Lambda Handler
# ============================================================================

def lambda_handler(event, context):
    """Main Lambda handler."""
    print(f"Event: {json.dumps(event)}")
    
    all_resources = []
    all_findings = []
    
    # 1. Discover resources
    print("Discovering SageMaker resources...")
    sagemaker_resources = discover_sagemaker_resources()
    all_resources.extend(sagemaker_resources)
    
    print("Discovering Bedrock resources...")
    bedrock_resources = discover_bedrock_resources()
    all_resources.extend(bedrock_resources)
    
    print(f"Total resources discovered: {len(all_resources)}")
    
    # 2. Evaluate resources
    for resource in all_resources:
        if resource['resourceType'].startswith('AWS::SageMaker'):
            result = evaluate_with_opa(resource, 'sagemaker')
        elif resource['resourceType'].startswith('AWS::Bedrock'):
            result = evaluate_with_opa(resource, 'bedrock')
        else:
            continue
        
        # Collect violations
        violations = result.get('violations', [])
        for violation in violations:
            finding = {
                'resourceType': resource['resourceType'],
                'resourceId': resource['resourceId'],
                'control': violation.get('control'),
                'message': violation.get('message'),
                'timestamp': datetime.now().isoformat()
            }
            all_findings.append(finding)
    
    # 3. Report findings
    print(f"Total findings: {len(all_findings)}")
    
    if all_findings:
        send_to_security_hub(all_findings)
        send_to_sns(all_findings)
    
    # 4. Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'resourcesScanned': len(all_resources),
            'findings': len(all_findings)
        })
    }

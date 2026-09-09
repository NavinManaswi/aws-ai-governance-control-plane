Fuser
# 🛡️ AWS AI Governance Control Plane

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![AWS](https://img.shields.io/badge/AWS-Certified-orange.svg)]()
[![NIST AI RMF](https://img.shields.io/badge/NIST%20AI%20RMF-Aligned-green.svg)]()
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Ready-blue.svg)]()
[![ISO 42001](https://img.shields.io/badge/ISO%2042001-Mapped-purple.svg)]()

---

## 📋 Table of Contents

- [About This Project](#-about-this-project)
- [Why This Matters](#-why-this-matters)
- [Architecture](#-architecture)
- [AWS Services Used](#-aws-services-used)
- [GRC Frameworks Addressed](#-grc-frameworks-addressed)
- [Quick Start](#-quick-start)
- [What's Inside](#-whats-inside)
- [Key Artifacts](#-key-artifacts)
- [Compliance Dashboard](#-compliance-dashboard)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 About This Project

This project implements a **serverless, automated AI governance control plane** on AWS that continuously scans, evaluates, and remediates AI/ML resources against regulatory frameworks.

**What it does:**

| Capability | Description |
|------------|-------------|
| 🔍 **Continuous Scanning** | Event-driven evaluation of SageMaker, Bedrock, and AgentCore resources |
| 📋 **Policy-as-Code** | OPA and Cedar policies for declarative compliance enforcement |
| 🚨 **Automated Alerting** | Security Hub findings + SNS notifications for violations |
| 📊 **Executive Dashboard** | QuickSight dashboard with real-time compliance metrics |
| 📁 **Audit Evidence** | Automated evidence collection via AWS Audit Manager |
| 🔄 **Self-Healing** | Automated remediation for common compliance violations |

**Organization:** NovaTech Financial Group *(hypothetical)*  
**Effective Date:** September 2026  
**Version:** 1.0

---

## 🚨 Why This Matters

### The Enforcement Era Is Here

- **EU AI Act** enforcement provisions went live in August 2026[reference:0]
- **AWS Security Hub CSPM** launched the **AI Security Best Practices standard** with **31 automated controls** covering network isolation, encryption, VPC placement, KMS key usage, and authorization controls[reference:1][reference:2]
- **AWS Config** now supports **9 new resource types** across Bedrock, Bedrock AgentCore, and SageMaker[reference:3]
- **NIST AI RMF** and **ISO/IEC 42001** provide the governance framework[reference:4]

### The Gap This Project Fills

| Challenge | How This Project Solves It |
|-----------|----------------------------|
| Manual compliance checks are slow and error-prone | Automated, event-driven scanning |
| Shadow AI resources go unnoticed | Continuous discovery and inventory |
| Audit evidence is scattered across systems | Centralized evidence collection |
| No real-time visibility into compliance posture | Executive dashboard |
| Regulatory requirements are complex | Policy-as-code with framework mappings |

---

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────────────┐
│ CONTROL PLANE (Governance) │
├─────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │ EventBridge │ │ EventBridge │ │
│ │ (Scheduled) │ │ (Resource Changes)│ │
│ └────────┬────────┘ └────────┬────────┘ │
│ │ │ │
│ └────────────┬───────────┘ │
│ ▼ │
│ ┌─────────────────────────┐ │
│ │ Lambda Scanner │ │
│ │ (Evaluates resources) │ │
│ └────────────┬────────────┘ │
│ │ │
│ ┌────────────┼────────────┐ │
│ ▼ ▼ ▼ │
│ ┌─────────────────┐ ┌──────────┐ ┌─────────────────┐ │
│ │ OPA Engine │ │ Cedar │ │ Bedrock │ │
│ │ (Policy-as- │ │ Engine │ │ Guardrails │ │
│ │ Code) │ │ │ │ │ │
│ └─────────────────┘ └──────────┘ └─────────────────┘ │
│ │ │ │ │
│ └────────────┼────────────┘ │
│ ▼ │
│ ┌─────────────────────────┐ │
│ │ AWS Config │ │
│ │ (Records compliance) │ │
│ └────────────┬────────────┘ │
│ │ │
│ ┌────────────┼────────────┐ │
│ ▼ ▼ ▼ │
│ ┌─────────────────┐ ┌──────────┐ ┌─────────────────┐ │
│ │ Security Hub │ │ SNS │ │ Lambda │ │
│ │ (Findings) │ │ (Alerts) │ │ Governor │ │
│ └─────────────────┘ └──────────┘ │ (Remediation) │ │
│ └─────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────┐ │
│ │ AWS Audit Manager │ │
│ │ (Evidence Collection) │ │
│ └─────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘


---

## 🔧 AWS Services Used

| Service | Purpose | Latest Feature |
|---------|---------|----------------|
| **Amazon EventBridge** | Trigger scans on schedule and resource changes | — |
| **AWS Lambda** | Serverless scanner, governor, and aggregator | — |
| **Open Policy Agent (OPA)** | Policy-as-code evaluation engine | Stateless interceptor for tool-calling validation[reference:5] |
| **AWS Cedar** | Fine-grained authorization for AI agents[reference:6] | Policy feature in Bedrock AgentCore[reference:7] |
| **Amazon Bedrock Guardrails** | Runtime safety and compliance policies[reference:8] | Baseline guardrails via Bedrock Policies[reference:9] |
| **AWS Config** | Continuous compliance recording[reference:10] | 9 new resource types for AI/ML[reference:11]; 191 new managed rules[reference:12] |
| **AWS Security Hub CSPM** | Centralized security findings[reference:13] | AI Security Best Practices standard (31 controls)[reference:14] |
| **Amazon SNS** | Alerting on violations | — |
| **AWS Audit Manager** | Automated evidence collection[reference:15] | AWS generative AI best practices framework[reference:16] |
| **Amazon QuickSight** | Executive compliance dashboard | — |

---

## 📋 GRC Frameworks Addressed

| Framework | How It's Addressed |
|-----------|-------------------|
| **EU AI Act (Art. 9, 11, 15)** | Continuous risk assessment; automated technical documentation; accuracy & robustness monitoring[reference:17] |
| **NIST AI RMF** | MAP (inventory), MEASURE (monitoring), MANAGE (remediation), GOVERN (policies)[reference:18] |
| **ISO/IEC 42001** | Clause 8 (Operation) — lifecycle controls; Clause 9 (Evaluation) — monitoring[reference:19] |
| **AWS AI Security Best Practices** | 31 automated controls[reference:20] |

---

## 🚀 Quick Start

| Step | Action | Command |
|------|--------|---------|
| **1** | Clone the repository | `git clone https://github.com/yourusername/aws-ai-governance-control-plane.git` |
| **2** | Navigate to the project | `cd aws-ai-governance-control-plane` |
| **3** | Deploy the infrastructure | `./scripts/deploy.sh` |
| **4** | Test the scanner | `python scripts/test-scanner.py` |
| **5** | View the dashboard | Open QuickSight and navigate to the AI Governance dashboard |

---

## 📂 What's Inside

| Folder | Description |
|--------|-------------|
| **infrastructure/** | SAM / CloudFormation templates for one-click deployment |
| **src/scanner/** | Lambda scanner that evaluates AI resources against policies |
| **src/governor/** | Lambda governor that enforces runtime policies |
| **src/aggregator/** | Lambda aggregator that consolidates compliance data |
| **policies/opa/** | Rego policies for SageMaker, Bedrock, and AgentCore compliance |
| **policies/cedar/** | Cedar policies for fine-grained agent authorization |
| **policies/guardrails/** | Bedrock Guardrails policies |
| **config-rules/** | AWS Config conformance pack for AI Security Best Practices |
| **audit-framework/** | AWS Audit Manager framework for AI governance |
| **dashboard/** | QuickSight dashboard definition |
| **scripts/** | Deployment and testing scripts |
| **.github/workflows/** | CI/CD pipeline |

---

## 🏆 Key Artifacts

### 1. [OPA Policies](policies/opa/)
Policy-as-code enforcement for AI resources:
- `sagemaker-compliance.rego` — Encryption, VPC, bias monitoring
- `bedrock-compliance.rego` — Guardrails, logging, model evaluation
- `agentcore-compliance.rego` — Identity, authorization, runtime

### 2. [Cedar Policies](policies/cedar/)
Fine-grained authorization for AI agents[reference:21]:
- `agent-permissions.cedar` — Who can perform which actions on what resources

### 3. [AWS Config Conformance Pack](config-rules/ai-security-best-practices.yaml)
31 automated controls for AI Security Best Practices[reference:22]:
- Network isolation, encryption, VPC placement, KMS key usage, authorization

### 4. [AWS Audit Manager Framework](audit-framework/ai-governance-framework.json)
Automated evidence collection for AI governance[reference:23]

---

## 📊 Compliance Dashboard

The QuickSight dashboard provides real-time visibility into:

| Metric | Description |
|--------|-------------|
| **Compliance Score** | Overall percentage of resources in compliance |
| **Resource Inventory** | Count of SageMaker, Bedrock, and AgentCore resources |
| **Violations by Control** | Top violated controls |
| **Violations by Service** | Compliance breakdown by service |
| **Trend Analysis** | Compliance trends over time |

---

## 🚀 Deployment

### Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.11+ installed
- Node.js 18+ installed (for CDK alternative)

### One-Click Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/aws-ai-governance-control-plane.git
cd aws-ai-governance-control-plane

# Deploy using SAM
sam build
sam deploy --guided

 ## Manual Deployment
# Deploy infrastructure
aws cloudformation deploy \
  --template-file infrastructure/template.yaml \
  --stack-name ai-governance-control-plane \
  --parameter-overrides file://infrastructure/parameter-overrides.json \
  --capabilities CAPABILITY_IAM

# Deploy OPA policies to S3
aws s3 sync policies/opa/ s3://your-bucket/policies/opa/

# Deploy Config conformance pack
aws config put-conformance-pack \
  --conformance-pack-name ai-security-best-practices \
  --template-body file://config-rules/ai-security-best-practices.yaml

📫 Contact
Channel	Details
GitHub	github.com/NavinManaswi
LinkedIn	linkedin.com/in/NavinManaswi
Email	manaswink@gmail.com
📝 License
This project is licensed under the MIT License.

⭐ Star This Repository
If you find this project helpful, please star this repository and share it with your network!

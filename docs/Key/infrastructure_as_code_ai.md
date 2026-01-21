# Infrastructure as Code (IaC) with AI

## What is AI for IaC?
Infrastructure as Code (IaC) is the practice of managing and provisioning computing infrastructure (servers, networks, load balancers) through machine-readable definition files rather than physical hardware configuration or interactive configuration tools. AI assists in writing, optimizing, and translating these configurations.

## Key Technologies
*   **Terraform (HCL)**: Cloud-agnostic infrastructure provisioning.
*   **Kubernetes (YAML)**: Container orchestration manifests.
*   **Ansible (YAML)**: Configuration management.
*   **Docker (Dockerfile)**: Container image definitions.

## AI Use Cases

### 1. Code Generation
*   **Prompt**: "Create a Terraform module for an AWS VPC with public and private subnets and a NAT gateway."
*   **AI Output**: Generates the complete `.tf` file with correct resource blocks, variables, and outputs.
*   **Benefit**: Reduces the need to memorize complex syntax and cloud provider APIs.

### 2. Translation / Migration
*   **Task**: Converting infrastructure definitions from one format to another.
*   **Example**: "Convert this AWS CloudFormation template to Terraform HCL."
*   **Example**: "Convert this Docker Compose file to a Kubernetes Deployment and Service manifest."

### 3. Optimization & Cost Estimation
*   AI can analyze existing IaC files and suggest changes to reduce costs (e.g., "You are using a `t3.large` but CPU usage is low; switch to `t3.medium`").
*   Identifying unused resources (zombie infrastructure).

### 4. Policy as Code Generation
*   Generating policy files (e.g., Open Policy Agent / Rego) to enforce security rules.
*   *Example*: "Write a policy that forbids creating S3 buckets without encryption."

## Tools
*   **GitHub Copilot**: Works well with HCL and YAML.
*   **Pulumi AI**: Allows defining infrastructure using natural language.
*   **K8sGPT**: Scans Kubernetes clusters, diagnoses issues, and explains them in plain English.

## Challenges
*   **Drift**: AI might generate code that conflicts with the current state of the infrastructure if it doesn't have access to the state file.
*   **Security**: AI might suggest insecure defaults (e.g., `0.0.0.0/0` for security groups) if not prompted correctly.

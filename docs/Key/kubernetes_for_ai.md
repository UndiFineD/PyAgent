# Kubernetes for AI

## Why Kubernetes (K8s) for AI?
Kubernetes is the de facto standard for container orchestration. While originally designed for microservices, it has become the backbone of scalable AI infrastructure because:
1.  **Scalability**: It can spin up 100 GPU nodes for a training job and spin them down when done (Autoscaling).
2.  **Resource Management**: It handles the allocation of expensive hardware (GPUs/TPUs) to different teams and jobs (Quotas).
3.  **Portability**: A training job defined in K8s runs the same on AWS, Google Cloud, or an on-prem supercomputer.

## Key Ecosystem Tools

### 1. Kubeflow
*   **What is it?**: The "ML Toolkit for Kubernetes." A suite of tools to make deploying ML workflows on K8s simple.
*   **Components**:
    *   **Kubeflow Pipelines (KFP)**: Defining multi-step workflows (Data Prep -> Train -> Evaluate) as code (Python DSL).
    *   **Katib**: Hyperparameter tuning.
    *   **Notebooks**: Spawning Jupyter servers for users.

### 2. Ray
*   **What is it?**: A unified compute framework for scaling Python applications.
*   **Ray on K8s (KubeRay)**: Allows running distributed Python code (like training a massive LLM across 100 GPUs) easily.
*   **Ray Serve**: A scalable model serving library.

### 3. KServe
*   **What is it?**: A standard for Model Inference on Kubernetes.
*   **Features**: Serverless inference (scale-to-zero when no traffic), canary rollouts, and standardized protocols (V2 Inference Protocol).

## Challenges
*   **Complexity**: Kubernetes is notoriously difficult to manage ("Day 2 Operations").
*   **Scheduling**: Default K8s scheduling is not optimized for AI (e.g., it might split a distributed training job across racks with slow interconnects). Tools like **Volcano** or **YuniKorn** are used for batch scheduling.

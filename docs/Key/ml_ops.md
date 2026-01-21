# MLOps (Machine Learning Operations)

Applying DevOps principles to Machine Learning systems. It aims to unify ML system development (Dev) and ML system operation (Ops).

## 1. The ML Lifecycle

1.  **Data Engineering**: Ingestion, cleaning, and feature extraction.
2.  **Model Development**: Experimentation, training, and hyperparameter tuning.
3.  **Deployment**: Serving the model via API (REST/gRPC).
4.  **Monitoring**: Tracking performance in production.

## 2. Key Components

*   **Feature Store**: A centralized repository for features (e.g., "User Average Spend"). Ensures that the model uses the exact same feature definition during Training and Inference.
*   **Model Registry**: A version control system for binary model files (e.g., MLflow). Tracks lineage: "Model v2.1 was trained on Dataset v5 using Code commit `abc123`."
*   **Pipeline Orchestration**: Tools like Airflow or Kubeflow to automate the workflow (Data -> Train -> Evaluate -> Deploy).

## 3. Monitoring & Drift

*   **Data Drift**: The input data distribution changes over time (e.g., users start buying different things in Summer vs. Winter).
*   **Concept Drift**: The relationship between inputs and outputs changes (e.g., "Spam" emails look different today than 5 years ago).
*   **Training-Serving Skew**: When the model performs well in training but fails in production due to subtle differences in the environment.

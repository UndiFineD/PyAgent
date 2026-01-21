# Feature Stores

## What is a Feature Store?
A Feature Store is a centralized data management layer for Machine Learning. It allows data scientists to define, store, and serve features (inputs for ML models) consistently for both training and inference.

## The Problem it Solves
*   **Training-Serving Skew**: A common bug where the code used to calculate a feature during training (e.g., in a Python notebook) differs slightly from the code used in production (e.g., in a Java microservice), leading to poor model performance.
*   **Duplication**: Different teams re-implementing the same feature (e.g., "User's average spend over 30 days") differently.

## Core Components

### 1. Offline Store
*   **Storage**: Cheap, high-capacity storage (Data Warehouse, S3, BigQuery).
*   **Use Case**: Storing months or years of historical feature data.
*   **Purpose**: Generating training datasets.

### 2. Online Store
*   **Storage**: Low-latency key-value store (Redis, DynamoDB, Cassandra).
*   **Use Case**: Storing only the *latest* value of a feature.
*   **Purpose**: Serving features to the model in real-time (millisecond latency) during inference.

### 3. Feature Registry
*   A catalog defining feature definitions, metadata, and ownership.

## How it Works
1.  **Feature Engineering**: A data engineer writes a pipeline to calculate "User Click Rate".
2.  **Materialization**: The Feature Store computes this value and saves it to both the Offline Store (history) and Online Store (current).
3.  **Training**: The data scientist queries the Offline Store: "Get me the click rate for User X on date Y."
4.  **Inference**: The production app queries the Online Store: "Get me the current click rate for User X."

## Tools
*   **Feast**: Open-source feature store.
*   **Tecton**: Enterprise feature platform (built by the team that created Uber Michelangelo).
*   **SageMaker Feature Store**: AWS managed offering.

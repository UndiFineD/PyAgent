# Experiment Tracking

## The "Spreadsheet Hell"
In traditional software, you write code, compile, and run. In Machine Learning, you run the same code hundreds of times with slightly different settings:
*   Learning Rate: 0.01 vs 0.001?
*   Batch Size: 32 vs 64?
*   Model Architecture: ResNet50 vs ResNet101?
*   Dataset Version: v1 vs v2?

Without a tool, data scientists end up with filenames like `model_final_v2_lr001_best.pth` and lose track of which combination produced the best result.

## What is Experiment Tracking?
It is the practice of automatically logging all metadata, parameters, metrics, and artifacts associated with every training run.

## Key Metrics to Track
1.  **Parameters (Inputs)**: Hyperparameters (LR, epochs, optimizer), Git commit hash, Dataset hash.
2.  **Metrics (Outputs)**: Loss curves (train/val), Accuracy, F1-Score, Latency.
3.  **Artifacts**: The saved model weights (`.pt`, `.h5`), confusion matrices, sample predictions (images/text).

## Tools

### 1. MLflow
*   **Type**: Open Source.
*   **Features**: Tracking, Projects (packaging), Models (serving), and Registry.
*   **Pros**: Can be hosted locally or on any cloud. Standard in many enterprises.

### 2. Weights & Biases (W&B)
*   **Type**: SaaS (Freemium).
*   **Features**: Beautiful visualizations, collaborative reports, system metrics (GPU usage).
*   **Pros**: The "GitHub for ML experiments." Extremely popular in the research community.

### 3. TensorBoard
*   **Type**: Open Source (Google).
*   **Features**: Visualization of loss curves and model graphs.
*   **Pros**: Built into TensorFlow/PyTorch. Good for real-time debugging but less good for comparing 100 historical runs.

## Benefits
*   **Comparability**: Overlaying loss curves from 10 different runs to see which converged faster.
*   **Reproducibility**: Being able to click on the best result and know exactly which Git commit and parameters produced it.

# Online Learning

Training a model incrementally as data arrives in a stream, rather than retraining from scratch on a static dataset.

## 1. Use Cases

*   **Stock Market Prediction**: The market changes every second. A model trained on last year's data is useless.
*   **Ad Click Prediction**: User preferences change instantly based on trends.
*   **IoT Sensors**: Devices with limited memory cannot store a massive dataset; they must learn and discard data on the fly.

## 2. Challenges

*   **Catastrophic Forgetting**: The model learns the new data but forgets the old data.
    *   *Solution*: Replay Buffers (store a small sample of old data) or Elastic Weight Consolidation (prevent important weights from changing too much).
*   **Concept Drift**: The underlying relationship changes (e.g., "Spam" definition changes). The model must adapt quickly.

## 3. Algorithms

*   **Stochastic Gradient Descent (SGD)**: Naturally supports online learning (batch size = 1).
*   **River**: A Python library specifically designed for online machine learning.
*   **Hoeffding Trees**: Decision trees that can grow incrementally as new data arrives.

# Loss Functions

The mathematical objective function $J(\theta)$ that the model tries to minimize. It measures the difference between the prediction $\hat{y}$ and the ground truth $y$.

## 1. Regression Losses (Predicting Numbers)

*   **MSE (Mean Squared Error)**: $\frac{1}{N} \sum (y - \hat{y})^2$.
    *   Penalizes large errors heavily (due to the square). Sensitive to outliers.
*   **MAE (Mean Absolute Error)**: $\frac{1}{N} \sum |y - \hat{y}|$.
    *   More robust to outliers.
*   **Huber Loss**: Combination of MSE (near 0) and MAE (far from 0). Best of both worlds.

## 2. Classification Losses (Predicting Categories)

*   **Cross-Entropy Loss (Log Loss)**: $-\sum y \log(\hat{y})$.
    *   The standard for classification. Penalizes confident wrong answers heavily.
*   **Focal Loss**: A modification of Cross-Entropy that down-weights easy examples (background) and focuses on hard examples (rare objects).
    *   Essential for Object Detection (RetinaNet) where 99% of the image is background.

## 3. Metric Learning Losses (Similarity)

*   **Triplet Loss**: Uses three inputs: Anchor ($A$), Positive ($P$), Negative ($N$).
    *   Goal: $Distance(A, P) < Distance(A, N) + Margin$.
    *   Used in Face Recognition (FaceNet).
*   **Contrastive Loss**: Pulls similar pairs together, pushes dissimilar pairs apart.

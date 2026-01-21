# Ensemble Learning

The wisdom of crowds for Machine Learning. Combining multiple models often yields better results than any single model.

## 1. Bagging (Bootstrap Aggregating)

*   **Concept**: Train multiple models independently on random subsets of the data (with replacement) and average their predictions.
*   **Goal**: Reduces **Variance** (Overfitting).
*   **Example**: **Random Forest**. It trains hundreds of Decision Trees. If one tree overfits to a specific noise pattern, the others likely won't, so the average is stable.

## 2. Boosting

*   **Concept**: Train models sequentially. Each new model focuses on correcting the errors made by the previous ones.
*   **Goal**: Reduces **Bias** (Underfitting).
*   **Examples**:
    *   **XGBoost / LightGBM**: Gradient Boosting Machines. The state-of-the-art for tabular data (Excel sheets).
    *   **AdaBoost**: Increases the weight of misclassified data points.

## 3. Stacking

*   **Concept**: Train a "Meta-Model" (or Blender) to combine the predictions of base models.
*   **Workflow**:
    1.  Train Model A (SVM) and Model B (Neural Net).
    2.  Feed their predictions ($P_A, P_B$) into Model C (Logistic Regression).
    3.  Model C learns: "When Model A is confident but Model B is unsure, trust Model A."

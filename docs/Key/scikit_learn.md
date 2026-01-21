# Scikit-Learn (sklearn)

Scikit-Learn is the most popular Python library for classical machine learning. It is built on top of NumPy, SciPy, and Matplotlib. Even in the age of Deep Learning, it remains essential for preprocessing, baselines, and simpler models.

## Key Algorithms

### 1. Supervised Learning
*   **Regression**: Linear Regression, Ridge/Lasso (Regularization), Support Vector Regression (SVR).
*   **Classification**: Logistic Regression, Support Vector Machines (SVM), Decision Trees, Random Forests, Gradient Boosting (though XGBoost/LightGBM are often preferred for speed).

### 2. Unsupervised Learning
*   **Clustering**: K-Means, DBSCAN (density-based), Hierarchical Clustering.
*   **Dimensionality Reduction**: PCA (Principal Component Analysis), t-SNE.

## The Unified API
The genius of Scikit-Learn is its consistent interface. Almost every object follows this pattern:
*   `estimator.fit(X, y)`: Train the model.
*   `estimator.predict(X)`: Make predictions.
*   `transformer.fit(X)`: Learn parameters (e.g., mean/std for scaling).
*   `transformer.transform(X)`: Apply the transformation.
*   `transformer.fit_transform(X)`: Do both efficiently.

## Pipelines
A tool to chain multiple steps together (preprocessing -> feature selection -> model) into a single object.
*   **Benefit 1**: Prevents **Data Leakage**. When you call `cross_val_score` on a pipeline, the preprocessing is fitted *only* on the training fold, not the validation fold.
*   **Benefit 2**: Reproducibility. You can save the entire pipeline as a pickle file.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
pipe.fit(X_train, y_train)
```

## Model Selection & Evaluation
*   **Cross-Validation**: `KFold`, `StratifiedKFold` (preserves class balance).
*   **Grid Search**: `GridSearchCV` exhaustively searches through a specified parameter grid.
*   **Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC.

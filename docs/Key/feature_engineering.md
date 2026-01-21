# Feature Engineering

Feature Engineering is the art and science of transforming raw data into features that better represent the underlying problem to the predictive models, resulting in improved model accuracy on unseen data.

## Numerical Features

### 1. Scaling and Normalization
*   **Min-Max Scaling**: Rescales data to a fixed range, usually [0, 1]. Sensitive to outliers.
*   **Standardization (Z-score)**: Rescales data to have a mean of 0 and a standard deviation of 1. Better for algorithms that assume a Gaussian distribution (e.g., Logistic Regression, SVMs).
*   **Log Transformation**: Applies a log function to handle skewed data (e.g., income, population).

### 2. Binning / Discretization
Converting continuous variables into categorical buckets.
*   **Example**: Converting `Age` (18, 25, 60) into `Age_Group` (Young, Adult, Senior).
*   **Why**: Handles non-linear relationships and outliers.

## Categorical Features

### 1. One-Hot Encoding
Creates a new binary column for each category.
*   **Pros**: Simple, works well for nominal data.
*   **Cons**: Creates high dimensionality (curse of dimensionality) if cardinality is high (e.g., Zip Codes).

### 2. Label Encoding / Ordinal Encoding
Assigns an integer to each category.
*   **Pros**: Compact.
*   **Cons**: Implies an order (0 < 1 < 2) which might not exist (e.g., Red < Blue < Green is false).

### 3. Target Encoding (Mean Encoding)
Replaces a category with the mean of the target variable for that category.
*   **Risk**: High risk of data leakage and overfitting. Requires smoothing or cross-validation.

### 4. Embeddings
Learning a dense vector representation for high-cardinality categories.
*   **Entity Embeddings**: Used in neural networks to map categories (like UserID or ProductID) to a low-dimensional space where similar items are close together.

## Text and Sequence Features

### 1. Bag of Words (BoW) & TF-IDF
*   **BoW**: Counts word frequencies.
*   **TF-IDF**: Weighs words by how unique they are to a document across the corpus.

### 2. N-Grams
Captures context by grouping adjacent words (e.g., "New York" vs "New" and "York").

## Dimensionality Reduction
Reducing the number of features while keeping the most important information.
*   **PCA (Principal Component Analysis)**: Linear transformation to find axes of maximum variance.
*   **t-SNE / UMAP**: Non-linear techniques for visualization.
*   **Feature Selection**: Removing features with low variance or high correlation (multicollinearity).

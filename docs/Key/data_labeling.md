# Data Labeling Strategies

Data Labeling is the process of adding meaningful tags or annotations to raw data (images, text, audio) so that a machine learning model can learn from it. It is often the most expensive and time-consuming part of the ML lifecycle.

## Types of Labeling

### 1. Manual Labeling (Human-in-the-Loop)
*   **In-House**: Domain experts (e.g., doctors labeling X-rays) annotate data. High quality, high cost.
*   **Crowdsourcing**: Platforms like Amazon Mechanical Turk or Scale AI distribute tasks to thousands of workers. Lower cost, variable quality.
*   **Best For**: Gold-standard test sets and complex tasks requiring human intuition.

### 2. Semi-Supervised Learning
Using a small amount of labeled data to label a large amount of unlabeled data.
*   **Self-Training**: Train a model on the small labeled set, use it to predict labels for the unlabeled set, and add high-confidence predictions to the training set.
*   **Label Propagation**: In a graph structure, propagate labels from labeled nodes to nearby unlabeled nodes.

### 3. Weak Supervision (Programmatic Labeling)
Instead of labeling individual data points, experts write **Labeling Functions** (heuristics) that output noisy labels.
*   **Example**: `def check_spam(text): if "buy now" in text return SPAM else ABSTAIN`
*   **Snorkel**: A famous framework that combines multiple noisy labeling functions using a generative model to estimate the true label.
*   **Impact**: Reduces labeling time from months to days.

### 4. Active Learning
A strategy where the model selects the most "confusing" or informative data points and asks a human to label only those.
*   **Uncertainty Sampling**: Pick samples where the model's prediction probability is near 0.5.
*   **Diversity Sampling**: Pick samples that are very different from what the model has seen before.
*   **Impact**: Achieving the same model performance with 10x fewer labeled examples.

### 5. Synthetic Data Generation
Using AI to generate labeled data from scratch.
*   **Computer Vision**: Rendering 3D scenes (Unity/Unreal Engine) where the labels (segmentation masks, depth maps) are known perfectly.
*   **NLP**: Using GPT-4 to generate instruction-tuning datasets (e.g., Alpaca, Evol-Instruct).

## Quality Control
*   **Inter-Annotator Agreement (IAA)**: Measuring how often different humans agree on the same label (Cohen's Kappa).
*   **Consensus Voting**: Asking 3 people to label the same item and taking the majority vote.

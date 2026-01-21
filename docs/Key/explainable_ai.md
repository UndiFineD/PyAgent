# Explainable AI (XAI)

Deep Learning models are "Black Boxes." They output a decision (e.g., "Loan Denied"), but they don't tell you *why*. **Explainable AI (XAI)** is the field of making these decisions transparent and interpretable to humans.

## 1. Why XAI?

*   **Trust**: A doctor won't trust an AI diagnosis unless they know the symptoms it looked at.
*   **Debugging**: If a model classifies a Husky as a Wolf, XAI can reveal it was looking at the *snow* in the background, not the animal (Spurious Correlation).
*   **Regulation**: Laws like GDPR ("Right to Explanation") require companies to explain automated decisions.

## 2. Local vs. Global Explanations

*   **Local**: Why did the model make *this specific* prediction? (e.g., "Why was *my* loan denied?")
*   **Global**: How does the model work in general? (e.g., "What features are most important for loan approval?")

## 3. Key Techniques

### A. SHAP (SHapley Additive exPlanations)
Based on Game Theory. It calculates the contribution of each feature to the prediction.
*   *Example*: "Income +$500, Age +$20, Debt -$1000 = Score 400."
*   It is model-agnostic (works for XGBoost, Neural Nets, etc.) and mathematically consistent.

### B. LIME (Local Interpretable Model-agnostic Explanations)
Approximates the complex neural network with a simple linear model *locally* around the specific data point.
*   It perturbs the input (changes pixels, removes words) and sees how the prediction changes.

### C. Saliency Maps (for Vision)
Visualizing which pixels in an image influenced the output the most.
*   **Grad-CAM**: Uses the gradients flowing into the final convolutional layer to highlight the "hot" regions (e.g., the dog's face).

## 4. The Interpretability-Accuracy Tradeoff

Generally, the most accurate models (Deep Neural Nets, Ensembles) are the hardest to explain. The most explainable models (Linear Regression, Decision Trees) are less accurate. XAI tries to bridge this gap.

# AI Ethics & Fairness

As AI systems make decisions about loans, hiring, and healthcare, ensuring they are fair and unbiased is critical.

## 1. Sources of Bias

*   **Historical Bias**: The training data reflects historical prejudices (e.g., a hiring model trained on past resumes might prefer men if the company historically hired men).
*   **Representation Bias**: Certain groups are underrepresented in the dataset (e.g., facial recognition failing on darker skin tones).
*   **Measurement Bias**: The labels are proxies, not the truth (e.g., using "arrest rate" as a proxy for "crime rate").

## 2. Fairness Metrics

*   **Demographic Parity**: The acceptance rate should be the same for all groups (e.g., 50% of men and 50% of women get the loan).
*   **Equalized Odds**: The True Positive Rate and False Positive Rate should be the same across groups.
*   **Counterfactual Fairness**: "Would the decision have been the same if the applicant were Black instead of White, with all other features adjusted accordingly?"

## 3. Mitigation

*   **Pre-processing**: Re-weighting the dataset to balance groups.
*   **In-processing**: Adding a "Fairness Penalty" to the Loss Function during training.
*   **Post-processing**: Adjusting the model's thresholds after training to achieve parity.

# Privacy Attacks and Defenses in AI

As AI models are trained on sensitive data (medical records, emails, code), the risk of them leaking this information has created a new field of "Privacy-Preserving Machine Learning."

## 1. The Attacks: How Models Leak Data

### Membership Inference Attack (MIA)
- **Goal**: Determine if a specific data point (e.g., John Doe's medical record) was used to train the model.
- **Mechanism**: Models often "overfit" slightly to their training data. If the model is more confident (lower loss) on John's record than on a random record, an attacker can infer John was in the training set.
- **Risk**: Reveals sensitive attributes (e.g., if the model was trained on "Patients with HIV," membership implies HIV status).

### Model Inversion Attack
- **Goal**: Reconstruct the training data from the model outputs.
- **Mechanism**: By repeatedly querying the model and optimizing the input to maximize a specific class probability (e.g., "Face ID: John"), an attacker can generate an image that looks like John.

### Extraction Attack
- **Goal**: Steal the model itself (weights/architecture).
- **Mechanism**: Query the model with many inputs to train a "shadow model" that mimics the victim model's behavior.

## 2. The Defenses: Protecting Data

### Differential Privacy (DP)
The gold standard for privacy.
- **Definition**: An algorithm is differentially private if its output doesn't change significantly whether any *single* individual is in the dataset or not.
- **DP-SGD (Differentially Private Stochastic Gradient Descent)**:
    1.  **Clip Gradients**: Limit how much any single data point can influence the model update.
    2.  **Add Noise**: Add random Gaussian noise to the gradients before updating the weights.
- **Trade-off**: DP usually reduces model accuracy.

### Federated Learning (FL)
- **Concept**: Train the model on the user's device (edge), not on a central server.
- **Mechanism**:
    1.  Server sends global model to devices.
    2.  Devices train locally on private data.
    3.  Devices send *updates* (gradients) back to server.
    4.  Server aggregates updates to improve global model.
- **Privacy**: Raw data never leaves the device. (Note: Gradients can still leak info, so FL is often combined with DP).

### Machine Unlearning
- **Goal**: Remove the influence of specific data points from a trained model (e.g., "Right to be Forgotten").
- **Challenge**: Retraining from scratch is expensive.
- **Methods**: SISA (Sharded, Isolated, Sliced, Aggregated) training allows retraining only a small fraction of the model.

## Summary

| Attack | Goal | Defense |
| :--- | :--- | :--- |
| **Membership Inference** | Was this data used? | Differential Privacy (DP-SGD) |
| **Model Inversion** | Reconstruct input data | Differential Privacy / Gradient Clipping |
| **Model Extraction** | Steal the model | API Rate Limiting / Watermarking |

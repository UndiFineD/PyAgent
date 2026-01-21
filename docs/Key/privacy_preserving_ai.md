# Privacy-Preserving AI

Techniques to train and use AI models without exposing sensitive user data (Medical records, Financial data).

## 1. Differential Privacy (DP)

*   **Concept**: Adding calculated noise to the data (or gradients) so that the output of the model is statistically the same whether *any single individual* is in the dataset or not.
*   **Epsilon ($\epsilon$)**: The "Privacy Budget." A lower $\epsilon$ means more privacy but less accuracy.
*   **DP-SGD**: A version of Stochastic Gradient Descent that clips gradients and adds noise during training.

## 2. Homomorphic Encryption (HE)

*   **Magic**: Performing math on *encrypted* data.
*   **Workflow**:
    1.  User encrypts data: $E(x)$.
    2.  Server runs model on encrypted data: $Model(E(x)) = E(y)$.
    3.  User decrypts result: $D(E(y)) = y$.
*   **Status**: Extremely slow (1000x-1,000,000x slower than plaintext), but improving.

## 3. Secure Multi-Party Computation (SMPC)

*   **Concept**: Splitting data into "shares" distributed across multiple servers. No single server sees the full data.
*   **Usage**: Two hospitals want to train a joint model on patient data without sharing the data with each other.

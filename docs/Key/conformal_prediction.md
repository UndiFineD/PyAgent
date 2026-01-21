# Conformal Prediction

Most AI models output a single prediction ("Cat") or a probability ("80% Cat"). But how much can we trust this?
**Conformal Prediction** is a statistical framework that converts any point prediction into a **Prediction Set** with a rigorous guarantee.

## 1. The Guarantee

"I am 95% confident that the true label is in this set: {Cat, Dog}."
- **Validity**: The probability that the true label is in the set is $\ge 1 - \alpha$ (e.g., 95%).
- This guarantee holds **regardless of the model** or the data distribution (as long as data is exchangeable). It is "distribution-free."

## 2. How it Works (Split Conformal)

1.  **Calibration Set**: Hold out a subset of data not used for training.
2.  **Non-Conformity Score**: Define a score $s(x, y)$ that measures how "weird" a pair is (e.g., 1 minus the softmax probability of the true class).
3.  **Quantile**: Compute the $1-\alpha$ quantile ($q$) of these scores on the calibration set.
4.  **Prediction**: For a new input, include all classes where the score is $\le q$.

## 3. Adaptive Sets

- If the image is clear, the set might be small: `{Cat}`.
- If the image is blurry, the set might be large: `{Cat, Dog, Fox}`.
- The size of the set reflects the **uncertainty**.

## Summary

Conformal Prediction is essential for **Safety-Critical AI** (Medical, Self-Driving), where "being wrong" is unacceptable, but "saying I don't know" (outputting a large set) is allowed.

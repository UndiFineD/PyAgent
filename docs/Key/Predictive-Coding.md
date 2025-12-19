# Predictive Coding

Predictive Coding is a theory from **Neuroscience** (Karl Friston) that suggests the brain is not a passive filter of information, but an active prediction machine.
It has inspired a class of neural network architectures that differ significantly from standard feedforward networks.

## 1. Top-Down vs. Bottom-Up

- **Standard CNN**: Information flows Bottom-Up (Pixels $\rightarrow$ Edges $\rightarrow$ Objects).
- **Predictive Coding**:
    - **Top-Down**: Higher layers generate a **Prediction** of what the lower layers should see.
    - **Bottom-Up**: Lower layers compare the prediction to the actual input and send the **Prediction Error** up.

## 2. Minimizing Surprise (Free Energy)

The goal of the brain (and the network) is to minimize the prediction error (Surprise).
- **Perception**: Updating the internal state (neurons) to better explain the input.
- **Action**: Moving the body to change the input to match the prediction.

## 3. PC Networks in AI

- **Local Learning**: In standard Backprop, the error signal must travel from the output all the way back. In PC, errors are computed locally at each layer. This is more biologically plausible.
- **Robustness**: PC networks are naturally robust to noise and adversarial attacks because the top-down priors "denoise" the input.

## Summary

Predictive Coding offers a unified theory of perception and action, moving away from "mapping inputs to outputs" towards "modeling the causes of inputs."

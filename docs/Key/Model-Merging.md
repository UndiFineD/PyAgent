# Model Merging

Model Merging is the technique of combining the weights of multiple fine-tuned models into a single model without any additional training. It has become a popular way to create "Frankenstein" models that outperform their individual parents.

## Why Merge?
*   **Combine Capabilities**: Merge a "Math" model with a "Coding" model to get a model good at both.
*   **Generalization**: Averaging weights often leads to a more robust model (similar to Ensembling, but with a single inference cost).
*   **No Training Cost**: It's purely arithmetic on the weight matrices.

## Techniques

### 1. Linear Averaging (Model Soups)
Simply taking the element-wise average of the weights.
$$ W_{new} = \frac{W_1 + W_2 + ... + W_n}{n} $$
*   **Requirement**: Models must share the same base architecture and initialization (e.g., all fine-tuned from Llama-2-7B).

### 2. SLERP (Spherical Linear Interpolation)
Linear averaging works poorly for high-dimensional vectors because it reduces the magnitude of the vector. SLERP interpolates along the surface of a hypersphere.
*   **Benefit**: Preserves the "direction" and magnitude of the weights better than linear averaging.
*   **Standard**: The go-to method for merging two models.

### 3. TIES (Task Arithmetic)
Resolves interference between models.
1.  **Trim**: Keep only the top-k% most changed parameters (sparse difference).
2.  **Elect**: Resolve sign conflicts (if one model increases a weight and another decreases it).
3.  **Merge**: Average the remaining weights.

### 4. DARE (Drop And REscale)
Randomly drops a percentage of the delta weights (changes from base model) and rescales the remaining ones.
*   **Benefit**: Allows merging many models (10+) without destroying the signal.

### 5. Passthrough (Frankenmerging)
Stitching layers from different models together.
*   **Example**: Taking the first 20 layers of Model A and the last 20 layers of Model B to create a 40-layer model.
*   **Risk**: Often results in a "brain damaged" model unless the layers are compatible.

## Tools
*   **MergeKit**: The standard open-source library for model merging.

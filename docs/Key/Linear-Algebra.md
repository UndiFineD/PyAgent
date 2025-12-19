# Linear Algebra for AI

## Overview
**Linear Algebra** is the branch of mathematics concerning linear equations and their representations in vector spaces. It is the "language" of Deep Learning because neural networks are essentially massive sequences of matrix multiplications.

## Key Structures

### 1. Scalars, Vectors, Matrices, Tensors
*   **Scalar ($x$)**: A single number (0-D tensor).
*   **Vector ($\mathbf{x}$)**: An array of numbers (1-D tensor). Represents a point in space or a direction.
*   **Matrix ($\mathbf{A}$)**: A 2-D grid of numbers. Represents a linear transformation (rotation, scaling, shear).
*   **Tensor**: An $n$-dimensional array (e.g., a batch of RGB images is a 4-D tensor: `[Batch, Height, Width, Channels]`).

## Core Operations

### 1. Dot Product (Inner Product)
The dot product of two vectors $\mathbf{a}$ and $\mathbf{b}$ is a scalar:
$$ \mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^n a_i b_i = ||\mathbf{a}|| ||\mathbf{b}|| \cos(\theta) $$
*   **Significance**: Measures similarity. If vectors point in the same direction, dot product is large. If orthogonal (90 degrees), it is zero. This is the basis of **Cosine Similarity** in embeddings.

### 2. Matrix Multiplication (MatMul)
Multiplying matrix $\mathbf{A}$ ($m \times n$) by matrix $\mathbf{B}$ ($n \times p$) results in $\mathbf{C}$ ($m \times p$).
*   **Significance**: The fundamental operation of a Dense (Linear) layer in a neural network: $\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$.

### 3. Transpose ($\mathbf{A}^T$)
Flipping a matrix over its diagonal.
*   **Significance**: Essential for aligning dimensions during backpropagation.

## Advanced Concepts

### 1. Eigenvalues and Eigenvectors
For a square matrix $\mathbf{A}$, an eigenvector $\mathbf{v}$ is a vector that does not change direction when $\mathbf{A}$ is applied, only length.
$$ \mathbf{A}\mathbf{v} = \lambda \mathbf{v} $$
*   **Significance**: Used in PCA (Principal Component Analysis) for dimensionality reduction and understanding the "dominant" features of a dataset.

### 2. Singular Value Decomposition (SVD)
Factorizing a matrix into three simpler matrices: $\mathbf{A} = \mathbf{U}\mathbf{\Sigma}\mathbf{V}^T$.
*   **Significance**: Used in LoRA (Low-Rank Adaptation) to approximate large weight updates with smaller matrices.

### 3. Norms ($L_1$, $L_2$)
*   **$L_1$ Norm (Manhattan)**: Sum of absolute values. Encourages sparsity (Lasso regularization).
*   **$L_2$ Norm (Euclidean)**: Square root of sum of squares. Used in weight decay (Ridge regularization) to prevent overfitting.

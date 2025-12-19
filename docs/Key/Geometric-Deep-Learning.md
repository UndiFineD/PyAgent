# Geometric Deep Learning

Geometric Deep Learning is the attempt to unify all deep learning architectures (CNNs, RNNs, GNNs, Transformers) under a single mathematical framework based on **Symmetry** and **Group Theory**. It is often called the "Erlangen Program" of Deep Learning.

## 1. The Core Idea: Structure and Symmetry

Standard Neural Networks (MLPs) ignore the structure of the input data. If you permute the pixels of an image, an MLP treats it as a new, unrelated input. A CNN, however, knows that shifting an image (translation) shouldn't change the object identity.

### Key Concepts
- **Domain ($\Omega$)**: The space where data lives (e.g., a 2D Grid for images, a Graph for molecules, a Sphere for planetary data).
- **Symmetry Group ($G$)**: The set of transformations that leave the object invariant (e.g., Translation, Rotation).
- **Invariance**: $f(g \cdot x) = f(x)$. The output doesn't change if you transform the input (e.g., classifying a cat regardless of where it is in the image).
- **Equivariance**: $f(g \cdot x) = g \cdot f(x)$. The output transforms in the same way as the input (e.g., segmentation masks shift if the image shifts).

## 2. The Blueprint

Geometric DL defines a neural network layer as:
$$ \text{Layer} = \text{Equivariant Linear Layer} \rightarrow \text{Non-linearity} \rightarrow \text{Pooling (Invariant)} $$

### Unifying Architectures

| Architecture | Domain | Symmetry Group | Operation |
| :--- | :--- | :--- | :--- |
| **CNN** | 2D Grid | Translation | Convolution |
| **Spherical CNN** | Sphere | 3D Rotation ($SO(3)$) | Spherical Convolution |
| **GNN** | Graph | Permutation | Message Passing |
| **Transformer** | Set (Sequence) | Permutation | Attention |
| **RNN** | 1D Grid (Time) | Time Translation | Recurrence |

## 3. Why it Matters

- **Data Efficiency**: By baking the symmetries of the physical world into the model architecture (inductive bias), we drastically reduce the amount of data needed to train. We don't need to show the model a cat in every possible position; the architecture already understands translation.
- **3D & Science**: Essential for AlphaFold (protein folding), drug discovery, and physics simulations where rotation and translation invariance are physical laws, not just preferences.

## Summary

Geometric Deep Learning provides the "Why" behind the "How." It explains why CNNs work on images and GNNs work on graphs: they respect the underlying symmetry of the data domain.

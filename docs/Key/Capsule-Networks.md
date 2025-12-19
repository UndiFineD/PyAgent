# Capsule Networks (CapsNets)

Proposed by Geoffrey Hinton, Capsule Networks aim to fix the deficiencies of Convolutional Neural Networks (CNNs), specifically their inability to handle spatial hierarchies and viewpoints correctly (the "Picasso problem").

## 1. The Problem with CNNs

- **Pooling**: Max-pooling throws away spatial information. It detects *if* a feature exists, but loses *where* it is relative to others.
- **Scalar Output**: Neurons output a single scalar activation. They don't carry orientation, scale, or other instantiation parameters.

## 2. Capsules & Vectors

A **Capsule** is a group of neurons whose activity vector represents the **instantiation parameters** of a specific type of entity (e.g., an object or an object part).
- **Length of Vector**: Represents the probability that the entity exists.
- **Orientation of Vector**: Represents the properties (pose, deformation, velocity, albedo, etc.).

## 3. Dynamic Routing by Agreement

Instead of Max-Pooling (which routes information to the most active neuron), CapsNets use **Dynamic Routing**:
1. **Prediction**: Lower-level capsules (e.g., "eye", "nose") predict the pose of higher-level capsules (e.g., "face").
2. **Agreement**: If the predictions from the "eye" and "nose" agree on the position of the "face", the coupling coefficient increases.
3. **Routing**: The output is sent *only* to the higher-level capsule that agrees with the prediction.

$$ c_{ij} = \frac{\exp(b_{ij})}{\sum_k \exp(b_{ik})} $$
(Coupling coefficients are determined by a "routing softmax").

## 4. Equivariance vs. Invariance

- **CNNs aim for Invariance**: If the cat moves, the output "cat" stays the same (but we lose the position).
- **CapsNets aim for Equivariance**: If the cat moves, the output vector *changes* to reflect the new position, but the length (probability) remains the same.

## Summary

While CapsNets have not yet replaced CNNs due to high computational cost (iterative routing), they represent a fundamental rethink of how neural networks should model spatial relationships and object hierarchies.

# Optimal Transport (OT)

Optimal Transport is a mathematical framework for comparing and moving probability distributions. It asks: "What is the minimum cost to transform one pile of dirt (distribution $P$) into another pile of dirt (distribution $Q$)?"

## 1. Wasserstein Distance (Earth Mover's Distance)

Standard metrics like KL Divergence fail when distributions don't overlap (gradient is zero).
Wasserstein Distance measures the "work" needed to move the mass.
- Even if two distributions are far apart, Wasserstein provides a meaningful gradient pointing towards the target.
- This is the key to **Wasserstein GANs (WGAN)**, which are much more stable than standard GANs.

## 2. The Sinkhorn Algorithm

Computing exact OT is computationally expensive ($O(N^3)$).
The **Sinkhorn Algorithm** adds an entropy regularization term, turning the problem into a series of simple matrix multiplications that can be computed on a GPU in $O(N^2)$.

## 3. Flow Matching & Diffusion

Modern generative models (like Stable Diffusion 3) use **Flow Matching**, which is based on OT.
- Instead of diffusing data to noise randomly, we construct a "Straight Path" (Geodesic) between the data distribution and the noise distribution.
- This results in faster sampling (fewer steps) and better quality.

## Summary

Optimal Transport provides the geometric foundation for modern Generative AI, replacing heuristic loss functions with rigorous metrics based on mass transportation.

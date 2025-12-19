# Deep Equilibrium Models (DEQs)

Standard Deep Learning assumes a fixed number of layers ($L=50$, $L=100$).
**Deep Equilibrium Models** assume that the network is an infinite-depth weight-tied layer that we run until it converges to a "fixed point".

## 1. The Fixed Point

Instead of $z_{k+1} = f(z_k, x)$, we look for a state $z^*$ such that:
$$ z^* = f(z^*, x) $$
This is the equilibrium state. The output of the network is this $z^*$.

## 2. Finding the Solution

We can find $z^*$ using:
- **Forward Iteration**: Just keep applying $f$ until $z$ stops changing.
- **Root Finding**: Rewrite as $g(z) = z - f(z, x) = 0$ and use Newton's Method or Broyden's Method to find the root. This is much faster than simple iteration.

## 3. Implicit Differentiation

How do we backpropagate through an "infinite" number of layers?
We use the **Implicit Function Theorem**.
- We don't need to store the intermediate steps of the solver.
- We can compute the gradient $\frac{\partial z^*}{\partial \theta}$ directly from the equilibrium condition, regardless of how we got there.
- **Memory Cost**: $O(1)$ (Constant memory), similar to Neural ODEs.

## Summary

DEQs allow us to decouple the "model definition" (the layer $f$) from the "compute budget" (how long we run the solver), offering a path to extremely deep, memory-efficient networks.

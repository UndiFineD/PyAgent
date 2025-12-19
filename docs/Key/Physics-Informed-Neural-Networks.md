# Physics-Informed Neural Networks (PINNs)

Traditional scientific computing solves Partial Differential Equations (PDEs) using numerical methods like Finite Element Method (FEM) or Finite Difference Method (FDM). These require meshing the domain and are computationally expensive.
**PINNs** solve PDEs by embedding the physical laws directly into the neural network's loss function.

## 1. The Core Idea

We want to find a function $u(x, t)$ that satisfies a PDE (e.g., the Heat Equation):
$$ \frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2} = 0 $$

We approximate $u(x, t)$ with a neural network $N(x, t; \theta)$.
The loss function has two parts:
1.  **Data Loss**: $MSE_{data} = ||N(x_{data}, t_{data}) - u_{measured}||^2$. (Fits observed data points).
2.  **Physics Loss**: $MSE_{physics} = ||\frac{\partial N}{\partial t} - \alpha \frac{\partial^2 N}{\partial x^2}||^2$. (Enforces the PDE).

## 2. Automatic Differentiation

Crucially, we compute the derivatives ($\frac{\partial N}{\partial t}$, $\frac{\partial^2 N}{\partial x^2}$) using **Automatic Differentiation** (Autograd), which is exact (up to floating point error), unlike numerical differences.

## 3. Benefits

- **Mesh-Free**: No need to generate complex meshes. You just sample random points in the domain.
- **Inverse Problems**: PINNs excel at discovering unknown parameters. If $\alpha$ (thermal diffusivity) is unknown, the network can learn it along with the solution $u$.
- **Data-Efficient**: The physics constraint acts as a powerful regularizer, allowing learning from very sparse data.

## Summary

PINNs are revolutionizing "AI for Science" by combining the flexibility of Deep Learning with the rigorous constraints of Physics.

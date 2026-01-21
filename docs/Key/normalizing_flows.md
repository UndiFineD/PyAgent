# Normalizing Flows

Generative models like GANs and VAEs approximate the data distribution $p(x)$.
- **GANs**: Implicitly model $p(x)$ (can sample, but can't evaluate likelihood).
- **VAEs**: Approximate $p(x)$ using a lower bound (ELBO).
**Normalizing Flows** allow for **exact likelihood estimation** and exact sampling.

## 1. Change of Variables Formula

If we have a simple distribution $z \sim \mathcal{N}(0, I)$ and an invertible function $f$, we can transform $z$ into a complex data point $x = f(z)$.
The probability density of $x$ is given by:
$$ p_x(x) = p_z(z) |\det \frac{\partial f^{-1}}{\partial x}| $$
We need to design neural networks that are **invertible** and have an **easy-to-compute Jacobian determinant**.

## 2. Coupling Layers (RealNVP, Glow)

To ensure invertibility and efficient determinants, we split the input $x$ into two halves $(x_1, x_2)$.
- $y_1 = x_1$ (Identity)
- $y_2 = x_2 \odot \exp(s(x_1)) + t(x_1)$
Here, $s$ (scale) and $t$ (translation) can be arbitrarily complex neural networks because they don't need to be inverted—only the affine transformation needs to be inverted.

## 3. Applications

- **Density Estimation**: Detecting anomalies (out-of-distribution data) by checking if $p(x)$ is low.
- **Image Generation**: Glow (Kingma & Dhariwal, 2018) generated high-quality faces before Diffusion took over.
- **Variational Inference**: Improving the posterior approximation in VAEs.

## Summary

Normalizing Flows provide a mathematically elegant way to model complex distributions, trading off some expressivity (constraints on architecture) for exactness.

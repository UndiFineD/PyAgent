# Flow Matching

Flow Matching is a generative modeling framework that generalizes and improves upon Diffusion Models. It is the mathematical foundation behind **Stable Diffusion 3** and modern audio generation models.

## 1. The Problem with Diffusion

Standard Diffusion Models (DDPM) rely on a stochastic differential equation (SDE) that slowly destroys data with noise and then learns to reverse it.
- **Curved Paths**: The trajectory from "Noise" to "Image" is often curved and complex.
- **Slow Sampling**: Because the path is curved, the solver needs many small steps (50-100) to trace it accurately.

## 2. The Solution: Straight Paths

Flow Matching uses **Optimal Transport** theory to define the *straightest possible path* between the noise distribution and the data distribution.

### Conditional Flow Matching (CFM)
Instead of learning to "denoise," the model learns a **Vector Field** $v_t(x)$.
- Imagine the noise distribution as a cloud of particles at time $t=0$.
- Imagine the data distribution (images) as a target shape at time $t=1$.
- The model learns the velocity vectors that push the particles from $t=0$ to $t=1$ in straight lines.

## 3. Rectified Flow

A specific instance of Flow Matching.
- **Reflow**: You can take a trained model, generate data, and then *retrain* the model on the pairs (Noise, Generated Data).
- **Result**: This "straightens" the flow even further. After a few rounds of Reflow, the trajectory is almost perfectly linear.
- **One-Step Generation**: If the path is a straight line, you can theoretically jump from Noise to Image in a single step (Euler integration).

## 4. Advantages

- **Efficiency**: Requires fewer inference steps (sampling) to get high-quality results.
- **Simplicity**: The training objective is a simple regression (matching the vector field), often more stable than the complex noise schedules of diffusion.

## Summary

Flow Matching is the "Calculus" upgrade to the "Algebra" of Diffusion. By using better math (Optimal Transport), it finds more efficient routes to generate data.

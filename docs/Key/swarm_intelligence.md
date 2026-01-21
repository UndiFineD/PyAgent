# Swarm Intelligence

Decentralized, self-organized systems inspired by the collective behavior of social animals (ants, birds, bees).

## 1. Particle Swarm Optimization (PSO)

*   **Inspiration**: A flock of birds searching for food.
*   **Mechanism**:
    *   A population of "particles" flies through the search space.
    *   Each particle knows its own best position ($p_{best}$) and the swarm's global best position ($g_{best}$).
    *   Velocity is updated to pull the particle toward both $p_{best}$ and $g_{best}$.
*   **Use Case**: Optimizing complex, non-differentiable functions (where Gradient Descent fails).

## 2. Ant Colony Optimization (ACO)

*   **Inspiration**: Ants finding the shortest path to food using pheromones.
*   **Mechanism**:
    *   Virtual ants explore paths.
    *   Shorter paths get traversed faster, accumulating more pheromones.
    *   Future ants prefer paths with strong pheromones.
*   **Use Case**: Routing problems (Traveling Salesman Problem), Network routing.

## 3. Boids (Bird-oid objects)

*   **Simulation**: Simulating flocking behavior using three simple rules:
    1.  **Separation**: Steer to avoid crowding local flockmates.
    2.  **Alignment**: Steer towards the average heading of local flockmates.
    3.  **Cohesion**: Steer to move towards the average position (center of mass) of local flockmates.

# Evolutionary Algorithms (EA)

Optimization algorithms inspired by biological evolution. Unlike Gradient Descent, they do not require the function to be differentiable.

## 1. The Loop

1.  **Population**: Start with a random set of candidate solutions (individuals).
2.  **Evaluation**: Measure the "Fitness" of each individual.
3.  **Selection**: Pick the best ones to be parents.
4.  **Crossover**: Combine parents to create children (mixing genes).
5.  **Mutation**: Randomly tweak genes to maintain diversity.
6.  **Repeat**.

## 2. Neuroevolution

Evolving Neural Networks instead of training them with Backpropagation.
*   **NEAT (NeuroEvolution of Augmenting Topologies)**: Evolves both the *weights* and the *structure* (adding neurons/connections) of the network.
*   **Advantages**: Can solve problems with sparse rewards or deceptive traps where Gradient Descent gets stuck in local minima.

## 3. Quality-Diversity (QD)

Algorithms like **MAP-Elites**.
*   Goal: Find a set of solutions that are both *high-performing* and *diverse*.
*   Example: A robot learning to walk.
    *   Gradient Descent finds one fast gait.
    *   QD finds a fast gait, a limping gait (useful if damaged), and a hopping gait.

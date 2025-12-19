# Game Theory Fundamentals for AI

**Game Theory** is the mathematical study of strategic interaction among rational decision-makers. In Artificial Intelligence, it provides the theoretical framework for Multi-Agent Systems (MARL) and adversarial training methods like GANs.

## Core Concepts

### 1. The Game
A game consists of:
*   **Players**: The agents making decisions.
*   **Strategies**: The set of possible actions each player can take.
*   **Payoffs**: The reward (or utility) each player receives based on the combination of strategies chosen by all players.

### 2. Types of Games
*   **Zero-Sum Game**: One player's gain is exactly the other player's loss (e.g., Chess, Go). The sum of utilities is zero.
*   **Non-Zero-Sum Game**: Win-win or lose-lose scenarios are possible (e.g., Prisoner's Dilemma).
*   **Cooperative vs. Non-Cooperative**: Whether players can form binding agreements.
*   **Perfect vs. Imperfect Information**: Do players know the full state of the game? (Chess = Perfect, Poker = Imperfect).

## Key Equilibrium Concepts

### 1. Nash Equilibrium
A state where no player can improve their payoff by unilaterally changing their strategy, assuming the other players keep theirs unchanged.
*   **Relevance**: In **GANs** (Generative Adversarial Networks), training is a game between the Generator and Discriminator. The goal is to reach a Nash Equilibrium where the Generator produces perfect data and the Discriminator guesses with 50% probability.

### 2. Minimax Theorem
In zero-sum games, the optimal strategy is to minimize the maximum possible loss (or maximize the minimum gain).
*   **Relevance**: This is the foundation of game-playing AI (like Deep Blue or AlphaGo's MCTS value estimation).

## Applications in AI

### 1. Generative Adversarial Networks (GANs)
*   **Players**: Generator ($G$) and Discriminator ($D$).
*   **Objective**: $G$ tries to fool $D$; $D$ tries to catch $G$.
*   **Challenge**: Training is unstable because finding a Nash Equilibrium in high-dimensional non-convex spaces is difficult (mode collapse).

### 2. Multi-Agent Reinforcement Learning (MARL)
*   **Scenario**: Multiple robots in a warehouse or autonomous cars at an intersection.
*   **Challenge**: The environment is **non-stationary** from the perspective of one agent because other agents are learning and changing their policies simultaneously.
*   **Solution**: Game-theoretic approaches (like fictitious play or counterfactual regret minimization) help agents converge to stable policies.

### 3. Mechanism Design (Reverse Game Theory)
Designing the rules of the game (e.g., an auction or ad bidding system) so that rational agents behave in a desired way (e.g., bidding truthfully).

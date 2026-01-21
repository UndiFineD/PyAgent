# AlphaGo & AlphaZero

## Overview
**AlphaGo** (2016) by DeepMind was the first AI program to defeat a human world champion (Lee Sedol) at the ancient game of Go, a feat previously thought to be a decade away due to the game's immense search space ($10^{170}$ positions).

## Key Innovations

### 1. Monte Carlo Tree Search (MCTS)
Instead of searching every possible move (Minimax), MCTS simulates thousands of random games from the current position to estimate the win probability.
*   **Selection**: Pick a promising path.
*   **Expansion**: Add a new node.
*   **Simulation**: Play randomly to the end.
*   **Backpropagation**: Update the win stats up the tree.

### 2. Deep Neural Networks
AlphaGo used two networks to guide the MCTS:
*   **Policy Network**: Predicts the next move (reducing the *breadth* of the search). "What would a pro play?"
*   **Value Network**: Predicts the winner from the current board state (reducing the *depth* of the search). "Who is winning?"

## Evolution

### 1. AlphaGo Lee (2016)
*   Trained on thousands of human amateur and professional games (Supervised Learning).
*   Then refined via Self-Play Reinforcement Learning.

### 2. AlphaGo Zero (2017)
*   **Tabula Rasa**: Started with **zero** human knowledge. No human games.
*   **Self-Play**: Played against itself millions of times.
*   **Result**: Surpassed AlphaGo Lee in 3 days. Proved that human data might actually bias the AI and limit its potential.

### 3. AlphaZero (2017)
*   **Generalization**: The same algorithm applied to Chess and Shogi.
*   **Result**: Defeated Stockfish (the best traditional Chess engine) after just 4 hours of training.
*   **Style**: Developed aggressive, alien strategies (sacrificing pieces for long-term positional advantage) that changed how humans play chess.

### 4. MuZero (2020)
*   **Model-Based RL**: Learned the rules of the game itself (the dynamics model) while playing. Can master Atari games without being told the rules or seeing the internal state.

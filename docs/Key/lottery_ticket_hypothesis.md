# Lottery Ticket Hypothesis

## Overview
The **Lottery Ticket Hypothesis**, proposed by Frankle and Carbin (2018), states that:

> "A randomly-initialized, dense neural network contains a subnetwork that is initialized such that—when trained in isolation—it can match the test accuracy of the original network after training for at most the same number of iterations."

## The "Winning Ticket"
*   **Dense Network**: The massive network we usually train.
*   **Winning Ticket**: A sparse subnetwork (e.g., 10-20% of the original weights) found inside the dense network.
*   **Key Insight**: The vast majority of weights in a neural network are unnecessary. The network is only successful because it is so large that it is statistically likely to contain this "lucky" initialization (the winning ticket).

## Finding the Ticket (Iterative Magnitude Pruning)
1.  Randomly initialize a dense network.
2.  Train it for $j$ iterations.
3.  Prune the $p\%$ of weights with the smallest magnitudes.
4.  **Reset** the remaining weights to their *original initial values* (from step 1).
5.  Retrain this sparse network. It will often reach the same accuracy as the dense one.

## Implications
*   **Efficiency**: If we could identify these tickets *before* training, we could train much smaller networks from the start (saving massive compute).
*   **Pruning**: Explains why we can prune trained models by 90% without losing accuracy.

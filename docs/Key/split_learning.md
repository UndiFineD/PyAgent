# Split Learning

Split Learning is a privacy-preserving machine learning technique that differs from Federated Learning. Instead of replicating the entire model on every client device, it **splits** the neural network layer-wise between the client and the server.

## 1. The Architecture

Imagine a deep neural network with 100 layers.
- **Client (Edge Device)**: Holds the first few layers (e.g., Layers 1-5).
- **Server (Cloud)**: Holds the remaining layers (e.g., Layers 6-100).
- **Cut Layer**: The point where the network is split.

## 2. The Training Process (Smash Data)

1.  **Forward Pass (Client)**: The client processes its private raw data (e.g., medical images) through the first 5 layers.
2.  **Transmission**: The output of the 5th layer (activations), often called "Smash Data," is sent to the server. **Raw data never leaves the client.**
3.  **Forward Pass (Server)**: The server takes the Smash Data and processes it through the rest of the network to generate a prediction.
4.  **Backward Pass (Server)**: The server calculates the loss and backpropagates gradients down to the Cut Layer.
5.  **Transmission**: The gradients at the Cut Layer are sent back to the client.
6.  **Backward Pass (Client)**: The client uses these gradients to update the weights of the first 5 layers.

## 3. Comparison with Federated Learning (FL)

| Feature | Federated Learning | Split Learning |
| :--- | :--- | :--- |
| **Model Location** | Full model on every client | Partial model on client, partial on server |
| **Data Privacy** | Gradients shared | Activations ("Smash Data") shared |
| **Client Compute** | High (Trains full model) | Low (Trains only first few layers) |
| **Communication** | Heavy (Sending full model weights) | Light (Sending activations per batch) |
| **Parallelism** | Clients train in parallel | Clients often train sequentially (Round Robin) |

## 4. Security Risks

While raw data isn't shared, the "Smash Data" (activations) can sometimes be reverse-engineered to reconstruct the input (Model Inversion Attack).
- **Mitigation**: Add noise (Differential Privacy) or use more complex transformations at the Cut Layer to obfuscate the data.

## Summary

Split Learning is ideal for **resource-constrained edge devices** (like IoT sensors) that cannot hold a full LLM or ResNet but still need to participate in private collaborative training.

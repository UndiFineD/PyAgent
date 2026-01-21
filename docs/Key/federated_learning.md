# Federated Learning

Standard AI training requires collecting all user data into a central server. This creates massive privacy risks and bandwidth costs. **Federated Learning (FL)** flips this model: instead of bringing the data to the code, we bring the code to the data.

## 1. The Core Loop (FedAvg)

1.  **Global Model**: A central server holds the "Global Model."
2.  **Broadcast**: The server sends the current model weights to thousands of client devices (e.g., smartphones).
3.  **Local Training**: Each device trains the model on its own *local, private data* for a few epochs.
4.  **Upload**: The devices send *only the weight updates* (gradients) back to the server. The raw data never leaves the device.
5.  **Aggregation**: The server averages the updates from all devices to create the new Global Model.

## 2. Privacy & Security

*   **Data Minimization**: The server never sees the user's photos or messages.
*   **Differential Privacy**: Even weight updates can leak information (e.g., if a gradient is huge for the word "cancer," the user might have typed "cancer"). Noise is added to the updates to mathematically guarantee privacy.
*   **Secure Aggregation**: Cryptographic protocols ensure the server can sum the updates without seeing the individual updates.

## 3. Challenges

*   **Non-IID Data**: Data is not Independent and Identically Distributed. One user might only type in English, another in Spanish. One takes photos of cats, another of cars. This heterogeneity makes training unstable.
*   **Communication Cost**: Sending model weights (GBs) to millions of phones is expensive.
*   **Stragglers**: Some devices are slow or run out of battery, delaying the aggregation step.

## 4. Use Cases

*   **Gboard (Google Keyboard)**: Predicting the next word without sending keystrokes to the cloud.
*   **Healthcare**: Hospitals collaborate to train a cancer detection model without sharing patient records (which would violate HIPAA).

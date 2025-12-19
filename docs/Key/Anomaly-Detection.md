# Anomaly Detection

Identifying rare items, events, or observations which raise suspicions by differing significantly from the majority of the data.

## 1. Use Cases

*   **Fraud Detection**: Credit card transactions that don't fit the user's pattern.
*   **Manufacturing**: Detecting defects in products on an assembly line.
*   **IT Operations (AIOps)**: Detecting server failures or cyberattacks before they happen.

## 2. Techniques

*   **Statistical**: "Is this value more than 3 standard deviations from the mean?" (Z-Score).
*   **Isolation Forests**: Randomly split the data. Anomalies are "easier" to isolate (require fewer splits) than normal points.
*   **One-Class SVM**: Learns a boundary around the "normal" data. Anything outside is an anomaly.

## 3. Deep Learning (Autoencoders)

*   **Concept**: Train a neural network to compress the input (Encoder) and then reconstruct it (Decoder).
*   **Training**: Train *only* on normal data.
*   **Inference**:
    *   Pass a new data point through the Autoencoder.
    *   Measure the **Reconstruction Error** (Input vs. Output).
    *   **Normal data**: Low error (the model learned how to compress it).
    *   **Anomaly**: High error (the model has never seen this pattern and fails to reconstruct it).

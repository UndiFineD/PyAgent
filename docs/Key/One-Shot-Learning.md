# One-Shot Learning (Few-Shot Learning)

Deep Learning typically requires thousands of examples per class. Humans can learn a new object (e.g., a "Segway") from seeing it just once.
**One-Shot Learning** aims to replicate this ability.

## 1. Siamese Networks

Instead of learning to **classify** (Image $\rightarrow$ Label), we learn to **compare** (Image A, Image B $\rightarrow$ Same/Different).
- **Architecture**: Two identical networks (sharing weights) process two images.
- **Distance**: We calculate the distance between their output vectors $d(f(A), f(B))$.
- **Loss**: Contrastive Loss or Triplet Loss minimizes distance for same class, maximizes for different.
- **Inference**: To classify a new image, compare it to the single example you have of each class. The closest match wins.

## 2. Prototypical Networks

An extension to Few-Shot Learning (e.g., 5 examples per class).
1.  **Embed**: Map the 5 examples of Class A to a vector space.
2.  **Prototype**: Calculate the mean (centroid) of these vectors. This is the "Prototype" for Class A.
3.  **Classify**: To classify a query image, find the nearest Prototype.

## 3. Relation Networks

Instead of using a fixed distance metric (like Euclidean distance), we train a neural network to learn the metric.
- The "Relation Module" takes the concatenation of the query embedding and the support embedding and outputs a similarity score $[0, 1]$.

## Summary

One-Shot Learning is critical for applications like **Face Recognition** (unlocking your phone), where you can't retrain the model every time a new user is added.

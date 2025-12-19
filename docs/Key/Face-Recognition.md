# Face Recognition

## Overview
**Face Recognition** is the task of identifying or verifying a person from a digital image or video frame. It is distinct from Face Detection (finding a face) and Face Analysis (age/gender/emotion).

## The Challenge: One-Shot Learning
In most classification tasks, we have thousands of examples per class. In Face Recognition, we often have only one reference photo (e.g., an ID card) and need to recognize the person in a new photo. This requires learning a **similarity metric** rather than a fixed classifier.

## Siamese Networks
*   **Architecture**: Two identical neural networks (sharing weights) process two images.
*   **Output**: Two embedding vectors.
*   **Goal**: Minimize the distance between vectors of the same person and maximize the distance between vectors of different people.

## Triplet Loss
Introduced by Google (FaceNet, 2015).
*   **Input**: Three images: Anchor (A), Positive (P), Negative (N).
*   **Objective**: Ensure that $Distance(A, P) + Margin < Distance(A, N)$.
*   **Result**: The network learns an embedding space where faces of the same person cluster tightly together.

## ArcFace (Additive Angular Margin Loss)
*   **Concept**: Instead of manipulating distances in Euclidean space (like Triplet Loss), ArcFace operates in **angular space** (on a hypersphere).
*   **Mechanism**: It adds an angular margin penalty to the target logit during training.
*   **Benefit**: Produces highly discriminative features that are more robust to variations in pose and lighting. Currently the state-of-the-art for face recognition.

## Privacy & Ethics
Face recognition is controversial due to privacy concerns and potential bias (e.g., lower accuracy for certain demographics). Many jurisdictions regulate its use.

# Recommender Systems

The algorithms that power Netflix, TikTok, and Amazon. They filter information to show users what they are most likely to engage with.

## 1. Traditional Approaches

*   **Content-Based Filtering**: "You liked Star Wars, so here is Star Trek." (Recommends similar items).
*   **Collaborative Filtering**: "Users who liked Star Wars also liked Harry Potter." (Recommends items liked by similar users).
    *   **Matrix Factorization**: Decomposing the User-Item interaction matrix into lower-dimensional vectors (Embeddings).

## 2. Deep Learning Approaches

*   **Two-Tower Models**:
    *   **User Tower**: A neural network processes user history/demographics into a vector $U$.
    *   **Item Tower**: A neural network processes item details into a vector $I$.
    *   **Score**: Dot product $U \cdot I$ represents the match probability.
*   **DLRM (Deep Learning Recommendation Model)**: Meta's open-source architecture combining categorical embeddings with MLPs.

## 3. Challenges

*   **Cold Start**: How to recommend things to a new user with no history?
*   **Exploration vs. Exploitation**: Should we show what we *know* they like (Exploit) or try something new to learn more (Explore)?
*   **Bias**: Recommender systems can create "filter bubbles" or echo chambers.

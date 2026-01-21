# Causal AI

Standard Machine Learning is based on **Correlation**: "People who buy diapers also buy beer."
**Causal AI** asks **Why?**: "Does buying diapers *cause* you to buy beer, or is there a confounding variable (e.g., being a young parent)?"

## 1. The Ladder of Causation (Judea Pearl)

1.  **Association (Seeing)**: $P(y|x)$. "What is the probability of rain if I see wet grass?" (Standard ML).
2.  **Intervention (Doing)**: $P(y|do(x))$. "What if I turn on the sprinkler? Will the grass be wet?" (RL / A/B Testing).
3.  **Counterfactuals (Imagining)**: "The grass is wet. Would it have been wet if I *hadn't* turned on the sprinkler?" (Causal Inference).

## 2. Structural Causal Models (SCM)

Representing the world as a graph (DAG - Directed Acyclic Graph).
*   Nodes are variables.
*   Edges represent causal influence ($A \rightarrow B$).
*   **Confounder**: A variable that influences both the treatment and the outcome (e.g., "Age" influences both "Exercise" and "Health"). If you don't control for it, you get Spurious Correlations.

## 3. Why do we need it?

*   **Robustness**: Correlations change (e.g., Google Flu Trends failed because search patterns changed). Causal mechanisms are invariant (Viruses cause flu, regardless of search trends).
*   **Fairness**: Determining if a model is biased. "Did the model deny the loan *because* of race?" (Counterfactual fairness).
*   **Decision Making**: To make policy decisions ("Should we raise interest rates?"), you need to know the causal effect, not just the correlation.

## 4. Causal Discovery

Algorithms that try to infer the causal graph from data alone.
*   **Constraint-based**: Look for conditional independencies in the data.
*   **Score-based**: Search for the graph structure that best fits the data.
*   *Note*: This is extremely hard and often impossible without domain knowledge.

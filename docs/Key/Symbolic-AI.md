# Symbolic AI (GOFAI)

"Good Old-Fashioned AI". The dominant paradigm before Deep Learning took over. It relies on explicit rules, logic, and symbols rather than statistical patterns.

## 1. Logic Programming (Prolog)

*   **Facts**: `parent(john, mary).` `parent(mary, ann).`
*   **Rules**: `grandparent(X, Y) :- parent(X, Z), parent(Z, Y).`
*   **Query**: `?- grandparent(john, ann).` -> **True**.
*   **Pros**: Perfectly explainable, verifiable, and requires zero training data.
*   **Cons**: Brittle. Fails in the messy real world (e.g., defining a "chair" with rules is impossible).

## 2. Neuro-Symbolic AI

The best of both worlds. Combining the learning capability of Neural Networks with the reasoning capability of Symbolic AI.
*   **Concept**: Use a Neural Network to perceive the world (Image -> Symbols) and a Symbolic Engine to reason about it (Symbols -> Answer).
*   **Example**: **AlphaGeometry**.
    *   Uses a Language Model to suggest new geometric constructions.
    *   Uses a Symbolic Engine to rigorously prove the theorem.
    *   Solved International Mathematical Olympiad problems at a Gold Medal level.

## 3. Knowledge Representation

*   **Ontologies**: Formal definitions of concepts and relationships (e.g., SNOMED CT for medical terms).
*   **Semantic Web**: Making the internet understandable by machines using RDF/OWL.

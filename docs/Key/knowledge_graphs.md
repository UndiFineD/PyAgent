# Knowledge Graphs (KGs)

A structured way to represent information as a graph of **Entities** (nodes) and **Relations** (edges).

## 1. Structure

*   **Triples**: The fundamental unit of data. `(Subject, Predicate, Object)`.
    *   Example: `(Elon Musk, CEO_OF, Tesla)`.
*   **Ontology**: The schema or "rules" of the graph. Defines what types of entities exist (Person, Company) and valid relationships.

## 2. Technologies

*   **RDF (Resource Description Framework)**: The standard data model for KGs.
*   **SPARQL**: The SQL-like query language for retrieving data from an RDF graph.
*   **Neo4j**: The most popular Graph Database (uses Property Graph model, slightly different from RDF).

## 3. GraphRAG (KG + LLM)

Standard RAG retrieves unstructured text chunks. GraphRAG retrieves structured facts.
*   **Multi-Hop Reasoning**: "Who is the CEO of the company that acquired DeepMind?"
    *   **Vector Search**: Might fail if the answer requires connecting two separate documents.
    *   **Graph Search**: Traverse edges: `DeepMind --acquired_by--> Google --CEO--> Sundar Pichai`.
*   **Hallucination Reduction**: KGs provide a "source of truth" that constrains the LLM's generation.

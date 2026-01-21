# Text-to-SQL

## Overview
**Text-to-SQL** is the task of converting natural language questions ("How many users signed up last week?") into executable SQL queries (`SELECT count(*) FROM users WHERE signup_date > ...`). This democratizes data access, allowing non-technical users to query databases.

## How It Works
1.  **Schema Linking**: The LLM is provided with the database schema (table names, column names, types, and foreign keys).
2.  **Query Generation**: The LLM translates the intent into SQL syntax (ANSI SQL, PostgreSQL, MySQL, etc.).
3.  **Execution**: The generated SQL is run against the database.
4.  **Response Generation**: The results are formatted back into natural language or a chart.

## Challenges
*   **Ambiguity**: "Show me the top products" - Top by revenue? By units sold? By rating?
*   **Schema Complexity**: Databases with hundreds of tables and obscure column names (`col_x_123`).
*   **Hallucination**: Generating SQL that references non-existent columns or tables.

## Techniques
*   **RAG for Schema**: Retrieving only the relevant tables for the query (instead of passing the entire schema).
*   **Few-Shot Prompting**: Providing examples of "Question -> SQL" pairs in the prompt.
*   **Chain-of-Thought**: Asking the model to explain its logic before writing the SQL.
*   **Self-Correction**: If the SQL fails to execute, feeding the error message back to the LLM to fix it.

## Benchmarks
*   **Spider**: The standard benchmark for cross-domain Text-to-SQL.
*   **BIRD**: A more challenging benchmark focusing on real-world database complexity.

## Tools
*   **Vanna.ai**: Open-source RAG framework for SQL generation.
*   **LlamaIndex**: Text-to-SQL query engines.
*   **LangChain**: SQLDatabaseChain.

## Security
*   **Read-Only Access**: Always run generated queries with a read-only database user to prevent `DROP TABLE`.
*   **Human-in-the-Loop**: Showing the SQL to the user for verification before execution.

# Guided Generation (Constrained Decoding)

LLMs are probabilistic, which makes them bad at following strict formats. Guided Generation forces the model's output to adhere to a specific schema (JSON, SQL, Regex) by manipulating the logits during inference.

## How it Works
At each step of generation, the inference engine checks which tokens are valid according to the constraint.
1.  **Constraint**: Output must be a valid JSON object.
2.  **Current State**: `{"name": "John", "age":`
3.  **Valid Next Tokens**: Numbers (`2`, `3`, `4`...).
4.  **Invalid Next Tokens**: Letters (`a`, `b`), Symbols (`}`).
5.  **Action**: Set the probability of all invalid tokens to 0 (-infinity logits).

## Techniques

### 1. JSON Mode
Most API providers (OpenAI, Anthropic) now offer a "JSON Mode".
*   **Mechanism**: Ensures the output is valid JSON.
*   **Limitation**: Doesn't guarantee the *schema* (keys and value types), just the syntax.

### 2. Context Free Grammars (CFG)
Defining a formal grammar (like EBNF) for the output.
*   **Tools**: `llama-cpp-python` (Grammars), `Outlines` (library).
*   **Power**: Can enforce complex structures. "Generate a Python function that returns a list of integers."

### 3. Regex Constraints
Forcing the output to match a Regular Expression.
*   **Example**: `\d{3}-\d{2}-\d{4}` (SSN format).
*   **Use Case**: Extracting specific entities or formatting dates.

### 4. Type Constraints (Function Calling)
When using "Tools" or "Function Calling", the model is constrained to generate arguments that match the function's signature (Pydantic model).

## Benefits
*   **Reliability**: 100% syntax guarantee. No more "I apologize, here is the corrected JSON" loops.
*   **Efficiency**: The model doesn't waste tokens generating invalid characters.
*   **Integration**: Makes LLMs safe to use as backend components in software systems.

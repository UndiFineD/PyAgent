# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_node_functions_d9bf156ee732.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_node_functions.py

# Extracted from: C:\DEV\PyAgent\.external\agentkit_prompting\src\agentkit\node_functions.py

# NOTE: extracted with static-only rules; review before use

def error_msg_default(prompt, result, error):

    """Default function to append the error message to the prompt.

    Args:

        prompt (list): List of messages in OpenAI format.

        result (str): Result of the LLM query.

        error (str): Error message for the LLM.

    Returns:

        prompt (list): List of messages in OpenAI format.

    """

    prompt.append({"role": "assistant", "content": result})

    prompt.append({"role": "user", "content": error})

    return prompt


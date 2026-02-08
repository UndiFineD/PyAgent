# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\config\llm.py
from environment.config.config import config
from openai import OpenAI


def get_client(model_prefix=None):
    """Get OpenAI client with appropriate credentials based on model prefix"""
    # Get model-specific API key and base URL if available, otherwise use defaults
    if model_prefix and f"{model_prefix}_api_key" in config["llm"]:
        api_key = config["llm"][f"{model_prefix}_api_key"]
        base_url = config["llm"][f"{model_prefix}_base_url"]
    else:
        api_key = config["llm"]["api_key"]
        base_url = config["llm"]["base_url"]

    # Create and return client
    return OpenAI(api_key=api_key, base_url=base_url)


def deepseek(model="deepseek-v3", system=None, user=None, messages=None):
    # Get client for deepseek
    client = get_client("deepseek")

    if messages is not None:
        pass
    else:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        if user is not None:
            messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        response_format={"type": "json_object"},
    )
    return response


def claude(model="claude-3-7-sonnet-20250219", system=None, user=None, messages=None):
    # Get client for claude
    client = get_client("claude")

    if messages is not None:
        pass
    else:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        if user is not None:
            messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    return response


def gemini(model="gemini-2.5-flash", system=None, user=None, messages=None):
    # Get client for gemini
    client = get_client("gemini")

    if messages is not None:
        pass
    else:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        if user is not None:
            messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    return response


def gpt(model="gpt-4o", system=None, user=None, messages=None):
    # Get client for gpt
    client = get_client("gpt")

    if messages is not None:
        pass
    else:
        messages = []
        if system is not None:
            messages.append({"role": "system", "content": system})
        if user is not None:
            messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    return response

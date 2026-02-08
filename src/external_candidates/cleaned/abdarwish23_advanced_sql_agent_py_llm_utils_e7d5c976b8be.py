# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\abdarwish23_advanced_sql_agent.py\app.py\utils.py\llm_utils_e7d5c976b8be.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\abdarwish23-Advanced_SQL_Agent\app\utils\llm_utils.py

# app/utils/llm_utils.py

from app.config import Config

from langchain_anthropic import ChatAnthropic

from langchain_groq import ChatGroq

from langchain_ollama import ChatOllama

from langchain_openai import ChatOpenAI


def get_llm(provider, model_name):

    temperature = Config.LLM_TEMPERATURE

    if provider == "openai":
        return ChatOpenAI(model_name=model_name, temperature=temperature)

    elif provider == "anthropic":
        return ChatAnthropic(model=model_name, temperature=temperature)

    elif provider == "groq":
        return ChatGroq(model_name=model_name, temperature=temperature)

    elif provider == "ollama":
        return ChatOllama(model=model_name, temperature=temperature)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

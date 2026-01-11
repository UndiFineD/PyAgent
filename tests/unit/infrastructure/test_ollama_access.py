
"""Unit tests for local Ollama API connectivity."""
import logging
import sys
import os

from requests import Response

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.infrastructure.backend.LLMClient import LLMClient

def test_ollama() -> None:
    logging.basicConfig(level=logging.DEBUG)
    import requests
    client = LLMClient(requests_lib=requests)
    
    print("Testing Ollama connectivity...")
    # Try a simple prompt. We know 'llama3' was mentioned in SubagentRunner,
    # but the 'tags' API showed empty models. Let's try to pull 'tinyllama' if it fails,
    # or just report the failure.
    
    # Actually, let's just try to call it.
    res: str = client.llm_chat_via_ollama(prompt="hi", model="tinyllama")
    if res:
        print(f"Ollama Success! Response: {res}")
    else:
        print("Ollama failed to respond (maybe model not downloaded?).")
        print("Checking if we can reach the server at all...")
        import requests
        try:
            resp: Response = requests.get("http://localhost:11434/api/tags")
            print(f"Tags response: {resp.json()}")
        except Exception as e: Exception:
            print(f"Could not reach Ollama server: {e}")

if __name__ == "__main__":
    test_ollama()

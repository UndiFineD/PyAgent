# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\embedding.py\ollama_d2514d827455.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\embedding\ollama.py

from typing import Literal

from httpx import Client

from requests import ConnectionError, HTTPError, RequestException

from src.embedding import BaseEmbedding


class OllamaEmbedding(BaseEmbedding):
    def embed(self, text):

        url = self.base_url or f"http://localhost:11434/api/embed"

        headers = self.headers

        payload = {"model": self.model, "input": text}

        try:
            with Client() as client:
                response = client.post(url=url, json=payload, headers=headers)

            response.raise_for_status()

            return response.json()["embeddings"][0]

        except HTTPError as err:
            print(f"Error: {err.response.text}, Status Code: {err.response.status_code}")

        except ConnectionError as err:
            print(err)

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\memory-search-simple-test.py
import json
import os

from mem0 import Memory

# Basic configuration
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "praison",
            "path": ".praison",
        },
    }
}

# Initialize memory
memory = Memory.from_config(config)

# Search Alice's hobbies
search_results = memory.search(query="KAG", user_id="user1", limit=5)

print(search_results)

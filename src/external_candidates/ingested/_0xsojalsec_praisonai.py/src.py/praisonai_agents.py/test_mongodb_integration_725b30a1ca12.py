# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\test_mongodb_integration.py
#!/usr/bin/env python3
"""Test MongoDB integration"""

import sys

sys.path.insert(0, "src/praisonai-agents")

try:
    from praisonaiagents.tools.mongodb_tools import MongoDBTools

    print("MongoDB tools import successful")

    # Test basic initialization (should work even without MongoDB running)
    tools = MongoDBTools()
    print("MongoDB tools initialization successful")

    # Test function imports
    from praisonaiagents.tools import mongodb_tools

    print("MongoDB tools module import successful")

    # Test individual function imports
    from praisonaiagents.tools import find_documents, insert_document, vector_search

    print("Individual MongoDB function imports successful")

    print("All MongoDB integration tests passed")
except Exception as e:
    print(f"MongoDB integration test failed: {e}")
    import traceback

    traceback.print_exc()

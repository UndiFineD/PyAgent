# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\test_import_debug.py
#!/usr/bin/env python3
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
# Add the praisonai-agents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "praisonai-agents"))

print("Testing import functionality...")

try:
    import praisonaiagents

    print("✓ praisonaiagents module is available")

    # Test importing specific classes
    try:
        from praisonaiagents import Agent, PraisonAIAgents, Task

        print(
            "✓ Successfully imported Agent, Task, PraisonAIAgents from praisonaiagents"
        )
    except ImportError as e:
        print(f"❌ Failed to import specific classes: {e}")

except ImportError as e:
    print(f"❌ praisonaiagents module not available: {e}")

# Test the praisonai package
try:
    import praisonai

    print("✓ praisonai package is available")

    # Test importing from praisonai
    try:
        from praisonai import Agent, PraisonAIAgents, Task

        print("✓ Successfully imported Agent, Task, PraisonAIAgents from praisonai")
    except ImportError as e:
        print(f"❌ Failed to import from praisonai: {e}")

except ImportError as e:
    print(f"❌ praisonai package not available: {e}")

# Check what's in the praisonai package
try:
    import praisonai

    print(f"praisonai package contents: {dir(praisonai)}")
    if hasattr(praisonai, "__all__"):
        print(f"praisonai.__all__: {praisonai.__all__}")

    # Check what we can actually import
    print("\nTesting actual imports:")
    for symbol in ["PraisonAI", "__version__", "Agent", "Task", "PraisonAIAgents"]:
        if hasattr(praisonai, symbol):
            print(f"✓ {symbol} is available")
        else:
            print(f"❌ {symbol} is NOT available")

except Exception as e:
    print(f"Error checking praisonai package: {e}")

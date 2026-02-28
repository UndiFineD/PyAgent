# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\validate_fix.py
import ast

try:
    with open("praisonaiagents/agent/agent.py", "r") as f:
        content = f.read()

    ast.parse(content)
    print("SUCCESS: agent.py syntax is valid")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
    print(f"Line {e.lineno}: {e.text}")
except Exception as e:
    print(f"ERROR: {e}")

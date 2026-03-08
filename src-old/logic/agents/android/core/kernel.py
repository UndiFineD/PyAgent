"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/android/core/kernel.description.md

# kernel

**File**: `src\logic\agents\android\core\kernel.py`  
**Type**: Python Module  
**Summary**: 0 classes, 5 functions, 8 imports  
**Lines**: 131  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for kernel.

## Functions (5)

### `run_adb_command(command)`

Executes a shell command via ADB.

### `get_screen_state()`

Dumps the current UI XML and returns the sanitized JSON string.

### `execute_action(action)`

Executes the action decided by the LLM.

### `get_llm_decision(goal, screen_context)`

Sends screen context to LLM and asks for the next move.

### `run_agent(goal, max_steps)`

## Dependencies

**Imports** (8):
- `json`
- `openai.OpenAI`
- `os`
- `sanitizer`
- `subprocess`
- `time`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/android/core/kernel.improvements.md

# Improvements for kernel

**File**: `src\logic\agents\android\core\kernel.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `kernel_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import os
import time
import subprocess
import json
from typing import Dict, Any, List
from openai import OpenAI
import sanitizer

# --- CONFIGURATION ---
ADB_PATH = "adb"  # Ensure adb is in your PATH
MODEL = "gpt-4o"  # Or "gpt-4-turbo" for faster/cheaper execution
SCREEN_DUMP_PATH = "/sdcard/window_dump.xml"
LOCAL_DUMP_PATH = "window_dump.xml"

_OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if _OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=_OPENAI_API_KEY)
    except Exception:
        # Fail-safe: if client cannot be constructed at import-time, set to None
        client = None
else:
    # Tests/import-time checks shouldn't require an active OpenAI client.
    client = None


def run_adb_command(command: List[str]):
    """Executes a shell command via ADB."""
    result = subprocess.run([ADB_PATH] + command, capture_output=True, text=True)
    if result.stderr and "error" in result.stderr.lower():
        print(f"❌ ADB Error: {result.stderr.strip()}")
    return result.stdout.strip()


def get_screen_state() -> str:
    """Dumps the current UI XML and returns the sanitized JSON string."""
    # 1. Capture XML
    run_adb_command(["shell", "uiautomator", "dump", SCREEN_DUMP_PATH])

    # 2. Pull to local
    run_adb_command(["pull", SCREEN_DUMP_PATH, LOCAL_DUMP_PATH])

    # 3. Read & Sanitize
    if not os.path.exists(LOCAL_DUMP_PATH):
        return "Error: Could not capture screen."

    with open(LOCAL_DUMP_PATH, "r", encoding="utf-8") as f:
        xml_content = f.read()

    elements = sanitizer.get_interactive_elements(xml_content)
    return json.dumps(elements, indent=2)


def execute_action(action: Dict[str, Any]):
    """Executes the action decided by the LLM."""
    act_type = action.get("action")

    if act_type == "tap":
        x, y = action.get("coordinates")
        print(f"👉 Tapping: ({x}, {y})")
        run_adb_command(["shell", "input", "tap", str(x), str(y)])

    elif act_type == "type":
        text = action.get("text").replace(" ", "%s")  # ADB requires %s for spaces
        print(f"⌨️ Typing: {action.get('text')}")
        run_adb_command(["shell", "input", "text", text])

    elif act_type == "home":
        print("🏠 Going Home")
        run_adb_command(["shell", "input", "keyevent", "KEYWORDS_HOME"])

    elif act_type == "back":
        print("🔙 Going Back")
        run_adb_command(["shell", "input", "keyevent", "KEYWORDS_BACK"])

    elif act_type == "wait":
        print("⏳ Waiting...")
        time.sleep(2)

    elif act_type == "done":
        print("✅ Goal Achieved.")
        exit(0)


def get_llm_decision(goal: str, screen_context: str) -> Dict[str, Any]:
    """Sends screen context to LLM and asks for the next move."""
    system_prompt = """
    You are an Android Driver Agent. Your job is to achieve the user's goal by navigating the UI.
    
    You will receive:
    1. The User's Goal.
    2. A list of interactive UI elements (JSON) with their (x,y) center coordinates.
    
    You must output ONLY a valid JSON object with your next action.
    
    Available Actions:
    - {"action": "tap", "coordinates": [x, y], "reason": "Why you are tapping"}
    - {"action": "type", "text": "Hello World", "reason": "Why you are typing"}
    - {"action": "home", "reason": "Go to home screen"}
    - {"action": "back", "reason": "Go back"}
    - {"action": "wait", "reason": "Wait for loading"}
    - {"action": "done", "reason": "Task complete"}
    
    Example Output:
    {"action": "tap", "coordinates": [540, 1200], "reason": "Clicking the 'Connect' button"}
    """

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"GOAL: {goal}\n\nSCREEN_CONTEXT:\n{screen_context}",
            },
        ],
    )

    return json.loads(response.choices[0].message.content)


def run_agent(goal: str, max_steps=10):
    print(f"🚀 Android Use Agent Started. Goal: {goal}")

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        # 1. Perception
        print("👀 Scanning Screen...")
        screen_context = get_screen_state()

        # 2. Reasoning
        print("🧠 Thinking...")
        decision = get_llm_decision(goal, screen_context)
        print(f"💡 Decision: {decision.get('reason')}")

        # 3. Action
        execute_action(decision)

        # Wait for UI to update
        time.sleep(2)


if __name__ == "__main__":
    # Example Goal: "Open settings and turn on Wi-Fi"
    # Or your demo goal: "Find the 'Connect' button and tap it"
    GOAL = input("Enter your goal: ")
    run_agent(GOAL)

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\demo\chat_with_memory.py
"""Memory Enhanced Chat Script

Usage:
    uv run python src/bootstrap.py demo/chat_with_memory.py

Alternative:
    cd demo
    python chat_with_memory.py
"""

import asyncio
from pathlib import Path

from demo.chat import ChatOrchestrator
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def main():
    """Main Entry - Start Chat Application"""
    orchestrator = ChatOrchestrator(PROJECT_ROOT)
    await orchestrator.run()


if __name__ == "__main__":
    asyncio.run(main())

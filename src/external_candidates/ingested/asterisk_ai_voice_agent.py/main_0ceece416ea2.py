# Extracted from: C:\DEV\PyAgent\.external\Asterisk-AI-Voice-Agent\main.py
import asyncio
import os

from src.engine import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

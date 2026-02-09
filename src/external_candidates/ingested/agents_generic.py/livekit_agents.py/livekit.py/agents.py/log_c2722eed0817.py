# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\log.py
import logging

DEV_LEVEL = 23
logging.addLevelName(DEV_LEVEL, "DEV")

logger = logging.getLogger("livekit.agents")

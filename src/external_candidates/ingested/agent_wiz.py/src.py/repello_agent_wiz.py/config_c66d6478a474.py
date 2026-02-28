# Extracted from: C:\DEV\PyAgent\.external\agent_wiz\src\repello_agent_wiz\config.py
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

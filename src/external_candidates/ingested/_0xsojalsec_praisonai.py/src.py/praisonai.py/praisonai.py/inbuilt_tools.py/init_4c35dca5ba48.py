# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai\praisonai\inbuilt_tools\__init__.py
# Only try to import autogen_tools if either CrewAI or AG2 is available
CREWAI_AVAILABLE = False
AUTOGEN_AVAILABLE = False
PRAISONAI_TOOLS_AVAILABLE = False

try:
    from crewai import Agent, Crew, Task

    CREWAI_AVAILABLE = True
except ImportError:
    pass

try:
    import autogen

    AUTOGEN_AVAILABLE = True
except ImportError:
    pass

# Only try to import tools if a framework is available
if CREWAI_AVAILABLE or AUTOGEN_AVAILABLE:
    try:
        from .autogen_tools import *

        PRAISONAI_TOOLS_AVAILABLE = True
    except ImportError:
        pass

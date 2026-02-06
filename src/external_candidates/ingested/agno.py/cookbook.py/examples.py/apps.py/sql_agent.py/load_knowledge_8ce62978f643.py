# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\examples\apps\sql_agent\load_knowledge.py
from agents import agent_knowledge
from agno.utils.log import logger


def load_knowledge(recreate: bool = True):
    logger.info("Loading SQL agent knowledge.")
    agent_knowledge.load(recreate=recreate)
    logger.info("SQL agent knowledge loaded.")


if __name__ == "__main__":
    load_knowledge()

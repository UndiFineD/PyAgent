# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\workshops\rag\template\tools\agent_app.py
import click
from rag_workshop.agents import build_agent
from smolagents import GradioUI


@click.command()
def main() -> None:
    """Run the RAG agent with a Gradio web interface.

    This function initializes a RAG (Retrieval-Augmented Generation) agent and launches
    a Gradio web interface for interactive use. The interface allows users to submit
    queries and receive responses from the agent.

    Returns:
        None
    """

    agent = build_agent()
    GradioUI(agent).launch()


if __name__ == "__main__":
    main()

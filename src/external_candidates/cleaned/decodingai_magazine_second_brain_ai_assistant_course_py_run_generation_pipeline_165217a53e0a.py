# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\workshops.py\rag.py\template.py\tools.py\run_generation_pipeline_165217a53e0a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\workshops\rag\template\tools\run_generation_pipeline.py

import os

import click

from rag_workshop.config import settings

from rag_workshop.generation import create_rag_chain


def setup_environment() -> None:
    """

    Set up the environment variables needed for the application.

    """

    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


@click.command()
def main() -> None:
    """

    Main function to demonstrate RAG functionality.

    Runs a series of example questions through a RAG chain and prints the results.

    """

    setup_environment()

    rag_chain = create_rag_chain()

    # Example queries

    questions = [
        "How does BERT work?",
        "How are similarity scores normalized?",
        "What is the difference between dynamic and continuous batching?",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        answer = rag_chain.invoke(question)

        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()

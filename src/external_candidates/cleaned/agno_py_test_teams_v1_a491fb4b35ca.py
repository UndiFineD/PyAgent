# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\tests.py\integration.py\teams.py\test_teams_v1_a491fb4b35ca.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\tests\integration\teams\test_teams_v1.py

from agno.agent import Agent

from agno.models.openai import OpenAIChat

from agno.tools.duckduckgo import DuckDuckGoTools


def test_team_basic():
    """Test basic functionality of a team."""

    researcher = Agent(
        name="Researcher",
        model=OpenAIChat("gpt-4o"),
        role="Research information",
        tools=[DuckDuckGoTools(cache_results=True)],
    )

    writer = Agent(
        name="Writer",
        model=OpenAIChat("gpt-4o"),
        role="Write content based on research",
    )

    team = Agent(
        name="Content Team",
        model=OpenAIChat("gpt-4o"),
        role="Content Team",
        team=[researcher, writer],
        instructions=[
            "First, have the Researcher gather information on the topic.",
            "Then, have the Writer create content based on the research.",
        ],
    )

    response = team.run("Write a short article about climate change solutions")

    assert response.content is not None

    assert isinstance(response.content, str)

    assert len(response.content) > 0

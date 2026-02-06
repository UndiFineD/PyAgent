# Extracted from: C:\DEV\PyAgent\.external\agno\cookbook\reasoning\agents\is_9_11_bigger_than_9_9.py
from agno.agent import Agent
from agno.cli.console import console
from agno.models.openai import OpenAIChat

task = "9.11 and 9.9 -- which is bigger?"

regular_agent = Agent(model=OpenAIChat(id="gpt-4o"), markdown=True)
reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

console.rule("[bold green]Regular Agent[/bold green]")
regular_agent.print_response(task, stream=True)
console.rule("[bold yellow]Reasoning Agent[/bold yellow]")
reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)

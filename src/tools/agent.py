"""Build Agent using Microsoft Agent Framework in Python
# Run this python script
> pip install anthropic agent-framework==1.0.0b260107
> python <this-script-path>.py
"""

import asyncio
import os

from agent_framework import MCPStdioTool, MCPStreamableHTTPTool, ToolProtocol, FunctionCallContent
from agent_framework.openai import OpenAIChatClient
from agent_framework.anthropic import AnthropicClient
from anthropic import AsyncAnthropicFoundry
from openai import AsyncOpenAI

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
openaiClient = AsyncOpenAI(
    base_url = "https://models.github.ai/inference",
    api_key = os.environ["GITHUB_TOKEN"],
)

AGENT_NAME = "ai-agent"
AGENT_INSTRUCTIONS = "you are a programmer, you have memory, you can think, you can search the internet. With these capabilities, I can assist you with a wide range of programming tasks. Here are some steps I can take to help you:\nUnderstand Your Request: I'll need a clear description of the programming task or problem you're facing.\nSearch for Information: If necessary, I can search the internet for relevant information, code snippets, or documentation.\nGenerate Code: Based on the information gathered, I can help write or generate the necessary code.\nDebugging: If you're encountering issues with your code, I can assist in identifying and fixing problems.\nExplain Concepts: I can explain programming concepts, best practices, and design patterns to help you understand and improve your code.\nProvide Resources: I can suggest tutorials, documentation, and other learning resources to help you further.\nTo get started, please provide me with more details about the programming task or problem you need help with."

# User inputs for the conversation
USER_INPUTS = [
    "you are a progrmmer",
    "you are a programmer, you have memory, you can think, you can search the internet",
]

def create_mcp_tools() -> list[ToolProtocol]:
    return [
        MCPStreamableHTTPTool(
            name="TavilyMCP".replace("-", "_"),
            description="MCP server for TavilyMCP",
            url="https://mcp.tavily.com/mcp",
            headers={
                "Authorization": "<your-auth-header>",
            }
        ),
        MCPStdioTool(
            name="markitdown-mm4igrov".replace("-", "_"),
            description="MCP server for markitdown-mm4igrov",
            command="uvx",
            args=[
                "markitdown-mcp",
            ]
        ),
        MCPStdioTool(
            name="memory-mm4ii8u0".replace("-", "_"),
            description="MCP server for memory-mm4ii8u0",
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-memory",
            ],
            env={
                "MEMORY_FILE_PATH": os.environ.get("MEMORY_FILE_PATH", ""),
            }
        ),
        MCPStdioTool(
            name="sequential-thinking-mm4illou".replace("-", "_"),
            description="MCP server for sequential-thinking-mm4illou",
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-sequential-thinking",
            ]
        ),
        MCPStreamableHTTPTool(
            name="MicrosoftLearnMCPserver".replace("-", "_"),
            description="MCP server for MicrosoftLearnMCPserver",
            url="https://learn.microsoft.com/api/mcp",
            headers={
            }
        ),
    ]

async def main() -> None:
    async with (
        OpenAIChatClient(
            async_client=openaiClient,
            model_id="mistral-ai/Codestral-2501"
        ).create_agent(
            instructions=AGENT_INSTRUCTIONS,
            temperature=0.8,
            top_p=0.1,
            tools=[
                *create_mcp_tools(),
            ],
        ) as agent
    ):
        # Process user messages
        for user_input in USER_INPUTS:
            print(f"\n# User: '{user_input}'")
            printed_tool_calls = set()
            async for chunk in agent.run_stream([user_input]):
                # log tool calls if any
                function_calls = [
                    c for c in chunk.contents 
                    if isinstance(c, FunctionCallContent)
                ]
                for call in function_calls:
                    if call.call_id not in printed_tool_calls:
                        print(f"Tool calls: {call.name}")
                        printed_tool_calls.add(call.call_id)
                if chunk.text:
                    print(chunk.text, end="")
            print("")
        
        print("\n--- All tasks completed successfully ---")

    # Give additional time for all async cleanup to complete
    await asyncio.sleep(1.0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Program finished.")

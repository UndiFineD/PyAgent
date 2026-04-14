import subprocess
import sys

from src.tools.tool_registry import list_tools


def test_tools_list_all_registered() -> None:
    tools = list_tools()
    assert tools, "No tools registered"


def test_tools_cli_help_for_each_tool() -> None:
    # Each registered tool should support --help without failing.
    for tool in list_tools():
        result = subprocess.run(
            [sys.executable, "-m", "src.tools", tool.name, "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"{tool.name} help failed: {result.stderr}"
        assert "usage:" in result.stdout.lower(), f"{tool.name} help output missing usage"

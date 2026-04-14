import subprocess
import sys


def test_tools_cli_help_runs_successfully() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "src.tools", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Run a registered PyAgent tool" in result.stdout


def test_tools_cli_runs_netcalc_tool() -> None:
    # A simple execution to ensure the CLI can dispatch to a registered tool.
    result = subprocess.run(
        [sys.executable, "-m", "src.tools", "netcalc", "cidr", "192.168.0.0/24"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Network:" in result.stdout

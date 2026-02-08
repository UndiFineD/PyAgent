# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\cli.py\main_9d5cecb5c297.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\cli\main.py

"""

Guardian CLI - Main entry point

AI-Powered Penetration Testing Automation Tool

"""

import sys

from pathlib import Path

from typing import Optional

import typer

# Import command groups

from cli.commands import ai_explain, analyze, init, recon, report, scan, workflow

from rich.console import Console

from rich.panel import Panel

# Initialize Typer app

app = typer.Typer(
    name="guardian",
    help="🔐 Guardian - AI-Powered Penetration Testing CLI Tool",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()

# Register command groups

app.command(name="init")(init.init_command)

app.command(name="scan")(scan.scan_command)

app.command(name="recon")(recon.recon_command)

app.command(name="analyze")(analyze.analyze_command)

app.command(name="report")(report.report_command)

app.command(name="workflow")(workflow.workflow_command)

app.command(name="ai")(ai_explain.explain_command)


@app.callback()
def callback():
    """

    Guardian - AI-Powered Penetration Testing CLI Tool

    Leverage Google Gemini AI to orchestrate intelligent penetration testing workflows.

    """

    pass


def version_callback(value: bool):
    """Print version and exit"""

    if value:
        console.print("[bold green]Guardian[/bold green] v0.1.0")

        console.print("AI-Powered Penetration Testing Tool")

        raise typer.Exit()


@app.command()
def version(
    show: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """Show Guardian version"""

    pass


def main():
    """Main entry point"""

    try:
        # Display banner

        banner = """

╔═══════════════════════════════════════════╗

║   🔐 GUARDIAN - AI Pentest Automation    ║

║   Powered by Google Gemini & LangChain   ║

╚═══════════════════════════════════════════╝

"""

        console.print(banner, style="bold cyan")

        # Run app

        app()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")

        sys.exit(0)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

        sys.exit(1)


if __name__ == "__main__":
    main()

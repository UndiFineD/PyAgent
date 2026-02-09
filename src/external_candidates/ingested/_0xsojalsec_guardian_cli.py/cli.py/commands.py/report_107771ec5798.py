# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\cli\commands\report.py
"""
guardian report - Generate reports
"""

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def report_command(
    session_id: str = typer.Option(
        ..., "--session", "-s", help="Session ID to generate report for"
    ),
    format: str = typer.Option(
        "markdown", "--format", "-f", help="Report format (markdown, html, json)"
    ),
    output: Path = typer.Option(None, "--output", "-o", help="Output file path"),
    config_file: Path = typer.Option(
        "config/guardian.yaml", "--config", "-c", help="Configuration file path"
    ),
):
    """
    Generate penetration testing report

    Creates a professional report from session data.
    """
    import asyncio
    from pathlib import Path

    from ai.gemini_client import GeminiClient
    from utils.helpers import load_config

    from core.memory import PentestMemory
    from core.reporter_agent import ReporterAgent

    console.print(f"[bold cyan]📄 Generating Report: {session_id}[/bold cyan]\n")

    # Load session
    session_file = Path(f"./reports/session_{session_id}.json")
    if not session_file.exists():
        console.print(f"[red]Session not found: {session_file}[/red]")
        raise typer.Exit(1)

    try:
        # Load configuration and session
        config = load_config(str(config_file))
        memory = PentestMemory(target="")
        memory.load_state(session_file)

        # Initialize Reporter Agent
        gemini = GeminiClient(config)
        reporter = ReporterAgent(config, gemini, memory)

        # Generate report
        console.print(f"Generating {format} report...")
        report = asyncio.run(reporter.execute(format=format))

        # Determine output path
        if not output:
            ext = {"markdown": "md", "html": "html", "json": "json"}.get(format, "txt")
            output = Path(f"./reports/report_{session_id}.{ext}")

        # Save report
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(report["content"])

        console.print(f"\n[green]✓ Report generated successfully![/green]")
        console.print(f"Output: [cyan]{output}[/cyan]")
        console.print(f"Format: [cyan]{format}[/cyan]")
        console.print(f"Findings: [cyan]{len(memory.findings)}[/cyan]")

    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        raise typer.Exit(1)

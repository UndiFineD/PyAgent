# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\cli\commands\workflow.py
"""
guardian workflow - Run predefined workflows
"""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from utils.helpers import load_config

from core.workflow import WorkflowEngine

console = Console()


def workflow_command(
    action: str = typer.Argument(..., help="Action: 'run' or 'list'"),
    name: str = typer.Option(
        None, "--name", "-n", help="Workflow name (recon, web, network, autonomous)"
    ),
    target: str = typer.Option(None, "--target", "-t", help="Target for the workflow"),
    config_file: Path = typer.Option(
        "config/guardian.yaml", "--config", "-c", help="Configuration file path"
    ),
):
    """
    Run or list penetration testing workflows

    Available workflows:
    - recon: Reconnaissance workflow
    - web: Web application pentest
    - network: Network infrastructure pentest
    - autonomous: AI-driven autonomous testing
    """
    if action == "list":
        _list_workflows()
        return

    if action == "run":
        if not name:
            console.print(
                "[bold red]Error:[/bold red] --name is required for 'run' action"
            )
            raise typer.Exit(1)

        if not target:
            console.print(
                "[bold red]Error:[/bold red] --target is required for 'run' action"
            )
            raise typer.Exit(1)

        _run_workflow(name, target, config_file)
    else:
        console.print(f"[bold red]Error:[/bold red] Unknown action: {action}")
        raise typer.Exit(1)


def _list_workflows():
    """List available workflows"""
    table = Table(title="Available Workflows")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("recon", "Reconnaissance: subdomain enum, port scan, tech detection")
    table.add_row("web", "Web Application: HTTP probing, vulnerability scanning")
    table.add_row("network", "Network Infrastructure: port scanning, service detection")
    table.add_row("autonomous", "AI-Driven: fully autonomous testing with AI decisions")

    console.print(table)


def _run_workflow(name: str, target: str, config_file: Path):
    """Run a workflow"""
    console.print(f"[bold cyan]🚀 Running {name} workflow on {target}[/bold cyan]\n")

    config = load_config(str(config_file))

    try:
        engine = WorkflowEngine(config, target)

        if name == "autonomous":
            results = asyncio.run(engine.run_autonomous())
        else:
            results = asyncio.run(engine.run_workflow(name))

        console.print(f"\n[bold green]✓ Workflow completed![/bold green]")
        console.print(f"Findings: [cyan]{results['findings']}[/cyan]")
        console.print(f"Session: [cyan]{results['session_id']}[/cyan]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)

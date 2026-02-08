# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_guardian_cli.py\cli.py\commands.py\recon_9322e686b257.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\cli\commands\recon.py

"""

guardian recon - Reconnaissance command

"""

import asyncio

from pathlib import Path

import typer

from rich.console import Console

from rich.progress import Progress, SpinnerColumn, TextColumn

from rich.table import Table

from utils.helpers import is_valid_domain, is_valid_url, load_config

from core.workflow import WorkflowEngine

console = Console()


def recon_command(
    domain: str = typer.Option(..., "--domain", "-d", help="Target domain for reconnaissance"),
    config_file: Path = typer.Option("config/guardian.yaml", "--config", "-c", help="Configuration file path"),
    save_results: bool = typer.Option(True, "--save/--no-save", help="Save results to file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without executing"),
):
    """

    Run reconnaissance workflow on a target domain

    Performs:

    - Subdomain enumeration

    - Port scanning

    - Service detection

    - Technology fingerprinting

    """

    console.print(f"[bold cyan]🔍 Starting Reconnaissance: {domain}[/bold cyan]\n")

    # Validate target

    if not is_valid_domain(domain) and not is_valid_url(domain):
        console.print(f"[bold red]Error:[/bold red] Invalid domain: {domain}")

        raise typer.Exit(1)

    if dry_run:
        console.print("[yellow]DRY RUN MODE - No actual scanning will occur[/yellow]\n")

        _show_recon_plan(domain)

        return

    # Load configuration

    config = load_config(str(config_file))

    # Run workflow

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running reconnaissance workflow...", total=None)

            # Run async workflow

            results = asyncio.run(_run_recon_workflow(config, domain))

            progress.update(task, completed=True)

        # Display results

        _display_results(results)

        console.print(f"\n[bold green]✓ Reconnaissance completed![/bold green]")

        console.print(f"Session ID: [cyan]{results['session_id']}[/cyan]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

        raise typer.Exit(1)


async def _run_recon_workflow(config: dict, domain: str) -> dict:
    """Run the reconnaissance workflow"""

    engine = WorkflowEngine(config, domain)

    results = await engine.run_workflow("recon")

    return results


def _show_recon_plan(domain: str):
    """Show what the recon workflow would do"""

    table = Table(title="Reconnaissance Plan")

    table.add_column("Step", style="cyan")

    table.add_column("Tool", style="green")

    table.add_column("Description", style="white")

    table.add_row("1", "Subfinder", f"Enumerate subdomains of {domain}")

    table.add_row("2", "Nmap", f"Scan discovered assets for open ports")

    table.add_row("3", "httpx", f"Probe HTTP services and detect technologies")

    table.add_row("4", "AI Analysis", f"Analyze findings and correlate results")

    console.print(table)


def _display_results(results: dict):
    """Display reconnaissance results"""

    console.print("\n[bold]📊 Results Summary[/bold]\n")

    findings = results.get("findings", 0)

    console.print(f"Total Findings: [cyan]{findings}[/cyan]")

    if "analysis" in results:
        console.print("\n[bold]🤖 AI Analysis:[/bold]")

        console.print(results["analysis"].get("response", "No analysis available"))

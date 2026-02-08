# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\cli\commands\init.py
"""
guardian init - Initialize Guardian configuration
"""

import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()


def init_command(
    config_dir: Path = typer.Option(Path.home() / ".guardian", "--config-dir", "-c", help="Configuration directory"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing configuration"),
):
    """
    Initialize Guardian configuration

    Creates configuration files and sets up the environment.
    """
    console.print("[bold cyan]🔧 Initializing Guardian...[/bold cyan]\n")

    # Create config directory
    config_dir.mkdir(parents=True, exist_ok=True)

    # Copy default config
    config_file = config_dir / "guardian.yaml"
    env_file = config_dir / ".env"

    if config_file.exists() and not force:
        if not Confirm.ask(f"Config file already exists at {config_file}. Overwrite?"):
            console.print("[yellow]Skipping configuration file[/yellow]")
        else:
            _copy_default_config(config_file)
    else:
        _copy_default_config(config_file)

    # Create .env file
    if not env_file.exists() or force:
        console.print("\n[bold]API Key Setup[/bold]")
        api_key = Prompt.ask("Enter your Google Gemini API key", password=True)

        with open(env_file, "w") as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")

        console.print(f"[green]✓[/green] Created environment file at {env_file}")

    # Create reports directory
    reports_dir = Path("./reports")
    reports_dir.mkdir(exist_ok=True)
    console.print(f"[green]✓[/green] Created reports directory at {reports_dir}")

    # Create logs directory
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)
    console.print(f"[green]✓[/green] Created logs directory at {logs_dir}")

    console.print(f"\n[bold green]✓ Guardian initialized successfully![/bold green]")
    console.print(f"\nConfiguration directory: [cyan]{config_dir}[/cyan]")
    console.print(f"Next steps:")
    console.print(f"  1. Edit {config_file} to customize settings")
    console.print(f"  2. Run 'guardian scan --target example.com' to start scanning")


def _copy_default_config(dest: Path):
    """Copy default configuration file"""
    # In production, this would copy from package data
    # For now, create a minimal config
    default_config = """# Guardian Configuration
ai:
  provider: gemini
  model: gemini-2.5-pro
  temperature: 0.2

pentest:
  safe_mode: true
  require_confirmation: true
  max_parallel_tools: 3

output:
  format: markdown
  save_path: ./reports
  verbosity: normal

scope:
  blacklist:
    - 127.0.0.0/8
    - 10.0.0.0/8
    - 172.16.0.0/12
    - 192.168.0.0/16
"""

    with open(dest, "w") as f:
        f.write(default_config)

    console.print(f"[green]✓[/green] Created configuration file at {dest}")

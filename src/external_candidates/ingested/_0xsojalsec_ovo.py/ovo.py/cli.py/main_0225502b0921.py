# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\cli\main.py
import typer
from ovo import __version__, console
from ovo.cli import app as app_cli
from ovo.cli import init, module, scheduler_cli
from ovo.cli.common import OVOCliError
from rich.panel import Panel

app = typer.Typer(
    pretty_exceptions_enable=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.add_typer(init.app, name="init")
app.add_typer(module.app, name="")
app.add_typer(app_cli.app, name="")
app.add_typer(scheduler_cli.app, name="scheduler")


def main():
    version = f"Version [green]{__version__}[/green]"
    console.print(f"""
   ▄▀▀█▄  ▄▖   ▄▄  ▄▀▀█▄   
  █    █▄ █▌   ██ █▄▀▄▀█▄  
 █     ██  █▌ ██ █     ██  
  ▀▄▄▄█▀    ███   ▀▄▄▄█▀   
 {version.rjust(39)}
    """)

    try:
        app()
    except OVOCliError as e:
        console.print(Panel.fit(str(e), title="CLI Error", border_style="red"))


if __name__ == "__main__":
    main()

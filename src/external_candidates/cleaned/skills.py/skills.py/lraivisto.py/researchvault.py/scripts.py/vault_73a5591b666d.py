# Extracted from: C:\DEV\PyAgent\.external\skills\skills\lraivisto\researchvault\scripts\vault.py
import argparse
import json
import os
import sys

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

# Ensure we can import from the parent directory (scripts package)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scripts.core as core
import scripts.db as db
import scripts.scuttle as scuttle_engine

console = Console()

if __name__ == "__main__":
    db.init_db()
    parser = argparse.ArgumentParser(description="Vault Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    # Init
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--id", required=True)
    init_parser.add_argument("--name")
    init_parser.add_argument("--objective", required=True)
    init_parser.add_argument("--priority", type=int, default=0)

    # Export
    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--id", required=True)
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    export_parser.add_argument("--output", help="Output file path")

    # List
    list_parser = subparsers.add_parser("list")

    # Status Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True)
    update_parser.add_argument("--status", choices=["active", "paused", "completed", "failed"])
    update_parser.add_argument("--priority", type=int, help="Update project priority")

    # Scuttle (Ingestion)
    scuttle_parser = subparsers.add_parser("scuttle")
    scuttle_parser.add_argument("url", help="URL to scuttle")
    scuttle_parser.add_argument("--id", required=True, help="Project ID")

    # Search (Hybrid: Cache + Brave API)
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--set-result")

    # Log
    log_parser = subparsers.add_parser("log")
    log_parser.add_argument("--id", required=True)
    log_parser.add_argument("--type", required=True)
    log_parser.add_argument("--step", type=int, default=0)
    log_parser.add_argument("--payload", default="{}")
    log_parser.add_argument("--conf", type=float, default=1.0, help="Confidence score (0.0-1.0)")
    log_parser.add_argument("--source", default="unknown", help="Source of the event (e.g. agent name)")
    log_parser.add_argument("--tags", default="", help="Comma-separated tags for the event")

    # Status
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--id", required=True)
    status_parser.add_argument("--filter-tag", help="Filter events by tag")

    # Insight
    insight_parser = subparsers.add_parser("insight")
    insight_parser.add_argument("--id", required=True)
    insight_parser.add_argument("--add", action="store_true")
    insight_parser.add_argument("--title")
    insight_parser.add_argument("--content")
    insight_parser.add_argument("--url", default="")
    insight_parser.add_argument("--tags", default="")
    insight_parser.add_argument("--filter-tag", help="Filter insights by tag")

    # Interactive Insight Mode
    insight_parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive session to add multiple insights",
    )

    args = parser.parse_args()

    if args.command == "init":
        core.start_project(args.id, args.name or args.id, args.objective, args.priority)
    elif args.command == "export":
        data = core.get_status(args.id)
        if not data:
            console.print(f"[red]Project '{args.id}' not found.[/red]")
        else:
            insights = core.get_insights(args.id)
            export_data = {
                "project": {
                    "id": data["project"][0],
                    "name": data["project"][1],
                    "objective": data["project"][2],
                    "status": data["project"][3],
                    "priority": data["project"][5],
                },
                "findings": [],
            }
            for i in insights:
                evidence = {}
                try:
                    evidence = json.loads(i[2])
                except:
                    pass
                export_data["findings"].append(
                    {
                        "title": i[0],
                        "content": i[1],
                        "source_url": evidence.get("source_url", ""),
                        "tags": i[3],
                        "timestamp": i[4],
                        "confidence": i[5],
                    }
                )

            output = ""
            if args.format == "json":
                output = json.dumps(export_data, indent=2)
            else:
                p = export_data["project"]
                output = f"# Research Vault: {p['name']}\n\n"
                output += f"**Objective:** {p['objective']}\n"
                output += f"**Status:** {p['status']}\n\n"
                output += "## Findings\n\n"
                for f in export_data["findings"]:
                    output += f"### {f['title']} (Conf: {f['confidence']})\n"
                    output += f"- **Source:** {f['source_url']}\n"
                    output += f"- **Tags:** {f['tags']}\n"
                    output += f"- **Date:** {f['timestamp']}\n\n"
                    output += f"{f['content']}\n\n---\n\n"

            if args.output:
                with open(args.output, "w") as f:
                    f.write(output)
                console.print(f"[green]✔ Exported to {args.output}[/green]")
            else:
                print(output)
    elif args.command == "list":
        projects = core.list_projects()
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
        else:
            table = Table(title="Research Vault Projects", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Prior", style="magenta", justify="center")
            table.add_column("Status", style="bold")
            table.add_column("Name", style="green")
            table.add_column("Objective")

            for p in projects:
                # p: id, name, objective, status, created_at, priority
                status_style = "green" if p[3] == "active" else "red" if p[3] == "failed" else "blue"
                table.add_row(
                    p[0],
                    str(p[5]),
                    f"[{status_style}]{p[3].upper()}[/{status_style}]",
                    p[1],
                    p[2],
                )
            console.print(table)
    elif args.command == "update":
        core.update_status(args.id, args.status, args.priority)
    elif args.command == "scuttle":
        try:
            service = core.get_ingest_service()
            console.print(f"[cyan]Ingesting {args.url}...[/cyan]")
            result = service.ingest(args.id, args.url)

            if result.success:
                console.print(f"[green]✔ Ingested:[/green] {result.metadata['title']} ({result.metadata['source']})")
            else:
                console.print(f"[red]Ingest failed:[/red] {result.error}")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
    elif args.command == "search":
        if args.set_result:
            # Agent Mode: Manual Injection
            try:
                result_data = json.loads(args.set_result)
                core.log_search(args.query, result_data)
                console.print(f"[green]✔ Cached provided result for:[/green] {args.query}")
            except json.JSONDecodeError:
                console.print("[red]Error: --set-result must be valid JSON.[/red]")
        else:
            # Standalone Mode: Check Cache -> API
            cached = core.check_search(args.query)
            if cached:
                console.print(f"[dim]Note: Serving cached result for '{args.query}'[/dim]")
                console.print_json(data=cached)
            else:
                try:
                    console.print(f"[cyan]Searching Brave for:[/cyan] {args.query}...")
                    result = core.perform_brave_search(args.query)
                    core.log_search(args.query, result)
                    console.print_json(data=result)
                except core.MissingAPIKeyError:
                    console.print(
                        Panel(
                            "[bold red]Active Search Unavailable[/bold red]\n\n"
                            "To use the Vault in standalone mode, you need a Brave Search API Key.\n"
                            "1. Get a free key: [link]https://brave.com/search/api[/link]\n"
                            "2. Set env var: [bold yellow]export BRAVE_API_KEY=YOUR_KEY[/bold yellow]\n\n"
                            "[dim]Or provide a result manually via --set-result if you are an Agent.[/dim]",
                            title="Setup Required",
                            border_style="red",
                        )
                    )
                except Exception as e:
                    console.print(f"[red]Search failed:[/red] {e}")
    elif args.command == "log":
        core.log_event(
            args.id,
            args.type,
            args.step,
            json.loads(args.payload),
            args.conf,
            args.source,
            args.tags,
        )
        console.print(
            f"[green]✔ Logged[/green] [bold cyan]{args.type}[/] for [bold white]{args.id}[/] (conf: {args.conf}, src: {args.source})"
        )
    elif args.command == "status":
        from rich.console import Group
        from rich.panel import Panel

        status = core.get_status(args.id, tag_filter=args.filter_tag)
        if not status:
            console.print(f"[red]Project '{args.id}' not found.[/red]")
        else:
            p = status["project"]
            # p: id, name, objective, status, created_at, priority

            # Header Info
            info_text = f"[bold white]{p[1]}[/bold white] [dim]({p[0]})[/dim]\n"
            info_text += f"Status: [bold {'green' if p[3] == 'active' else 'red'}]{p[3].upper()}[/]\n"
            info_text += f"Objective: {p[2]}\n"
            info_text += f"Created: {p[4]}"

            # Event Table
            event_table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
            event_table.add_column("Time", style="dim")
            event_table.add_column("Source", style="cyan")
            event_table.add_column("Type", style="yellow")
            event_table.add_column("Conf", justify="right")
            event_table.add_column("Data")

            for e in status["recent_events"]:
                # e: event_type, step, payload, confidence, source, timestamp, tags
                conf_color = "green" if e[3] > 0.8 else "yellow" if e[3] > 0.5 else "red"
                short_time = e[5].split("T")[1][:8]
                event_table.add_row(
                    short_time,
                    e[4],
                    e[0],
                    f"[{conf_color}]{e[3]}[/]",
                    e[2][:50] + "..." if len(e[2]) > 50 else e[2],
                )

            # Insights Panel (if any)
            insights = core.get_insights(args.id)
            if insights:
                insight_table = Table(box=box.SIMPLE, show_header=False)
                for i in insights:
                    insight_table.add_row(f"💡 [bold]{i[0]}[/]: {i[1]}")
                content = Group(
                    info_text,
                    Rule(style="white"),
                    event_table,
                    Rule(style="white"),
                    insight_table,
                )
            else:
                content = Group(info_text, Rule(style="white"), event_table)

            console.print(Panel(content, title=f"Research Vault Status: {p[1]}", border_style="blue"))
    elif args.command == "insight":
        if args.interactive:
            console.print(
                Panel(
                    f"Interactive Insight Mode for [bold cyan]{args.id}[/bold cyan]\nType [bold red]exit[/] to finish.",
                    border_style="green",
                )
            )
            while True:
                title = console.input("[bold yellow]Title[/]: ").strip()
                if title.lower() in ["exit", "quit"]:
                    break
                content = console.input("[bold yellow]Content[/]: ").strip()
                tags = console.input("[bold yellow]Tags (comma-separated)[/]: ").strip()
                conf_str = console.input("[bold yellow]Confidence (0.0-1.0)[/]: ").strip()
                try:
                    conf = float(conf_str) if conf_str else 1.0
                except ValueError:
                    conf = 1.0

                core.add_insight(args.id, title, content, "", tags, confidence=conf)
                console.print("[green]✔ Added.[/green]\n")
        elif args.add:
            if not args.title or not args.content:
                print("Error: --title and --content required for adding insight.")
            else:
                core.add_insight(args.id, args.title, args.content, args.url, args.tags)
                print(f"Added insight to project '{args.id}'.")
        else:
            insights = core.get_insights(args.id, tag_filter=args.filter_tag)
            if not insights:
                print("No insights found" + (f" with tag '{args.filter_tag}'" if args.filter_tag else ""))
            for i in insights:
                evidence = {}
                try:
                    evidence = json.loads(i[2])
                except:
                    pass
                source = evidence.get("source_url", "unknown")
                print(f"[{i[4]}] {i[0]} (Conf: {i[5]})\nContent: {i[1]}\nSource: {source}\nTags: {i[3]}\n")

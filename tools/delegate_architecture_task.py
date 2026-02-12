#!/usr/bin/env python3
"""
Simplified task runner that delegates architecture implementation to GitHub Copilot CLI.
Usage: python tools/delegate_architecture_task.py --spec temp/implement_architecture.json
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def load_spec(path: str) -> dict:
    """Load JSON specification file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_copilot_cli() -> str | None:
    """Find GitHub Copilot CLI executable."""
    # Always prefer invoking via command name, not explicit .BAT path.
    # This keeps logs and behavior consistent with `copilot` usage.
    for command_name in ("copilot", "github-copilot-cli"):
        if shutil.which(command_name):
            return command_name

    # Fallback: if VS Code Copilot CLI is installed but not on PATH, add its folder
    # and still return command name `copilot` (not the .BAT path).
    bundled_bat = os.path.expandvars(
        r"%APPDATA%\Code\User\globalStorage\github.copilot-chat\copilotCli\copilot.BAT"
    )
    if os.path.exists(bundled_bat):
        copilot_dir = os.path.dirname(bundled_bat)
        os.environ["PATH"] = copilot_dir + os.pathsep + os.environ.get("PATH", "")
        return "copilot"

    return None


def run_copilot_cli(cli_path: str, spec_path: str) -> int:
    """Execute Copilot CLI with the specification file.
    
    Uses a 60-second timeout to detect hangs early.
    """
    abs_spec_path = os.path.abspath(spec_path)
    
    # Modern Copilot CLI command (agentic mode)
    prompt = f"Implement the task described in the specification file at: {abs_spec_path}"
    
    cmd = [cli_path, "-p", prompt]
    
    print(f"Executing Copilot CLI...")
    print(f"Spec file: {abs_spec_path}")
    print(f"Command: {cli_path} -p \"<prompt>\"")
    print(f"Timeout: 60 seconds for initial response\n")
    
    try:
        # Run with 60-second timeout to detect hangs
        proc = subprocess.run(
            cmd,
            timeout=60,
            capture_output=False,  # Allow real-time output
            shell=(os.name == 'nt'),  # Use shell on Windows for .BAT files
        )
        return proc.returncode
        
    except subprocess.TimeoutExpired:
        print("\nERROR: Command timed out after 60 seconds. This may indicate:")
        print("   1. Copilot CLI is hanging waiting for input")
        print("   2. The task is taking longer than expected")
        print("   3. There's a configuration issue with the CLI")
        return 124  # Standard timeout exit code
        
    except OSError as e:
        print(f"ERROR: Failed to execute CLI: {e}", file=sys.stderr)
        return 1


def summarize_spec(spec: dict) -> None:
    """Print a summary of the specification."""
    print("=" * 70)
    print("SPECIFICATION SUMMARY")
    print("=" * 70)
    
    if isinstance(spec, dict):
        print(f"Task ID:     {spec.get('task_id', 'N/A')}")
        print(f"Title:       {spec.get('title', 'N/A')}")
        print(f"Priority:    {spec.get('priority', 'N/A')}")
        print(f"Status:      {spec.get('status', 'N/A')}")
        
        if 'requirements' in spec and 'patterns' in spec['requirements']:
            patterns = spec['requirements']['patterns']
            print(f"\nPatterns to implement: {len(patterns)}")
            for i, pattern in enumerate(patterns, 1):
                print(f"  {i}. {pattern.get('name', 'Unnamed')}")
        
        if 'constraints' in spec:
            print(f"\nConstraints: {len(spec['constraints'])}")
    
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Delegate architecture task to GitHub Copilot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/delegate_architecture_task.py --spec temp/implement_architecture.json
  python tools/delegate_architecture_task.py --spec temp/my_task.json --dry-run
        """
    )
    
    parser.add_argument(
        "--spec",
        required=True,
        help="Path to JSON specification file"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be executed without running"
    )
    
    args = parser.parse_args()
    
    # Validate spec file exists
    if not os.path.exists(args.spec):
        print(f"ERROR: Specification file not found: {args.spec}", file=sys.stderr)
        sys.exit(2)
    
    # Load and display specification
    try:
        spec = load_spec(args.spec)
        summarize_spec(spec)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in specification file: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Failed to load specification: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Find Copilot CLI
    cli_path = find_copilot_cli()
    if not cli_path:
        print("ERROR: GitHub Copilot CLI not found!", file=sys.stderr)
        print("\nSearched in:", file=sys.stderr)
        print("  - %APPDATA%\\Code\\User\\globalStorage\\github.copilot-chat\\copilotCli\\copilot.BAT")
        print("  - PATH environment variable (copilot, github-copilot-cli)")
        print("\nPlease install GitHub Copilot CLI or check your PATH.")
        sys.exit(4)
    
    print(f"OK: Found Copilot CLI: {cli_path}\n")
    
    # Dry run mode
    if args.dry_run:
        print("DRY RUN MODE - Would execute:")
        print(f"  CLI: {cli_path}")
        print(f"  Spec: {os.path.abspath(args.spec)}")
        print(f"  Prompt: Implement the task described in the specification file...")
        print("\nOK: Dry run complete.")
        sys.exit(0)
    
    # Execute Copilot CLI
    rc = run_copilot_cli(cli_path, args.spec)
    
    if rc == 0:
        print("\nSUCCESS: Task delegation completed successfully!")
    elif rc == 124:
        print("\nTIMEOUT: Task delegation timed out.")
    else:
        print(f"\nERROR: Task delegation failed with exit code {rc}")
    
    sys.exit(rc)

if __name__ == "__main__":
    main()


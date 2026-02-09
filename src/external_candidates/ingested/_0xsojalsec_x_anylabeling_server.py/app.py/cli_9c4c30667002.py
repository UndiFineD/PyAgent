# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\cli.py
"""Command-line interface for X-AnyLabeling Server."""

import argparse
import os
from pathlib import Path

import uvicorn
from app import __version__
from app.core.config import get_settings


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="x-anylabeling-server",
        description="X-AnyLabeling Server - AI Model Inference Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--host",
        type=str,
        help="Server host (default: from config)",
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Server port (default: from config)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        help="Number of workers (default: from config)",
    )

    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (for development)",
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to server.yaml config file (overrides XANYLABELING_SERVER_CONFIG env var)",
    )

    parser.add_argument(
        "--models-config",
        type=str,
        help="Path to models.yaml config file (overrides XANYLABELING_MODELS_CONFIG env var)",
    )

    args = parser.parse_args()

    # Set environment variables for configs if provided
    if args.config:
        os.environ["XANYLABELING_SERVER_CONFIG"] = str(args.config)
    if args.models_config:
        os.environ["XANYLABELING_MODELS_CONFIG"] = str(args.models_config)

    # Load settings from config file
    config_path = Path(args.config) if args.config else None
    settings, actual_config_path = get_settings(config_path)

    # Override with command-line arguments if provided
    host = args.host or settings.server.host
    port = args.port or settings.server.port
    workers = args.workers or settings.server.workers
    reload = args.reload

    print(f"Starting X-AnyLabeling Server v{__version__}")
    print(f"Server: http://{host}:{port}")
    if args.config:
        print(f"Using server config: {args.config}")
    if args.models_config:
        print(f"Using models config: {args.models_config}")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
    )


if __name__ == "__main__":
    main()

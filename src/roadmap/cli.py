#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PyAgent roadmap CLI.

Usage::

    python -m src.roadmap generate --out <dir>
    python -m src.roadmap vision
    python -m src.roadmap milestones --out <file> --items "Phase 1" "Phase 2"

"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from . import milestones, vision


def generate(outdir: Path | str) -> Path:
    """Generate a full roadmap document in *outdir*."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "roadmap.md"
    text = vision.get_template()
    text += "\n" + "# Milestones\n"
    asyncio.run(milestones.create(outfile, ["TBD"]))
    return outfile


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.roadmap",
        description="PyAgent roadmap generation utilities.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # generate subcommand
    gen = sub.add_parser("generate", help="Generate roadmap.md in output directory.")
    gen.add_argument("--out", default="docs/roadmap", help="Output directory (default: docs/roadmap)")

    # vision subcommand
    sub.add_parser("vision", help="Print the vision template to stdout.")

    # milestones subcommand
    ms = sub.add_parser("milestones", help="Write a milestones file.")
    ms.add_argument("--out", default="docs/roadmap/milestones.md", help="Output file path.")
    ms.add_argument("items", nargs="*", default=["TBD"], help="Milestone items.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    parsed = parser.parse_args(argv)

    if parsed.command == "generate":
        outfile = generate(parsed.out)
        print(f"Generated: {outfile}")
        return 0

    if parsed.command == "vision":
        print(vision.get_template())
        return 0

    if parsed.command == "milestones":
        asyncio.run(milestones.create(parsed.out, parsed.items))
        print(f"Written: {parsed.out}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())

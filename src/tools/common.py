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
"""Shared helper functions used by development utilities."""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, TypeVar

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]

T = TypeVar("T")


def load_config(path: str) -> Any:
    """Load JSON or TOML configuration file.  Dispatches on extension."""
    file_path = Path(path)
    if file_path.suffix.lower() in {".toml"}:
        if tomllib is None:
            raise RuntimeError("TOML support requires Python 3.11+ or the 'tomli' package.")
        with open(file_path, "rb") as f:
            return tomllib.load(f)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_logger(name: str, level: int = logging.WARNING) -> logging.Logger:
    """Return a named logger with a console handler (idempotent)."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


def ensure_dir(path: str | os.PathLike) -> Path:
    """Create *path* (and any parents) if it does not exist.  Returns a Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


async def retry(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> T:
    """Call *fn* up to *max_attempts* times, sleeping *delay* seconds between tries.

    Raises the last exception if all attempts fail.
    """
    last_exc: BaseException | None = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except exceptions as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)
    raise last_exc  # type: ignore[misc]


def format_table(rows: list[list[Any]], headers: list[str]) -> str:
    """Render a list of rows as a fixed-width text table.

    Example::

        >>> print(format_table([["alice", 30], ["bob", 25]], ["Name", "Age"]))
        Name   Age
        -----  ---
        alice  30
        bob    25
    """
    col_count = len(headers)
    str_rows: list[list[str]] = [[str(row[i]) if i < len(row) else "" for i in range(col_count)] for row in rows]
    widths = [max([len(headers[i])] + [len(r[i]) for r in str_rows]) for i in range(col_count)]

    def _render_row(cells: list[str]) -> str:
        """Render a single row of cells, padded to column widths."""
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    header_line = _render_row(headers)
    separator = "  ".join("-" * w for w in widths)
    body = "\n".join(_render_row(r) for r in str_rows)
    return f"{header_line}\n{separator}\n{body}"

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
"""FLM Provider Tokens-Per-Second Benchmark.

Sends repeated chat completions to the FLM provider and reports how many
tokens per second the backend can sustain over a chosen duration.

Usage:
    python scripts/FlmTpsBenchmark.py [options]

Options:
    --base-url URL     FLM base URL  [env: DV_FLM_BASE_URL,
                       default: http://127.0.0.1:52625/v1/]
    --model MODEL      Model name    [env: DV_FLM_DEFAULT_MODEL,
                       default: qwen3.5:4b]
    --timeout SECS     HTTP timeout per request  [env: DV_FLM_TIMEOUT,
                       default: 120]
    --max-retries N    HTTP retries on transient errors  [env: DV_FLM_MAX_RETRIES,
                       default: 3]
    --duration SECS    How long to run  [default: 300 (5 minutes)]
    --max-tokens N     Max completion tokens per request  [default: 512]
    --prompt TEXT      Prompt text to use (repeatable, short prompts are fine)
    --cooldown SECS    Seconds to pause between requests  [default: 0]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Load .env from repo root (if present) before reading any env vars.
# Uses python-dotenv when available; silently skips if not installed.
# ---------------------------------------------------------------------------
_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
if _ENV_FILE.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV_FILE, override=False)  # don't override already-set shell vars
    except ImportError:
        # dotenv not installed — parse manually (key=value, skip comments)
        with _ENV_FILE.open(encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if not _line or _line.startswith("#") or "=" not in _line:
                    continue
                _k, _, _v = _line.partition("=")
                _k = _k.strip()
                _v = _v.strip().strip('"').strip("'")
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

# ---------------------------------------------------------------------------
# Dependency guard — the openai package is required.
# ---------------------------------------------------------------------------
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: 'openai' package is required.  Run: pip install openai", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Default prompt — long enough to generate a decent token stream.
# ---------------------------------------------------------------------------
_DEFAULT_PROMPT = (
    "Explain in detail how the transformer architecture works in modern large-language "
    "models, including the concepts of self-attention, positional encoding, multi-head "
    "attention, feed-forward layers, and how they are combined into an encoder-decoder "
    "or decoder-only model.  Cover the training process and typical inference optimisations."
)

# ANSI
_RESET = "\033[0m"
_BOLD = "\033[1m"
_GREEN = "\033[32m"
_CYAN = "\033[36m"
_YELLOW = "\033[33m"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class _RequestResult:
    """Represents the result of a single completion request,
    including token counts and elapsed time.
    """
    completion_tokens: int
    prompt_tokens: int
    elapsed: float  # seconds

    @property
    def tps(self) -> float:
        """Tokens per second for this request,
        based on completion tokens and elapsed time."""
        if self.elapsed <= 0:
            return 0.0
        return self.completion_tokens / self.elapsed


@dataclass
class _Stats:
    """Accumulates results and computes aggregate statistics for the benchmark run."""
    results: list[_RequestResult] = field(default_factory=list)
    errors: int = 0

    def record(self, r: _RequestResult) -> None:
        """Record the result of a completed request."""
        self.results.append(r)

    @property
    def completed(self) -> int:
        """Number of completed requests (i.e. results recorded)."""
        return len(self.results)

    @property
    def total_completion_tokens(self) -> int:
        """Total completion tokens across all recorded results."""
        return sum(r.completion_tokens for r in self.results)

    @property
    def total_prompt_tokens(self) -> int:
        """Total prompt tokens across all recorded results."""
        return sum(r.prompt_tokens for r in self.results)

    @property
    def total_tokens(self) -> int:
        """Total tokens (prompt + completion) across all recorded results."""
        return self.total_completion_tokens + self.total_prompt_tokens

    @property
    def total_elapsed(self) -> float:
        """Total elapsed time across all recorded results."""
        return sum(r.elapsed for r in self.results)

    @property
    def avg_tps(self) -> float:
        """Overall average: total completion tokens / total wall time in requests."""
        if not self.results or self.total_elapsed <= 0:
            return 0.0
        return self.total_completion_tokens / self.total_elapsed

    @property
    def last_tps(self) -> float:
        """Tokens per second for the most recent request, or 0 if no results."""
        return self.results[-1].tps if self.results else 0.0

    @property
    def max_tps(self) -> float:
        """Maximum tokens per second observed in any single request."""
        return max((r.tps for r in self.results), default=0.0)

    @property
    def min_tps(self) -> float:
        """Minimum tokens per second observed in any single request."""
        return min((r.tps for r in self.results), default=0.0)

    @property
    def avg_completion_tokens(self) -> float:
        """Average completion tokens per request."""
        if not self.results:
            return 0.0
        return self.total_completion_tokens / len(self.results)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Builds the argument parser for the benchmark CLI,
    with options for FLM base URL, model, duration, max tokens, prompt, and cooldown."""
    p = argparse.ArgumentParser(
        description="FLM Provider Tokens-Per-Second Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--base-url",
        default=os.environ.get("DV_FLM_BASE_URL", "http://127.0.0.1:52625/v1/"),
        help="FLM OpenAI-compatible base URL  [env: DV_FLM_BASE_URL]",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("DV_FLM_DEFAULT_MODEL", "qwen3.5:4b"),
        help="Model name  [env: DV_FLM_DEFAULT_MODEL]",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("DV_FLM_TIMEOUT", "120")),
        metavar="SECS",
        help="HTTP request timeout in seconds  [env: DV_FLM_TIMEOUT, default: 120]",
    )
    p.add_argument(
        "--max-retries",
        type=int,
        default=int(os.environ.get("DV_FLM_MAX_RETRIES", "3")),
        metavar="N",
        help="Max HTTP retries on transient errors  [env: DV_FLM_MAX_RETRIES, default: 3]",
    )
    p.add_argument(
        "--duration",
        type=float,
        default=300.0,
        metavar="SECS",
        help="Benchmark duration in seconds  [default: 300]",
    )
    p.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        metavar="N",
        help="Max completion tokens per request  [default: 512]",
    )
    p.add_argument(
        "--prompt",
        default=_DEFAULT_PROMPT,
        help="User prompt text  [default: built-in]",
    )
    p.add_argument(
        "--cooldown",
        type=float,
        default=0.0,
        metavar="SECS",
        help="Pause between requests in seconds  [default: 0]",
    )
    return p


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _fmt_tps(v: float) -> str:
    """Format tokens-per-second value with color and fixed width."""
    return f"{v:7.2f}"


def _fmt_dur(seconds: float) -> str:
    """Format duration in seconds as MM:SS."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def _bar(fraction: float, width: int = 30) -> str:
    """Return a simple text progress bar for the given fraction."""
    filled = int(fraction * width)
    return "[" + "=" * filled + " " * (width - filled) + "]"


def _print_live(stats: _Stats, elapsed_wall: float, duration: float) -> None:
    """Print a live-updating status line with progress bar,
    elapsed time, request counts, and token rates."""
    fraction = min(elapsed_wall / duration, 1.0)
    remaining = max(duration - elapsed_wall, 0.0)
    progress = _bar(fraction)
    line = (
        f"\r{_CYAN}{progress}{_RESET} "
        f"{_fmt_dur(elapsed_wall)}/{_fmt_dur(duration)}  "
        f"req={stats.completed:<4d}  err={stats.errors:<3d}  "
        f"tok/s(cur)={_YELLOW}{_fmt_tps(stats.last_tps)}{_RESET}  "
        f"tok/s(avg)={_GREEN}{_fmt_tps(stats.avg_tps)}{_RESET}  "
        f"remain={_fmt_dur(remaining)}"
    )
    # Pad to terminal width to avoid leftover chars when line shortens
    print(line, end="", flush=True)


def _print_summary(stats: _Stats, wall_time: float, args: argparse.Namespace) -> None:
    """Print a summary report at the end of the benchmark,
    including total requests, errors, token counts, and token rates."""
    print()
    print()
    print(f"{_BOLD}{'═' * 64}{_RESET}")
    print(f"{_BOLD}  FLM Benchmark Summary{_RESET}")
    print(f"{'─' * 64}")
    print(f"  Backend          : {args.base_url}")
    print(f"  Model            : {args.model}")
    print(f"  Timeout          : {args.timeout}s  max_retries={args.max_retries}")
    print(f"  Duration (target): {_fmt_dur(args.duration)} ({args.duration:.0f}s)")
    print(f"  Duration (actual): {_fmt_dur(wall_time)} ({wall_time:.1f}s)")
    print(f"{'─' * 64}")
    print(f"  Requests completed : {stats.completed}")
    print(f"  Errors             : {stats.errors}")
    print(f"{'─' * 64}")
    print(f"  Completion tokens  : {stats.total_completion_tokens:,}")
    print(f"  Prompt tokens      : {stats.total_prompt_tokens:,}")
    print(f"  Total tokens       : {stats.total_tokens:,}")
    print(f"  Avg tokens/request : {stats.avg_completion_tokens:.1f}")
    print(f"{'─' * 64}")
    # Wall-clock TPS (time from start to finish, including cooldown/overhead)
    wall_tps = stats.total_completion_tokens / wall_time if wall_time > 0 else 0.0
    print(f"  Tok/s  (wall-clock): {_GREEN}{_BOLD}{wall_tps:7.2f}{_RESET}")
    print(f"  Tok/s  (avg in-req): {stats.avg_tps:7.2f}")
    print(f"  Tok/s  (max 1 req) : {stats.max_tps:7.2f}")
    print(f"  Tok/s  (min 1 req) : {stats.min_tps:7.2f}")
    print(f"{'═' * 64}")


# ---------------------------------------------------------------------------
# Core benchmark loop
# ---------------------------------------------------------------------------

def _run_benchmark(client: Any, args: argparse.Namespace) -> _Stats:
    """Run the benchmark loop, sending repeated chat completion requests
    to the FLM backend, and recording statistics."""
    stats = _Stats()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": args.prompt},
    ]

    deadline = time.perf_counter() + args.duration
    wall_start = time.perf_counter()

    print(f"\n{_BOLD}Starting FLM TPS benchmark{_RESET}")
    print(f"  URL      : {args.base_url}")
    print(f"  Model    : {args.model}")
    print(f"  Timeout  : {args.timeout}s  max_retries={args.max_retries}")
    print(f"  Target   : {args.duration:.0f}s  max_tokens={args.max_tokens}")
    print()

    while time.perf_counter() < deadline:
        try:
            t0 = time.perf_counter()
            response = client.chat.completions.create(
                messages=messages,
                model=args.model,
                max_tokens=args.max_tokens,
            )
            elapsed = time.perf_counter() - t0

            usage = getattr(response, "usage", None)
            completion_tokens = getattr(usage, "completion_tokens", None) if usage else None
            prompt_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0

            if completion_tokens is None or completion_tokens == 0:
                # Fallback: count words as a rough proxy when usage is absent
                content = response.choices[0].message.content or ""
                completion_tokens = len(content.split())

            stats.record(_RequestResult(
                completion_tokens=int(completion_tokens),
                prompt_tokens=int(prompt_tokens),
                elapsed=elapsed,
            ))

        except KeyboardInterrupt:
            print("\n\n  Interrupted by user.", flush=True)
            break
        except Exception as exc:  # noqa: BLE001
            stats.errors += 1
            print(f"\n  [error] {exc}", flush=True)

        _print_live(stats, time.perf_counter() - wall_start, args.duration)

        if args.cooldown > 0 and time.perf_counter() < deadline:
            time.sleep(args.cooldown)

    return stats


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Main entry point for the benchmark CLI.
    Parses arguments, checks backend reachability,
    and runs the benchmark loop."""

    args = _build_parser().parse_args(argv)

    client = OpenAI(
        base_url=args.base_url,
        api_key="dummy",
        timeout=args.timeout,
        max_retries=args.max_retries,
    )

    # Quick reachability check
    try:
        client.models.list()
    except Exception as exc:
        print(f"ERROR: Cannot reach FLM backend at {args.base_url}: {exc}", file=sys.stderr)
        print("       Is the server running?  Check --base-url.", file=sys.stderr)
        return 1

    wall_start = time.perf_counter()
    try:
        stats = _run_benchmark(client, args)
    except KeyboardInterrupt:
        stats = _Stats()
    wall_time = time.perf_counter() - wall_start

    _print_summary(stats, wall_time, args)

    if stats.completed == 0:
        print("No requests completed — check your FLM backend.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

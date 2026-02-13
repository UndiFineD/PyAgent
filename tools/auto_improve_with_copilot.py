#!/usr/bin/env python3
"""
Iterate Python files under `src/`, extract comments/docstrings, and ask local `copilot` CLI
(or use a safe fallback) to propose improvements. Supports --dry-run and --apply.

Usage examples:
  python tools/auto_improve_with_copilot.py --dry-run --max 10
  python tools/auto_improve_with_copilot.py --apply
"""
# pylint: disable=import-error,broad-except

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
import difflib

# Add the project root to sys.path for imports
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Reuse helper to find Copilot CLI (if installed)
from tools.delegate_architecture_task import find_copilot_cli

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = WORKSPACE_ROOT / "src"
SUGGESTIONS_DIR = WORKSPACE_ROOT / ".suggestions"
SUGGESTIONS_DIR.mkdir(exist_ok=True)

MODULE_DOCSTRING_RE = re.compile(r"^\s*(?:\"\"\"|''')([\s\S]*?)(?:\"\"\"|''')", re.M)
COMMENT_RE = re.compile(r"^\s*#(.*)$", re.M)

# Only allow GitHub free models (updated to match CLI model names)
ALLOWED_GITHUB_FREE_MODELS = [
    "gpt-5-mini",
    "gpt-4.1",
]


@dataclass
class FileAnalysis:
    """Container for analysis results for a single Python file."""
    path: Path
    module_doc: str
    comments: List[str]
    original_text: str


def get_available_models() -> List[str]:
    """Retrieve available GitHub Copilot models from CLI."""
    try:
        cli = find_copilot_cli()
        if not cli:
            return ALLOWED_GITHUB_FREE_MODELS
        proc = subprocess.run(
            [cli, "--list-models"],
            capture_output=True,
            text=True,
            timeout=5,  # Reduced timeout
            shell=(os.name == "nt"),
            check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            return [line.strip() for line in proc.stdout.split("\n") if line.strip()]
    except Exception:
        pass  # Silently fall back
    return ALLOWED_GITHUB_FREE_MODELS


def choose_model(models: List[str]) -> str:
    """Choose the first available model from the list."""
    return models[0] if models else ALLOWED_GITHUB_FREE_MODELS[0]


def filter_allowed_models(models):
    """Filter an iterable of model descriptors to only allowed GitHub-free models.

    `models` may be strings or dict-like objects with `name` or `model` keys.
    """

    def name_of(m):
        """Return a display name for a model descriptor `m`.

        Accepts either a string or a dict-like object with `name`/`model` keys.
        """
        if isinstance(m, str):
            return m
        try:
            return m.get("name") or m.get("model") or str(m)
        except Exception:
            return str(m)

    return [m for m in models if name_of(m) in ALLOWED_GITHUB_FREE_MODELS]


def list_python_files(src_root: Path) -> List[Path]:
    """Return a list of Python files under `src_root` recursively."""
    return [p for p in src_root.rglob("*.py") if p.is_file() and ".suggested" not in p.stem]


def extract_comments_and_docstring(text: str) -> Tuple[str, List[str]]:
    """Extract module docstring and top-level comments from `text`."""
    m = MODULE_DOCSTRING_RE.search(text)
    module_doc = m.group(1).strip() if m else ""
    comments = [c.strip() for c in COMMENT_RE.findall(text) if c.strip()]
    return module_doc, comments


def build_prompt(analysis: FileAnalysis) -> str:
    """Build a detailed, safety-minded prompt sent to Copilot CLI for a file.

    The prompt instructs the model to improve correctness, inline
    documentation and readability while preserving behavior and headers.
    The CLI expects only the full replacement file inside a single fenced
    Python code block; this function enforces that constraint in the text
    sent to the model.
    """

    parts = [
        "You are GitHub Copilot (local CLI). Improve the Python source code below",
        "while preserving behavior and public APIs unless you are fixing a bug.",
        "Only return the full file contents in a single fenced python code block",
        "(no explanations, no additional text).",
        "Preserve file header (encoding / license) exactly as-is.",
        "---",
        "Priority (highest -> lowest):",
        "1) Fix correctness or security bugs.",
        "2) Improve and expand inline documentation: module, function, and parameter",
        "   docstrings. Add short examples for public functions when helpful.",
        "3) Add or tighten type annotations where they can be inferred unambiguously.",
        "4) Refactor for clarity and maintainability: prefer small, local changes.",
        "5) Apply safe lint/format fixes (ruff/flake8 style) and keep max-line-length=120.",
        "6) Do not add network calls, secrets, or external side effects.",
        "If you must change behavior, add a single-line comment above the change:",
        "   # BEHAVIOR CHANGED: <short reason>",
        "If you modify or add public APIs, keep backward compatibility or clearly",
        "document the change in a short comment above the new/changed symbol.",
        "---",
    ]

    if analysis.module_doc:
        parts.append("Context: existing module docstring follows:")
        parts.append(analysis.module_doc)
        parts.append("---")

    if analysis.comments:
        parts.append("Top comments from the file (for context):")
        for c in analysis.comments[:20]:
            parts.append(f"- {c}")
        parts.append("---")

    parts.append("Source:")
    parts.append("```py\n" + analysis.original_text + "\n```")
    parts.append("---\nReturn only the improved file contents in a single fenced python code block.")
    return "\n".join(parts)


def call_copilot_cli(prompt: str, timeout: int = 60) -> Optional[str]:
    """Invoke the Copilot CLI with `prompt` and return its stdout (or None)."""

    available_models = get_available_models()
    available_models = filter_allowed_models(available_models)
    if not available_models:
        raise RuntimeError("No allowed GitHub-free models available.")
    chosen = choose_model(available_models)

    def name_of(m):
        """Return a display name for a model descriptor `m`.

        Accepts either a string or a dict-like object with `name`/`model` keys.
        """
        if isinstance(m, str):
            return m
        try:
            return m.get("name") or m.get("model") or str(m)
        except Exception:
            return str(m)

    model_name = name_of(chosen)

    cli = find_copilot_cli()
    if not cli:
        return None

    shell_flag = os.name == "nt"

    # Try invoking CLI with an explicit model flag, then fall back if the CLI rejects it.
    cmd_with_model = [cli, "-p", prompt, "--model", model_name]
    try:
        proc = subprocess.run(
            cmd_with_model,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=shell_flag,
            check=False,
        )
        if proc.returncode == 0:
            return proc.stdout

        stderr = (proc.stderr or "").lower()
        # If CLI doesn't recognize the flag, retry without model selection.
        if any(
            tok in stderr for tok in ("unknown flag", "unrecognized argument", "unknown option", "unrecognized flag")
        ):
            cmd = [cli, "-p", prompt]
            proc2 = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=shell_flag,
                check=False,
            )
            if proc2.returncode != 0:
                print(f"copilot CLI returned code {proc2.returncode}; stderr:\n{proc2.stderr}")
                return None
            return proc2.stdout

        print(f"copilot CLI returned code {proc.returncode}; stderr:\n{proc.stderr}")
        return None

    except Exception as e:
        print(f"Failed to run copilot CLI: {e}")
        return None


def extract_code_block(response: str) -> Optional[str]:
    """Extract the first fenced Python code block from `response`, if any."""
    # Find the first fenced python code block
    m = re.search(r"```(?:py|python)?\n([\s\S]*?)\n```", response, re.I)
    if m:
        return m.group(1).rstrip() + "\n"
    # If no code block, but response looks like full file, return as-is
    if "def " in response or "class " in response:
        return response
    return None


def safe_fallback_improvement(original: str) -> str:
    """Return a minimal, safe 'improvement' used when Copilot CLI isn't available."""
    # Minimal, safe "improvement" used when Copilot CLI isn't available:
    header = "# Refactored by copilot-placeholder\n"
    if original.startswith("#!"):
        # preserve shebang
        parts = original.split("\n", 1)
        return parts[0] + "\n" + header + (parts[1] if len(parts) > 1 else "")
    return header + original


def analyze_file(path: Path) -> FileAnalysis:
    """Read `path` and return a `FileAnalysis` with extracted comments/docstring."""
    text = path.read_text(encoding="utf-8")
    module_doc, comments = extract_comments_and_docstring(text)
    return FileAnalysis(path=path, module_doc=module_doc, comments=comments, original_text=text)


def propose_improvement_for_file(analysis: FileAnalysis, use_copilot: bool = True) -> Tuple[Path, str, bool]:
    """Return (path, proposed_text, applied_flag).

    applied_flag is True when the proposal was generated by Copilot CLI; False when fallback used.
    """
    prompt = build_prompt(analysis)
    if use_copilot:
        response = call_copilot_cli(prompt)
        if response:
            code = extract_code_block(response)
            if code:
                return analysis.path, code, True
            # if response didn't contain code block but contains full file, accept it
            if response.strip() and response.strip().startswith("#") or "def " in response:
                return analysis.path, response, True
    # fallback
    return analysis.path, safe_fallback_improvement(analysis.original_text), False


def apply_proposal(path: Path, new_text: str, backup: bool = True) -> None:
    """Apply a proposed text change to a file, optionally creating a backup."""
    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(path, bak)
    path.write_text(new_text, encoding="utf-8")


def create_bak_diff(path: Path) -> Optional[Path]:
    """If a backup exists next to `path` (e.g. file.py.bak), write a unified
    diff between the backup and the current file to `file.py.bak.diff` and
    return the diff path. Returns None if no backup or no diff produced.
    """
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        return None
    try:
        bak_text = bak.read_text(encoding="utf-8")
    except Exception:
        bak_text = ""
    try:
        orig_text = path.read_text(encoding="utf-8")
    except Exception:
        orig_text = ""

    diff_lines = list(
        difflib.unified_diff(
            bak_text.splitlines(keepends=False),
            orig_text.splitlines(keepends=False),
            fromfile=str(bak),
            tofile=str(path),
            lineterm="",
        )
    )
    if not diff_lines:
        return None
    diff_path = path.with_suffix(path.suffix + ".bak.diff")
    diff_path.write_text("\n".join(diff_lines) + "\n", encoding="utf-8")
    return diff_path
def attempt_copilot_merge(orig_text: str, suggested_text: str, timeout: int = 120) -> Optional[str]:
    """Ask the Copilot CLI to produce a merged version given three inputs.

    Returns merged text if Copilot returns a code block / plausible file, else None.
    """
    # TODO FIXME: Here you should merge a diff to the original, only if it is an improvement
    prompt_parts = [
        (
            "Here you should merge a diff to the original, only if it is an improvement."
        ),
        "Return only the full file contents in a single fenced python code block (no explanations).",
        "If conflicts exist, make a best-effort merge and prefer code that preserves intended behavior.",
        "---",
        "ORIGINAL (current file):",
        "```py\n" + (orig_text or "") + "\n```",
        "---",
        "DIFF (new proposal):",
        "```py\n" + (suggested_text or "") + "\n```",
        "---",
    ]
    prompt = "\n".join(prompt_parts)
    try:
        resp = call_copilot_cli(prompt, timeout=timeout)
        if not resp:
            return None
        merged = extract_code_block(resp)
        if merged:
            return merged
        # If no fenced block but response looks like a file, accept it
        if resp.strip().startswith("#") or "def " in resp or "class " in resp:
            return resp
    except Exception:
        return None
    return None


def smart_apply_proposal(path: Path, new_text: str, use_copilot_merge: bool = True) -> bool:
    """Attempt to apply a proposal intelligently when a .bak exists.

    Returns True if the file was applied/updated on disk. If a merge conflict
    is detected and no automatic resolution is possible, the function will
    write a suggested file next to the original and return False.
    """
    bak = path.with_suffix(path.suffix + ".bak")
    try:
        orig_text = path.read_text(encoding="utf-8")
    except Exception:
        orig_text = ""

    # If no bak, behave like normal apply_proposal (creates bak then write)
    if not bak.exists():
        apply_proposal(path, new_text, backup=True)
        return True

    try:
        bak_text = bak.read_text(encoding="utf-8")
    except Exception:
        bak_text = ""

    # If backup equals original, safe to overwrite (no intervening manual changes)
    if bak_text == orig_text:
        apply_proposal(path, new_text, backup=True)
        return True

    # There are intervening changes between bak and original. Try Copilot merge if allowed.
    merged = None
    if use_copilot_merge:
        merged = attempt_copilot_merge(bak_text, orig_text, new_text)

    if merged:
        # Persist merged result, keep a backup of current original
        apply_proposal(path, merged, backup=True)
        # write diff between orig and merged
        diff_lines = list(
            difflib.unified_diff(
                orig_text.splitlines(keepends=False),
                merged.splitlines(keepends=False),
                fromfile=str(path),
                tofile=str(path) + " (merged)",
                lineterm="",
            )
        )
        if diff_lines:
            diff_path = path.with_suffix(path.suffix + ".merge.diff")
            diff_path.write_text("\n".join(diff_lines) + "\n", encoding="utf-8")
        return True

    # Could not auto-merge. Save suggestion next to original and leave file untouched.
    suggested = save_suggestion(path, new_text)
    conflict_marker = path.with_suffix(path.suffix + ".merge.conflict")
    conflict_marker.write_text(f"Merge conflict: manual review needed. Suggested file: {suggested}\n", encoding="utf-8")
    print(f"Merge conflict detected for {path}; suggestion saved to {suggested}")
    return False


def save_suggestion(path: Path, new_text: str) -> Path:
    """Save suggestion next to the original file as `<name>.suggested.py` and
    write a unified diff file next to the original as `<file>.py.diff`.

    Returns the `Path` to the written suggested file.
    """
    # Read original text if possible (used to build diff)
    try:
        original_text = path.read_text(encoding="utf-8")
    except Exception:
        original_text = ""

    # Suggested file: same directory as original, with `.suggested.py` suffix
    suggested = path.with_name(path.stem + ".suggested" + path.suffix)
    suggested.parent.mkdir(parents=True, exist_ok=True)
    suggested.write_text(new_text, encoding="utf-8")

    # Run auto-fixers / linters on the suggested file to produce a cleaner proposal.
    try:
        apply_auto_fixes(suggested)
    except Exception:
        # Don't fail saving suggestion if fixers are unavailable or fail.
        pass

    # Write unified diff next to the original file: file.py.diff
    diff_path = path.with_suffix(path.suffix + ".diff")
    diff_lines = list(
        difflib.unified_diff(
            original_text.splitlines(keepends=False),
            new_text.splitlines(keepends=False),
            fromfile=str(path),
            tofile=str(suggested),
            lineterm="",
        )
    )
    if diff_lines:
        diff_text = "\n".join(diff_lines) + "\n"
        diff_path.write_text(diff_text, encoding="utf-8")

    return suggested


def apply_auto_fixes(suggested_path: Path) -> None:
    """Run project auto-fixers on `suggested_path` in-place.

    Steps:
    - Run `ruff format` to format code.
    - Run `ruff check --fix` to apply automatic fixes.
    - Run `mypy` and `pylint` for reports (do not fail on their errors).
    """
    # Prefer ruff for formatting and auto-fixes
    try:
        subprocess.run(["& c:/DEV/PyAgent/.venv/Scripts/Activate.ps1; ruff", "format", str(suggested_path)], check=False)
    except Exception:
        pass

    try:
        subprocess.run(["& c:/DEV/PyAgent/.venv/Scripts/Activate.ps1; ruff", "check", str(suggested_path), "--fix"], check=False)
    except Exception:
        pass

    # Run type/lint checks and capture outputs next to the suggestion for review
    reports = []
    try:
        proc = subprocess.run(
            ["& c:/DEV/PyAgent/.venv/Scripts/Activate.ps1; python", "-m", "mypy", str(suggested_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        reports.append(("mypy", proc.stdout + proc.stderr))
    except Exception:
        pass

    try:
        proc = subprocess.run(["& c:/DEV/PyAgent/.venv/Scripts/Activate.ps1; pylint", str(suggested_path)], capture_output=True, text=True, check=False)
        reports.append(("pylint", proc.stdout + proc.stderr))
    except Exception:
        pass

    if reports:
        rpt_path = suggested_path.with_suffix(suggested_path.suffix + ".lint.txt")
        with rpt_path.open("w", encoding="utf-8") as fh:
            for name, out in reports:
                fh.write(f"=== {name} report ===\n")
                fh.write(out or "(no output)\n")
                fh.write("\n\n")


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the auto-improvement script.

    Parses command-line arguments and processes Python files under the source directory.
    """
    parser = argparse.ArgumentParser(description="Auto-improve Python files using local Copilot CLI (or placeholder)")
    parser.add_argument("--src-dir", default=str(SRC_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--smart-apply",
        action="store_true",
        help="When applying, attempt Copilot-assisted smart merge if backups differ",
    )
    parser.add_argument("--max", type=int, default=0, help="Max files to process (0 = all)")
    args = parser.parse_args(argv)

    files = list_python_files(Path(args.src_dir))
    if args.max > 0:
        files = files[: args.max]

    print(f"Found {len(files)} python files under {args.src_dir}")

    for idx, fp in enumerate(files, start=1):
        print(f"\n[{idx}/{len(files)}] Processing: {fp}")
        analysis = analyze_file(fp)
        # If a backup exists, create a .bak diff for visibility
        try:
            create_bak_diff(fp)
        except Exception:
            pass

        path, proposal, from_copilot = propose_improvement_for_file(analysis, use_copilot=True)
        suggestion_path = save_suggestion(path, proposal)
        if not args.apply:
            print(f"  -> Suggestion saved: {suggestion_path}  (from_copilot={from_copilot})")
        else:
            print(f"  -> Applying proposal to {path}  (from_copilot={from_copilot})")
        if args.apply:
            if args.smart_apply:
                applied = smart_apply_proposal(path, proposal, use_copilot_merge=True)
                if applied:
                    print(f"  -> Smart-applied proposal to {path} (backup created)")
                else:
                    print(f"  -> Proposal saved for manual review: {suggestion_path}")
            else:
                apply_proposal(path, proposal)
                print(f"  -> Applied proposal to {path} (backup created)")
        else:
            print("  -> Dry run (not applied). Use --apply to overwrite files.")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

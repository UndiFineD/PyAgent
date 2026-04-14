"""Minimal context manager helper for orchestration agents.

This module provides a safe, lightweight `assemble_context` function used by
agents when building a redacted context for LLM fallbacks. It handles redaction
of sensitive information and combines task/override/agent code into a compact
context for LLM calls.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any

from backend import PostgresBackend

REDACT_PATTERNS = [
    re.compile(
        (r"(?:api[_-]?key|secret|token|pass(?:word)?)" r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-\./]{8,}['\"]?"),
        re.I,
    ),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    # key=value or "key": "value" patterns for common secret names
    re.compile(
        (
            r"(?:api[_-]?key|client[_-]?secret|secret|token|pass(?:word)?|auth)"
            r"\s*[:=]\s*[\'\"]?[A-Za-z0-9_\-\./+]{8,}[\'\"]?"
        ),
        re.I,
    ),
    # Authorization: Bearer <token>
    re.compile(r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9\-\._~\+/]+=*", re.I),
    # PEM private key blocks
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----", re.I),
    # Emails
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    # Long hex or base64-like strings (likely tokens/keys)
    re.compile(r"\b[0-9a-fA-F]{30,}\b"),
    re.compile(r"\b(?:[A-Za-z0-9+/]{40,}={0,2})\b"),
]


def redact(text: str) -> str:
    """Redact sensitive information from text using predefined patterns."""
    out = text
    for pat in REDACT_PATTERNS:
        out = pat.sub("<REDACTED>", out)

    # Also scrub common JSON keys like "password", "secret", "api_key"
    try:
        # replace occurrences like "key": "value" -> "key": "<REDACTED>"
        json_key_names = [
            "password",
            "pass",
            "secret",
            "api_key",
            "client_secret",
            "token",
            "authorization",
            "access_token",
            "private_key",
        ]
        for key in json_key_names:
            # match "key"\s*:\s*"..." or 'key': '...'
            key_pat = re.compile(rf"([\"']){key}\1\s*:\s*([\"'])(.*?)\2", re.I)
            out = key_pat.sub(rf"\1{key}\1: \2<REDACTED>\2", out)
    except Exception:
        pass

    return out


def _read_agent_file(agent_name: str) -> str:
    """Read the agent's code file as text for context assembly."""
    # Prefer code directory (.github/agents/code) next to this orchestration package
    base = Path(__file__).resolve().parents[1]
    code_dir = base / "code"
    candidates = [code_dir / f"{agent_name}.py", base / f"{agent_name}.py", base / f"{agent_name}.md"]
    for p in candidates:
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                return ""
    return ""


def assemble_context(agent_name: str, task: Dict[str, Any], max_chars: int = 16_000) -> Dict[str, Any]:
    """Assemble a minimal, redacted context for LLM calls.

    Returns a dict with keys: context (str), length (int), redacted (bool)
    """
    backend = PostgresBackend()
    # 1. Task summary
    try:
        task_json = json.dumps(task, default=str)
    except Exception:
        task_json = str(task)

    # 2. Rules/overrides
    try:
        overrides = backend.get_rule_overrides(agent_name) or {}
        overrides_text = json.dumps(overrides, default=str)
    except Exception:
        overrides_text = "{}"

    # 3. Agent code/text
    agent_src = _read_agent_file(agent_name)

    # 4. Combine and redact
    pieces = [f"TASK:\n{task_json}", f"OVERRIDES:\n{overrides_text}"]
    if agent_src:
        pieces.append(f"AGENT_SRC:\n{agent_src}")

    combined = "\n---\n".join(pieces)
    redacted = redact(combined)

    # 5. Truncate to max_chars (simple heuristic to reduce context)
    if len(redacted) > max_chars:
        # keep head and tail
        head = redacted[: max_chars // 2]
        tail = redacted[-(max_chars // 2) :]
        redacted = head + "\n...<TRUNCATED>...\n" + tail

    return {"context": redacted, "length": len(redacted), "redacted": True}

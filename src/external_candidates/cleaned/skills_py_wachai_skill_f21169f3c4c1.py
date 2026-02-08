# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\akshat_mishra101.py\wachai_mandates.py\scripts.py\wachai_skill_f21169f3c4c1.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\akshat-mishra101\wachai-mandates\scripts\wachai_skill.py

#!/usr/bin/env python3

"""

WachAI Mandates Skill - Create, Sign, Verify (ERC-8004 / x402-style agreements)



This script provides a minimal command-line interface for working with WachAI

Mandates using the `mandates-core` Python SDK:

- Create a mandate (server signs first / offer)

- Sign a mandate (client countersigns / accept)

- Verify both signatures



Commands:

- create-mandate --swap <TOKEN_IN> <TOKEN_OUT> <AMOUNT_IN> <AMOUNT_OUT>

- create-mandate --custom <KIND_NAME> --body <INLINE_JSON_OBJECT>

- sign <mandate-id>

- verify <mandate-id>



Environment Variables:

- WACHAI_PRIVATE_KEY: EVM private key used to sign (server for create, client for sign)

- WACHAI_STORE_DIR: Optional override for local mandate storage (default: ~/.wachai/mandates)



Notes:

- A local `.env` in the current working directory is auto-loaded if present (optional).

"""

from __future__ import annotations


import argparse

import ast

import json

import os

import sys

from datetime import datetime, timedelta, timezone

from pathlib import Path

from typing import Any, Dict, Optional


from eth_account import Account

from mandates_core import Mandate, build_core


def _eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def _print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))


# ----------------------------

# .env (optional, dependency-free)

# ----------------------------


def _load_dotenv(path: Optional[Path] = None) -> None:
    """

    Tiny, dependency-free .env loader.

    - Only sets keys that are not already present in os.environ

    - Supports KEY=VALUE lines and ignores blanks/comments

    """

    p = path or (Path.cwd() / ".env")

    if not p.exists() or not p.is_file():
        return

    try:
        raw = p.read_text(encoding="utf-8")

    except Exception:
        return

    for line in raw.splitlines():
        s = line.strip()

        if not s or s.startswith("#"):
            continue

        if "=" not in s:
            continue

        k, v = s.split("=", 1)

        k = k.strip()

        v = v.strip().strip('"').strip("'")

        if k and k not in os.environ:
            os.environ[k] = v


# ----------------------------

# Mandate storage

# ----------------------------


def _default_store_dir() -> Path:
    return Path.home() / ".wachai" / "mandates"


def store_dir() -> Path:
    override = os.environ.get("WACHAI_STORE_DIR")

    return Path(override).expanduser() if override else _default_store_dir()


def mandate_path(mandate_id: str) -> Path:
    return store_dir() / f"{mandate_id}.json"


def save_mandate_dict(mandate: Dict[str, Any], *, path: Optional[Path] = None) -> Path:
    mid = mandate.get("mandateId") or mandate.get("mandate_id") or mandate.get("id")

    if not mid and path is None:
        raise ValueError("Cannot save mandate: missing mandateId")

    p = path or mandate_path(str(mid))

    p.parent.mkdir(parents=True, exist_ok=True)

    p.write_text(json.dumps(mandate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return p


def load_mandate_dict(mandate_id: str) -> Dict[str, Any]:
    p = mandate_path(mandate_id)

    if not p.exists():
        raise FileNotFoundError(
            f"Mandate '{mandate_id}' not found at {p}. (Set WACHAI_STORE_DIR to override storage location.)"
        )

    return json.loads(p.read_text(encoding="utf-8"))


# ----------------------------

# Helpers

# ----------------------------


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_deadlines(*, mandate_minutes: int = 10, swap_minutes: int = 5) -> tuple[str, str]:
    now = utc_now()

    return (
        to_iso_z(now + timedelta(minutes=mandate_minutes)),
        to_iso_z(now + timedelta(minutes=swap_minutes)),
    )


def normalize_private_key(pk: str) -> str:
    pk = pk.strip()

    if not pk:
        raise ValueError("Empty private key")

    if pk.startswith(("0x", "0X")):
        return "0x" + pk[2:]

    return "0x" + pk


def require_private_key(env_var: str = "WACHAI_PRIVATE_KEY") -> str:
    _load_dotenv()  # optional; does nothing if no .env

    val = os.environ.get(env_var)

    if not val:
        raise SystemExit(f"Missing required env var: {env_var}")

    return normalize_private_key(val)


def address_from_private_key(private_key: str) -> str:
    return Account.from_key(private_key).address


def to_caip10(address: str, *, chain_id: int) -> str:
    return f"eip155:{chain_id}:{address}"


def normalize_caip10_or_address(value: str, *, chain_id: int) -> str:
    v = value.strip()

    if v.startswith("eip155:"):
        return v

    if not v.startswith("0x"):
        raise ValueError(f"Expected 0x-address or CAIP-10, got: {value}")

    return to_caip10(v, chain_id=chain_id)


def maybe_parse_int(s: str, *, name: str) -> int:
    try:
        return int(s, 0)

    except Exception as e:
        raise ValueError(f"Invalid {name}: {s}") from e


def _build_swap_core(
    *,
    chain_id: int,
    token_in: str,
    token_out: str,
    amount_in: str,
    min_out: str,
    recipient: str,
    swap_deadline: str,
    primitives_base_url: Optional[str] = None,
) -> Dict[str, Any]:
    payload = {
        "chainId": chain_id,
        "tokenIn": token_in,
        "tokenOut": token_out,
        "amountIn": amount_in,
        "minOut": min_out,
        "recipient": recipient,
        "deadline": swap_deadline,
    }

    # Prefer remote primitive registry (deterministic schema), but fall back to

    # attaching a manual core if offline.

    try:
        if primitives_base_url:
            return build_core("swap@1", payload, base_url=primitives_base_url)

        return build_core("swap@1", payload)

    except Exception:
        return {"kind": "swap@1", "payload": payload}


def parse_inline_object(text: str) -> Dict[str, Any]:
    """

    Parse an inline object passed via CLI.

    - Prefer strict JSON (double quotes)

    - Fallback to Python literal dict syntax (single quotes), via ast.literal_eval

    """

    s = text.strip()

    if not s:
        raise ValueError("Empty --body")

    try:
        obj = json.loads(s)

    except Exception:
        obj = ast.literal_eval(s)

    if not isinstance(obj, dict):
        raise ValueError("--body must be an object/dict")

    return obj


# ----------------------------

# CLI commands

# ----------------------------


def cmd_create_mandate(args: argparse.Namespace) -> int:
    private_key = require_private_key()

    server_address = address_from_private_key(private_key)

    chain_id = args.chain_id

    server_caip10 = (
        normalize_caip10_or_address(args.server, chain_id=chain_id)
        if args.server
        else to_caip10(server_address, chain_id=chain_id)
    )

    if args.client:
        client_caip10 = normalize_caip10_or_address(args.client, chain_id=chain_id)

    else:
        # If client isn't specified, default to self for an easy demo.

        client_caip10 = to_caip10(server_address, chain_id=chain_id)

    mandate_deadline, swap_deadline = default_deadlines()

    if args.deadline:
        mandate_deadline = args.deadline

    if args.swap_deadline:
        swap_deadline = args.swap_deadline

    if args.swap:
        token_in, token_out, amount_in_raw, min_out_raw = args.swap

        amount_in = str(maybe_parse_int(amount_in_raw, name="AMOUNT_IN"))

        min_out = str(maybe_parse_int(min_out_raw, name="AMOUNT_OUT"))

        # Recipient defaults to the client address (CAIP-10 ends with 0x address).

        recipient = args.recipient or client_caip10.split(":")[-1]

        intent = args.intent or f"Swap {amount_in} of {token_in} for >= {min_out} of {token_out} on chain {chain_id}"

        core = _build_swap_core(
            chain_id=chain_id,
            token_in=token_in,
            token_out=token_out,
            amount_in=amount_in,
            min_out=min_out,
            recipient=recipient,
            swap_deadline=swap_deadline,
            primitives_base_url=args.primitives_base_url,
        )

    elif args.custom:
        if not args.body:
            raise SystemExit("Missing required flag for --custom: --body")

        payload = parse_inline_object(args.body)

        intent = args.intent or f"Run custom task {args.custom}"

        core = {"kind": args.custom, "payload": payload}

    else:
        raise SystemExit("create-mandate requires one of: --swap ... OR --custom <KIND> --body <JSON>")

    m = Mandate.new(
        version="0.1.0",
        client=client_caip10,
        server=server_caip10,
        deadline=mandate_deadline,
        intent=intent,
        core=core,
    )

    # Server signs first (offer).

    m.sign_as_server(private_key)

    d = m.to_dict()

    if not args.no_store:
        p = save_mandate_dict(d)

        if args.print_path:
            _eprint(f"Saved: {p}")

    _print_json(d)

    return 0


def cmd_sign(args: argparse.Namespace) -> int:
    private_key = require_private_key()

    d = load_mandate_dict(args.mandate_id)

    m = Mandate(**d)

    # Client countersigns (accept).

    m.sign_as_client(private_key)

    out = m.to_dict()

    save_mandate_dict(out)

    _print_json(out)

    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    d = load_mandate_dict(args.mandate_id)

    m = Mandate(**d)

    try:
        server_ok = bool(m.verify_server())

    except Exception:
        server_ok = False

    try:
        client_ok = bool(m.verify_client())

    except Exception:
        client_ok = False

    try:
        all_ok = bool(m.verify_all())

    except Exception:
        all_ok = False

    report = {
        "mandateId": d.get("mandateId"),
        "verifyServer": server_ok,
        "verifyClient": client_ok,
        "verifyAll": all_ok,
        "hasServerSig": "serverSig" in (d.get("signatures") or {}),
        "hasClientSig": "clientSig" in (d.get("signatures") or {}),
    }

    _print_json(report)

    return 0 if all_ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wachai", description="WachAI Mandates CLI (create, sign, verify)")

    sub = p.add_subparsers(dest="cmd", required=True)

    create = sub.add_parser("create-mandate", help="Create a mandate and sign it as server (offer)")

    mode = create.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--swap",
        nargs=4,
        metavar=("FROM_ADDRESS", "TO_ADDRESS", "AMOUNT_IN", "AMOUNT_OUT"),
        help="Create a swap@1 mandate core (tokenIn tokenOut amountIn minOut)",
    )

    mode.add_argument(
        "--custom",
        metavar="KIND",
        help="Create a custom core (no remote primitive build). Requires --body.",
    )

    create.add_argument(
        "--body",
        help='Inline JSON object for custom core payload (e.g. \'{"field":"value"}\')',
    )

    create.add_argument("--chain-id", default=1, type=int, help="EVM chain id (default: 1)")

    create.add_argument(
        "--client",
        help="Client address (0x..) or CAIP-10 (eip155:chainId:0x..). Defaults to server address for demos.",
    )

    create.add_argument(
        "--server",
        help="Server address (0x..) or CAIP-10. Defaults to WACHAI_PRIVATE_KEY address.",
    )

    create.add_argument("--recipient", help="Swap recipient 0x address. Defaults to the client address.")

    create.add_argument("--deadline", help="Mandate deadline (ISO-8601, e.g. 2025-12-31T00:10:00Z)")

    create.add_argument(
        "--swap-deadline",
        help="Swap payload deadline (ISO-8601, e.g. 2025-12-31T00:00:00Z)",
    )

    create.add_argument("--intent", help="Human-readable intent string")

    create.add_argument(
        "--primitives-base-url",
        help="Override primitives registry base URL used by mandates_core.build_core",
    )

    create.add_argument("--no-store", action="store_true", help="Do not save mandate to local store")

    create.add_argument("--print-path", action="store_true", help="Print save path to stderr")

    create.set_defaults(func=cmd_create_mandate)

    sign = sub.add_parser("sign", help="Sign an existing mandate as client (accept)")

    sign.add_argument("mandate_id", help="Mandate id (mandateId)")

    sign.set_defaults(func=cmd_sign)

    verify = sub.add_parser("verify", help="Verify an existing mandate's signatures")

    verify.add_argument("mandate_id", help="Mandate id (mandateId)")

    verify.set_defaults(func=cmd_verify)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()

    args = parser.parse_args(argv)

    try:
        return int(args.func(args))

    except SystemExit:
        raise

    except Exception as e:
        _eprint(f"Error: {e}")

        return 1


if __name__ == "__main__":
    raise SystemExit(main())

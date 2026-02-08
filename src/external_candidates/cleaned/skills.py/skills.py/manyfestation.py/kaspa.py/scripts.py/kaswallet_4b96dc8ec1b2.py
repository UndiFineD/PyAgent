# Extracted from: C:\DEV\PyAgent\.external\skills\skills\manyfestation\kaspa\scripts\kaswallet.py
#!/usr/bin/env python3
import argparse
import asyncio
import os
import sys
import urllib.parse
from typing import Any, Optional


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def get_env(name: str) -> Optional[str]:
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def get_timeout_ms(name: str, default_ms: int) -> int:
    raw = get_env(name)
    if not raw:
        return default_ms
    try:
        ms = int(raw)
        return ms if ms > 0 else default_ms
    except ValueError:
        return default_ms


def payment_uri(address: str, amount: Optional[str], message: Optional[str], label: Optional[str]) -> str:
    params = {}
    if amount is not None:
        params["amount"] = amount
    if message is not None:
        params["message"] = message
    if label is not None:
        params["label"] = label
    if not params:
        return address
    return f"{address}?{urllib.parse.urlencode(params)}"


async def maybe_await(result: Any) -> Any:
    if asyncio.iscoroutine(result):
        return await result
    return result


def first_attr(obj: Any, names: list[str]) -> Optional[Any]:
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    return None


async def call_first(obj: Any, names: list[str], *args: Any, **kwargs: Any) -> Any:
    fn = first_attr(obj, names)
    if fn is None:
        raise RuntimeError(f"None of methods exist: {', '.join(names)}")
    return await maybe_await(fn(*args, **kwargs))


def load_kaspa_module():
    try:
        import kaspa  # type: ignore

        return kaspa
    except Exception as exc:
        raise RuntimeError("Python package 'kaspa' is not installed. Run: bash install.sh") from exc


async def build_rpc_client(kaspa_mod: Any, network: str, rpc_url: Optional[str]) -> Any:
    # Try a few constructor styles to be resilient across versions.
    RpcClient = getattr(kaspa_mod, "RpcClient", None)
    Resolver = getattr(kaspa_mod, "Resolver", None)
    Encoding = getattr(kaspa_mod, "Encoding", None)

    if RpcClient is None:
        raise RuntimeError("kaspa.RpcClient not found in installed 'kaspa' package")

    encoding = None
    if Encoding is not None:
        encoding = getattr(Encoding, "Borsh", None) or getattr(Encoding, "borsh", None)

    # Prefer resolver when no URL is provided.
    if rpc_url is None and Resolver is not None:
        try:
            resolver = Resolver()
            try:
                client = RpcClient(
                    {"resolver": resolver, "networkId": network, "encoding": encoding}
                    if encoding
                    else {"resolver": resolver, "networkId": network}
                )
            except Exception:
                client = RpcClient(resolver)
            return client
        except Exception:
            pass

    # Direct URL fallback.
    if rpc_url is None:
        raise RuntimeError("No KASPA_RPC_URL set and resolver mode unavailable/failed")

    try:
        client = RpcClient(
            {"url": rpc_url, "networkId": network, "encoding": encoding}
            if encoding
            else {"url": rpc_url, "networkId": network}
        )
        return client
    except Exception:
        pass

    try:
        client = RpcClient(rpc_url)
        return client
    except Exception as exc:
        raise RuntimeError(f"Failed to create RpcClient for rpc_url={rpc_url}") from exc


async def rpc_connect(client: Any, connect_timeout_ms: int) -> None:
    if hasattr(client, "connect"):
        await asyncio.wait_for(maybe_await(client.connect()), timeout=connect_timeout_ms / 1000.0)


async def rpc_disconnect(client: Any) -> None:
    if hasattr(client, "disconnect"):
        try:
            await maybe_await(client.disconnect())
        except Exception:
            pass


async def cmd_node_info(args: argparse.Namespace) -> int:
    kaspa_mod = load_kaspa_module()
    network = args.network
    rpc_url = args.rpc
    connect_timeout_ms = args.connect_timeout_ms

    client = await build_rpc_client(kaspa_mod, network, rpc_url)
    await rpc_connect(client, connect_timeout_ms)

    try:
        info = await call_first(client, ["get_server_info", "getServerInfo"])
        print(info)
        return 0
    finally:
        await rpc_disconnect(client)


async def cmd_balance(args: argparse.Namespace) -> int:
    kaspa_mod = load_kaspa_module()
    network = args.network
    rpc_url = args.rpc
    connect_timeout_ms = args.connect_timeout_ms
    request_timeout_ms = args.request_timeout_ms

    client = await build_rpc_client(kaspa_mod, network, rpc_url)
    await rpc_connect(client, connect_timeout_ms)

    try:
        # Prefer get_balance_by_address, but be flexible across versions.
        fn_names = [
            "get_balance_by_address",
            "getBalanceByAddress",
            "get_balance",
            "getBalance",
        ]

        async def do_call():
            # Some variants accept dict, some accept positional.
            try:
                return await call_first(client, fn_names, {"address": args.address})
            except Exception:
                return await call_first(client, fn_names, args.address)

        result = await asyncio.wait_for(do_call(), timeout=request_timeout_ms / 1000.0)
        print(result)
        return 0
    finally:
        await rpc_disconnect(client)


async def cmd_send(args: argparse.Namespace) -> int:
    # Best-effort implementation: APIs differ across versions.
    # We keep strong safety: require --yes for broadcast.
    if not args.dry_run and not args.yes:
        eprint("Refusing to send without explicit confirmation. Re-run with --yes or use --dry-run.")
        return 2

    kaspa_mod = load_kaspa_module()
    network = args.network
    rpc_url = args.rpc
    connect_timeout_ms = args.connect_timeout_ms
    request_timeout_ms = args.request_timeout_ms

    mnemonic = get_env("KASPA_MNEMONIC")
    private_key = get_env("KASPA_PRIVATE_KEY")
    if args.from_mnemonic_env and not mnemonic:
        eprint("KASPA_MNEMONIC is not set.")
        return 2
    if args.from_private_key_env and not private_key:
        eprint("KASPA_PRIVATE_KEY is not set.")
        return 2
    if args.from_mnemonic_env and args.from_private_key_env:
        eprint("Choose only one: --from-mnemonic-env or --from-private-key-env")
        return 2
    if not args.from_mnemonic_env and not args.from_private_key_env:
        eprint("Sender is required: use --from-mnemonic-env or --from-private-key-env (secrets via env).")
        return 2

    client = await build_rpc_client(kaspa_mod, network, rpc_url)
    await rpc_connect(client, connect_timeout_ms)

    try:
        # For now, we only support versions of the SDK that expose a convenience 'send' method.
        # If not present, we fail with a clear message.
        send_fn = first_attr(client, ["send", "send_transaction", "sendTransaction"])
        if send_fn is None:
            raise RuntimeError(
                "Installed 'kaspa' SDK does not expose a simple send API. "
                "Try upgrading: pip install -U kaspa, or use the MCP backend mode."
            )

        payload = {
            "to": args.to,
            "amount": args.amount,
            "network": network,
        }
        if args.custom_fee is not None:
            payload["customFee"] = args.custom_fee

        if args.from_mnemonic_env:
            payload["mnemonic"] = mnemonic  # DO NOT PRINT
        else:
            payload["privateKey"] = private_key  # DO NOT PRINT

        if args.dry_run:
            print(
                f"DRY RUN:\n"
                f"  network: {network}\n"
                f"  rpc: {rpc_url or '(resolver)'}\n"
                f"  to: {args.to}\n"
                f"  amount: {args.amount}\n"
                f"  customFee: {args.custom_fee or '(auto)'}\n"
            )
            return 0

        async def do_send():
            return await maybe_await(send_fn(payload))

        result = await asyncio.wait_for(do_send(), timeout=request_timeout_ms / 1000.0)
        print(result)
        return 0
    finally:
        await rpc_disconnect(client)


def main() -> int:
    parser = argparse.ArgumentParser(prog="kaswallet.sh", add_help=True)

    parser.add_argument("--network", default=get_env("KASPA_NETWORK") or "mainnet")
    parser.add_argument("--rpc", default=get_env("KASPA_RPC_URL"))
    parser.add_argument(
        "--connect-timeout-ms",
        type=int,
        default=get_timeout_ms("KASPA_CONNECT_TIMEOUT_MS", 60000),
    )
    parser.add_argument(
        "--request-timeout-ms",
        type=int,
        default=get_timeout_ms("KASPA_REQUEST_TIMEOUT_MS", 60000),
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_info = sub.add_parser("node-info", help="Print node/server info")
    p_info.set_defaults(func=cmd_node_info)

    p_bal = sub.add_parser("balance", help="Get balance for an address")
    p_bal.add_argument("--address", required=True)
    p_bal.set_defaults(func=cmd_balance)

    p_uri = sub.add_parser("payment-uri", help="Generate a Kaspa payment request URI")
    p_uri.add_argument("--address", required=True)
    p_uri.add_argument("--amount")
    p_uri.add_argument("--message")
    p_uri.add_argument("--label")

    p_send = sub.add_parser("send", help="Send KAS (requires env secrets)")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--amount", required=True)
    p_send.add_argument("--custom-fee", dest="custom_fee")
    p_send.add_argument("--from-mnemonic-env", action="store_true")
    p_send.add_argument("--from-private-key-env", action="store_true")
    p_send.add_argument("--dry-run", action="store_true")
    p_send.add_argument("--yes", action="store_true")
    p_send.set_defaults(func=cmd_send)

    args = parser.parse_args()

    if args.cmd == "payment-uri":
        print(payment_uri(args.address, args.amount, args.message, args.label))
        return 0

    try:
        return asyncio.run(args.func(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        eprint(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

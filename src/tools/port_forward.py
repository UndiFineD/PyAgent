#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Port forwarding helpers for firewall configuration."""

from __future__ import annotations

import argparse
import asyncio
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


async def _handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    remote_host: str,
    remote_port: int,
) -> None:
    """Handle a client connection and forward data to the remote host."""
    remote_reader, remote_writer = await asyncio.open_connection(remote_host, remote_port)

    async def _pipe(src: asyncio.StreamReader, dst: asyncio.StreamWriter) -> None:
        """Pipe data from src to dst."""
        try:
            while not src.at_eof():
                data = await src.read(4096)
                if not data:
                    break
                dst.write(data)
                await dst.drain()
        except Exception:
            pass
        finally:
            dst.close()

    await asyncio.gather(
        _pipe(reader, remote_writer),
        _pipe(remote_reader, writer),
        return_exceptions=True,
    )


async def main(args: list[str] | None = None) -> int:
    """Main entry point for the port_forward tool."""
    parser = argparse.ArgumentParser(prog="port_forward")
    parser.add_argument("--listen-port", type=int, required=True, help="Local port to listen on")
    parser.add_argument("--target-host", required=True, help="Remote host to forward to")
    parser.add_argument("--target-port", type=int, required=True, help="Remote port to forward to")
    parser.add_argument("--duration", type=int, default=60, help="Duration (s) to keep the forwarder running")

    parsed = parser.parse_args(args=args)

    server = await asyncio.start_server(
        lambda r, w: _handle_client(r, w, parsed.target_host, parsed.target_port),
        host="127.0.0.1",
        port=parsed.listen_port,
    )
    print(f"Forwarding 127.0.0.1:{parsed.listen_port} -> {parsed.target_host}:{parsed.target_port}")

    async with server:
        await asyncio.wait_for(server.serve_forever(), timeout=parsed.duration)

    return 0


register_tool(
    "port_forward",
    main,
    "Simple TCP port forwarder (async)",
)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

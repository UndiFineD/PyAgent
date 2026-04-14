import asyncio

import httpx
import pytest

from runtime_py import run_http_server


@pytest.mark.asyncio
async def test_http_server() -> None:
    """Test that the HTTP server can handle a simple request."""
    # Python handler returns (status, body)

    async def handler(uri: str) -> tuple[int, str]:
        """Example handler that ignores the URI and returns a fixed response."""
        return 200, "hello"

    # bind to a known port so the test can connect
    port = 8001
    addr = f"127.0.0.1:{port}"
    run_http_server(addr, handler)

    # give the runtime a moment to start the service
    await asyncio.sleep(0.05)

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://127.0.0.1:{port}/")
        assert resp.status_code == 200
        assert resp.text == "hello"

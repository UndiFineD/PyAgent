import os
import subprocess
import sys
from pathlib import Path


def test_spawn_simple() -> None:
    """Test that spawn_task can run a simple async function."""
    # execute the async routine in a fresh Python subprocess to isolate runtime
    script = r"""
import asyncio
import runtime

async def inner():
    event = asyncio.Event()

    async def worker():
        event.set()

    runtime.spawn_task(worker())
    await asyncio.wait_for(event.wait(), timeout=1.0)

asyncio.run(inner())
# after event set, shut down runtime before exiting
runtime._shutdown_runtime()
"""
    env = dict(os.environ)
    src_dir = str((Path(__file__).resolve().parents[2] / "src"))
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_dir if not existing else f"{src_dir}{os.pathsep}{existing}"
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, env=env)
    # subprocess should exit normally; crash will result in nonzero exit code
    assert result.returncode == 0, f"Spawn task script failed: {result.stderr.decode()}"

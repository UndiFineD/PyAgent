# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\asynctasks\examples\hello_word_job.py
"""
Hello World task

Provides a simple Hello World task
"""

from typing import Any

from core.asynctasks.task_manager import task


@task()
async def hello_world(data: Any) -> Any:
    return f"hello world: {data}"

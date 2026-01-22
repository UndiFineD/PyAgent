"""
Manager for parallel execution.
(Facade for src.core.base.common.execution_core)
"""

from src.core.base.common.execution_core import ExecutionCore as ParallelProcessor

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers

    def process_files_threaded(
        self, files: list[Path], worker_func: Callable[[Path], Any]
    ) -> list[Any]:
        """Process files using worker threads."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if HAS_TQDM:
                results = list(
                    tqdm(
                        executor.map(worker_func, files),
                        total=len(files),
                        desc="Processing (Threads)",
                    )
                )
            else:
                results = list(executor.map(worker_func, files))
        return [r for r in results if r is not None]

    async def async_process_files(
        self, files: list[Path], worker_func: Callable[[Path], Any]
    ) -> list[Any]:
        """Process multiple files concurrently using async/await."""
        modified_results: list[Any] = []
        loop = asyncio.get_running_loop()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:

            async def wrap_worker(file_path: Path) -> None:
                try:
                    res = await loop.run_in_executor(executor, worker_func, file_path)
                    if res:
                        modified_results.append(res)
                except Exception as e:
                    logging.error(f"[async] Failed to process {file_path.name}: {e}")

            tasks = [wrap_worker(f) for f in files]
            if tasks:
                await asyncio.gather(*tasks)

        return modified_results

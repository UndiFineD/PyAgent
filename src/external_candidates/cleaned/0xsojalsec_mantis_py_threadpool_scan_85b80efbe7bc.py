# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_mantis.py\mantis.py\scan_orchestration.py\threadpool_scan_85b80efbe7bc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\scan_orchestration\threadpool_scan.py

import asyncio

import logging

import time

from datetime import timedelta

from mantis.models.tool_logs_model import AssetLogs

from mantis.utils.common_utils import CommonUtils


class ExecuteScanThreadPool:
    async def execute_and_store(self, tool_tuple):

        tool_start_time = time.perf_counter()

        scanner = tool_tuple[0]

        logging.debug(f"Executing command for {type(scanner).__name__}")

        results = await scanner.execute(tool_tuple)

        if results == None:
            logging.warning(
                f"No scan efficiency matrix returned, scan efficiency for {type(scanner).__name__} will be hampered"
            )

        else:
            results["tool_name"] = type(scanner).__name__

            tool_end_time = time.perf_counter()

            tool_time_taken = str(timedelta(seconds=round(tool_end_time - tool_start_time, 0)))

            results["tool_time_taken"] = tool_time_taken

            asset_log = AssetLogs(**results)

        return asset_log

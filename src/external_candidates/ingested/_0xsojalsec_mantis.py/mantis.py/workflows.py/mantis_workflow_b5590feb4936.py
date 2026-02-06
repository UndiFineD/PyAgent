# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mantis\mantis\workflows\mantis_workflow.py
import asyncio

from mantis.models.args_model import ArgsModel
from mantis.modules.workflow import Workflow


class MantisWorkflow:
    @staticmethod
    def select_workflow(args: ArgsModel) -> None:

        asyncio.run(Workflow.workflow_executor(args))

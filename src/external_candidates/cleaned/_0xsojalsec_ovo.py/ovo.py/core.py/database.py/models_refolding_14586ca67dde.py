# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\database\models_refolding.py
from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from ovo.core.database import DescriptorJob
from ovo.core.database.descriptors_refolding import REFOLDING_TESTS_BY_TYPE
from ovo.core.database.models import Base, DescriptorWorkflow, WorkflowTypes


class RefoldingSupportedDesignWorkflow(ABC):
    """Abstract class that defines an interface for workflows supported by the RefoldingWorkflow workflow"""

    def get_refolding_native_pdb_path(self, contig_index: int) -> Optional[str]:
        raise NotImplementedError()

    def get_refolding_design_paths(self, design_ids: list[str]) -> dict[str, str]:
        raise NotImplementedError()

    def get_refolding_design_type(self) -> str:
        raise NotImplementedError()


@WorkflowTypes.register("Refolding workflow")
@dataclass
class RefoldingWorkflow(DescriptorWorkflow):
    chains: List[str] = field(default_factory=lambda: ["FULL"])
    tests: List[str] = None
    design_type: str = None
    native_pdb_path: str = None

    def get_pipeline_name(self) -> str:
        return "ovo.refolding"

    def prepare_params(self, workdir: str) -> dict:
        from ovo.core.logic.descriptor_logic import prepare_refolding_params

        return prepare_refolding_params(self, workdir=workdir)

    def process_results(self, job: DescriptorJob, callback: Callable = None) -> list[Base]:
        from ovo.core.logic.descriptor_logic import read_descriptor_file_values

        descriptor_values = read_descriptor_file_values(
            descriptor_job=job,
            # descriptor key prefix (pipeline|tool_key) -> filename to parse
            filenames={f"refolding|{test}": test for test in self.tests},
            # mapping from design.id to ID column in produced file
            design_id_mapping={design_id: design_id for design_id in self.design_ids},
        )
        return descriptor_values + [job]

    def validate(self):
        super().validate()
        if not self.design_type:
            raise ValueError("Design type not specified")
        if not self.tests:
            raise ValueError("No tests specified")
        for test in self.tests:
            # TODO validate test name
            assert test in REFOLDING_TESTS_BY_TYPE[self.design_type], (
                f"Invalid test for design type {self.design_type}: {test}"
            )

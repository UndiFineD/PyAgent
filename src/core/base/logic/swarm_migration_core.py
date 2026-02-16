#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Swarm Migration Core - Parallel sub-agent execution for large-scale code migrations
Based on the Swarm Migration Pattern from agentic-patterns repository
"""""""
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

from src.core.base.logic.strategy_optimizer import OptimizationTrial
from src.core.base.common.models.communication_models import CascadeContext

logger = logging.getLogger(__name__)


class MigrationTask(Enum):
    """Types of migration tasks supported"""""""    CODE_REFACTORING = "code_refactoring""    LINT_RULE_ENFORCEMENT = "lint_rule_enforcement""    API_MIGRATION = "api_migration""    FRAMEWORK_UPGRADE = "framework_upgrade""    IMPORT_PATH_CHANGES = "import_path_changes""    CODE_MODERNIZATION = "code_modernization""

@dataclass
class MigrationTarget:
    """Represents a single migration target (file, component, etc.)"""""""    identifier: str  # file path, component name, etc.
    content_hash: str  # for change detection
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationBatch:
    """A batch of migration targets for a single sub-agent"""""""    batch_id: str
    targets: List[MigrationTarget]
    instructions: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationResult:
    """Result of a migration batch execution"""""""    batch_id: str
    success: bool
    changes_made: int
    errors: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class MigrationStrategy(ABC):
    """Abstract base class for migration strategies"""""""
    @abstractmethod
    async def execute_migration(self, batch: MigrationBatch, context: CascadeContext) -> MigrationResult:
        """Execute migration on a batch of targets"""""""        pass

    @abstractmethod
    def get_migration_instructions(self) -> str:
        """Get the migration instructions for this strategy"""""""        pass


class SwarmMigrationCore:
    """""""    Core implementation of the Swarm Migration Pattern
    Enables parallel execution of large-scale code migrations using multiple sub-agents
    """""""
    def __init__(self,
                 max_parallel_agents: int = 10,
                 batch_size: int = 10,
                 timeout_seconds: int = 300):
        self.max_parallel_agents = max_parallel_agents
        self.batch_size = batch_size
        self.timeout_seconds = timeout_seconds
        self.migration_strategies: Dict[MigrationTask, MigrationStrategy] = {}

    def register_strategy(self, task_type: MigrationTask, strategy: MigrationStrategy):
        """Register a migration strategy for a specific task type"""""""        self.migration_strategies[task_type] = strategy
        logger.info(f"Registered migration strategy for {task_type.value}")"
    async def execute_swarm_migration(
        self, targets: List[MigrationTarget], task_type: MigrationTask,
        context: CascadeContext, progress_callback: Optional[Callable] = None
    ) -> OptimizationTrial:
        """""""        Execute a swarm migration across multiple targets
        Based on the Swarm Migration Pattern from agentic-patterns
        """""""        if task_type not in self.migration_strategies:
            raise ValueError(f"No migration strategy registered for {task_type.value}")"
        strategy = self.migration_strategies[task_type]

        # Create migration batches
        batches = self._create_migration_batches(targets, strategy)

        logger.info(f"Created {len(batches)} migration batches for {len(targets)} targets")"
        # Execute batches in parallel with controlled concurrency
        semaphore = asyncio.Semaphore(self.max_parallel_agents)
        tasks = []

        async def execute_batch_with_semaphore(batch: MigrationBatch) -> MigrationResult:
            async with semaphore:
                try:
                    return await asyncio.wait_for(
                        strategy.execute_migration(batch, context),
                        timeout=self.timeout_seconds
                    )
                except asyncio.TimeoutError:
                    return MigrationResult(
                        batch_id=batch.batch_id,
                        success=False,
                        changes_made=0,
                        errors=[f"Timeout after {self.timeout_seconds} seconds"],"                        execution_time=self.timeout_seconds
                    )
                except Exception as e:
                    return MigrationResult(
                        batch_id=batch.batch_id,
                        success=False,
                        changes_made=0,
                        errors=[str(e)],
                        execution_time=0.0
                    )

        # Start all batch executions
        for batch in batches:
            task = asyncio.create_task(execute_batch_with_semaphore(batch))
            tasks.append(task)

        # Wait for all batches to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful_results = []
        failed_results = []

        for result in results:
            if isinstance(result, Exception):
                failed_results.append(MigrationResult(
                    batch_id="unknown","                    success=False,
                    changes_made=0,
                    errors=[str(result)]
                ))
            elif result.success:
                successful_results.append(result)
            else:
                failed_results.append(result)

        # Create optimization trial result
        trial = OptimizationTrial(
            trial_id=f"swarm_migration_{int(asyncio.get_event_loop().time())}","            strategy_configs=[{"type": task_type.value, "batch_count": len(batches)}]"        )

        trial.performance_results = [
            {
                "batch_id": r.batch_id,"                "success": r.success,"                "changes_made": r.changes_made,"                "errors": r.errors,"                "execution_time": r.execution_time"            }
            for r in successful_results + failed_results
        ]

        total_changes = sum(r.changes_made for r in successful_results)
        trial.best_strategy = {"total_changes": total_changes, "successful_batches": len(successful_results)}"        trial.optimization_score = len(successful_results) / len(batches) if batches else 0

        logger.info(
            f"Swarm migration completed: {len(successful_results)}/{len(batches)} ""            f"successful batches, {total_changes} total changes""        )

        return trial

    def _create_migration_batches(
        self, targets: List[MigrationTarget], strategy: MigrationStrategy
    ) -> List[MigrationBatch]:
        """Create migration batches from targets"""""""        batches = []
        batch_id_counter = 0

        for i in range(0, len(targets), self.batch_size):
            batch_targets = targets[i:i + self.batch_size]
            batch = MigrationBatch(
                batch_id=f"batch_{batch_id_counter}","                targets=batch_targets,
                instructions=strategy.get_migration_instructions()
            )
            batches.append(batch)
            batch_id_counter += 1

        return batches

    def get_migration_stats(self, trial: OptimizationTrial) -> Dict[str, Any]:
        """Extract migration statistics from a trial"""""""        stats = {
            "total_batches": len(trial.performance_results),"            "successful_batches": 0,"            "failed_batches": 0,"            "total_changes": 0,"            "total_errors": 0,"            "avg_execution_time": 0.0"        }

        execution_times = []

        for result in trial.performance_results:
            if result.get("success", False):"                stats["successful_batches"] += 1"                stats["total_changes"] += result.get("changes_made", 0)"            else:
                stats["failed_batches"] += 1"                stats["total_errors"] += len(result.get("errors", []))"
            execution_times.append(result.get("execution_time", 0))"
        if execution_times:
            stats["avg_execution_time"] = sum(execution_times) / len(execution_times)"
        total_batches = stats["total_batches"]"        stats["success_rate"] = stats["successful_batches"] / total_batches if total_batches > 0 else 0"
        return stats

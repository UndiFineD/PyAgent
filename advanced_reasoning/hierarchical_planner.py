"""Hierarchical Task Planner

Decomposes complex goals into subtasks, manages dependencies, and generates
execution plans. Perfect for project planning, workflow design, and goal decomposition.

Features:
  - Hierarchical goal decomposition
  - Dependency management
  - Resource scheduling
  - Risk assessment
  - Gantt chart generation
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class TaskPriority(Enum):
    """Task priority levels"""

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Task execution status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class Task:
    """A task in the plan"""

    task_id: str
    name: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration_hours: float = 1.0
    dependencies: List[str] = field(default_factory=list)  # Task IDs
    resources_required: Dict[str, int] = field(default_factory=dict)  # resource -> count
    subtasks: List['Task'] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    risk_level: str = "low"  # low, medium, high
    owner: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def total_duration(self) -> float:
        """Total duration including subtasks"""
        if self.subtasks:
            return sum(t.total_duration for t in self.subtasks)
        return self.estimated_duration_hours

    @property
    def is_complete(self) -> bool:
        """Is task complete?"""
        if self.subtasks:
            return all(t.is_complete for t in self.subtasks)
        return self.status == TaskStatus.COMPLETED

    @property
    def all_dependencies_met(self) -> bool:
        """Are all dependencies satisfied?"""
        return len(self.dependencies) == 0


@dataclass
class ExecutionPlan:
    """Complete execution plan"""

    goal: str
    root_task: Task
    all_tasks: List[Task]
    critical_path: List[Task]
    total_duration_hours: float
    parallelizable_groups: List[List[Task]]
    resource_requirements: Dict[str, int]
    risk_assessment: Dict[str, str]

    def gantt_chart(self) -> str:
        """Generate ASCII Gantt chart"""
        chart = "Gantt Chart\n"
        chart += "═" * 60 + "\n"

        # Sort by start time
        sorted_tasks = sorted(
            self.all_tasks,
            key=lambda t: t.start_time or datetime.now()
        )

        for task in sorted_tasks:
            if task.start_time and task.end_time:
                duration = (task.end_time - task.start_time).total_seconds() / 3600
                bar_length = int(duration / 4)  # Scale
                chart += f"{task.name[:20]:<20} "
                chart += "█" * bar_length + "\n"

        return chart

    def critical_path_summary(self) -> str:
        """Get critical path summary"""
        path_str = " → ".join(t.name for t in self.critical_path)
        return f"Critical Path ({len(self.critical_path)} tasks):\n  {path_str}"


class HierarchicalPlanner:
    """Plans complex goals hierarchically"""

    def __init__(self, model=None):
        """Initialize planner.
        
        Args:
            model: LLM for decomposition (optional)

        """
        self.model = model
        self.planning_history: List[Tuple[str, ExecutionPlan]] = []

    def plan_goal(
        self,
        goal: str,
        context: Optional[str] = None,
        max_depth: int = 4
    ) -> ExecutionPlan:
        """Plan a complex goal.
        
        Args:
            goal: The goal to achieve
            context: Background context
            max_depth: Max decomposition depth
        
        Returns:
            ExecutionPlan with all tasks and schedule

        """
        # Create root task
        root = Task(
            task_id="root",
            name=goal,
            description=goal,
            priority=TaskPriority.HIGH
        )

        # Decompose recursively
        self._decompose_task(root, depth=0, max_depth=max_depth)

        # Flatten to get all tasks
        all_tasks = self._flatten_tasks(root)

        # Calculate dependencies and ordering
        self._establish_dependencies(all_tasks)

        # Find critical path
        critical_path = self._find_critical_path(all_tasks)

        # Calculate schedule
        self._schedule_tasks(root, all_tasks)

        # Group parallelizable tasks
        parallel_groups = self._find_parallel_groups(all_tasks)

        # Calculate resource requirements
        resources = self._calculate_resources(all_tasks)

        # Risk assessment
        risks = self._assess_risks(all_tasks)

        # Total duration
        total_duration = root.total_duration

        plan = ExecutionPlan(
            goal=goal,
            root_task=root,
            all_tasks=all_tasks,
            critical_path=critical_path,
            total_duration_hours=total_duration,
            parallelizable_groups=parallel_groups,
            resource_requirements=resources,
            risk_assessment=risks
        )

        self.planning_history.append((goal, plan))
        return plan

    def _decompose_task(self, task: Task, depth: int, max_depth: int):
        """Decompose a task into subtasks"""
        if depth >= max_depth:
            return

        # Generate subtasks (would use LLM in real implementation)
        subtasks = self._generate_subtasks(task, depth)

        task.subtasks = subtasks

        # Recursively decompose
        for subtask in subtasks:
            self._decompose_task(subtask, depth + 1, max_depth)

    def _generate_subtasks(self, task: Task, depth: int) -> List[Task]:
        """Generate subtasks for a task"""
        # Heuristic-based decomposition
        subtasks = []

        # Generic breakdown pattern
        patterns = {
            0: ["Planning", "Analysis", "Design"],
            1: ["Implementation", "Testing", "Integration"],
            2: ["Verification", "Documentation", "Deployment"],
        }

        if depth in patterns:
            for i, name in enumerate(patterns[depth]):
                subtask = Task(
                    task_id=f"{task.task_id}_{i}",
                    name=f"{name}: {task.name}",
                    description=f"{name} phase of {task.name}",
                    estimated_duration_hours=task.estimated_duration_hours / len(patterns[depth]),
                    priority=task.priority,
                    risk_level=task.risk_level
                )
                subtasks.append(subtask)

        return subtasks

    def _flatten_tasks(self, task: Task, flattened: Optional[List[Task]] = None) -> List[Task]:
        """Flatten task hierarchy"""
        if flattened is None:
            flattened = []

        flattened.append(task)

        for subtask in task.subtasks:
            self._flatten_tasks(subtask, flattened)

        return flattened

    def _establish_dependencies(self, tasks: List[Task]):
        """Establish task dependencies"""
        # Simple heuristic: each task depends on previous at same level
        # (Real implementation would be more sophisticated)
        for i, task in enumerate(tasks):
            if i > 0:
                # Depend on previous task at same priority level
                prev_task = tasks[i - 1]
                if prev_task.priority == task.priority:
                    task.dependencies.append(prev_task.task_id)

    def _find_critical_path(self, tasks: List[Task]) -> List[Task]:
        """Find critical path through task graph"""
        # Tasks with no parallelism opportunity form critical path
        critical = []

        for task in tasks:
            if not task.dependencies or len(task.dependencies) > 1:
                critical.append(task)

        return sorted(critical, key=lambda t: t.estimated_duration_hours, reverse=True)

    def _schedule_tasks(self, root: Task, tasks: List[Task]):
        """Schedule tasks with start and end times"""
        current_time = datetime.now()

        # Schedule root
        root.start_time = current_time
        root.end_time = current_time + timedelta(hours=root.total_duration)

        # Schedule children sequentially (simple heuristic)
        for task in root.subtasks:
            task.start_time = current_time
            duration = task.total_duration
            task.end_time = current_time + timedelta(hours=duration)
            current_time += timedelta(hours=duration)

    def _find_parallel_groups(self, tasks: List[Task]) -> List[List[Task]]:
        """Find groups of tasks that can run in parallel"""
        groups = []
        used = set()

        for task in tasks:
            if task.task_id in used:
                continue

            # Find tasks that can run in parallel with this one
            parallel_group = [task]
            used.add(task.task_id)

            for other in tasks:
                if (other.task_id not in used and
                    not other.dependencies and
                    len(parallel_group) < 3):  # Limit group size
                    parallel_group.append(other)
                    used.add(other.task_id)

            if len(parallel_group) > 0:
                groups.append(parallel_group)

        return groups

    def _calculate_resources(self, tasks: List[Task]) -> Dict[str, int]:
        """Calculate total resource requirements"""
        resources: Dict[str, int] = {}

        for task in tasks:
            for resource, count in task.resources_required.items():
                resources[resource] = resources.get(resource, 0) + count

        return resources

    def _assess_risks(self, tasks: List[Task]) -> Dict[str, str]:
        """Assess risks for the plan"""
        risks = {}

        high_risk_count = sum(1 for t in tasks if t.risk_level == "high")
        medium_risk_count = sum(1 for t in tasks if t.risk_level == "medium")

        if high_risk_count > 0:
            risks['critical_risks'] = f"{high_risk_count} high-risk tasks"

        if medium_risk_count > 2:
            risks['moderate_risks'] = f"{medium_risk_count} medium-risk tasks"

        # Dependency risk
        max_deps = max(len(t.dependencies) for t in tasks) if tasks else 0
        if max_deps > 3:
            risks['dependency_complexity'] = f"Up to {max_deps} task dependencies"

        return risks


class ProjectScheduler:
    """Schedule projects with resource constraints"""

    def __init__(self):
        """Initialize scheduler"""
        self.tasks: List[Task] = []
        self.resource_availability: Dict[str, int] = {}

    def add_task(self, task: Task):
        """Add task to schedule"""
        self.tasks.append(task)

    def set_resource_availability(self, resource: str, available: int):
        """Set available resources"""
        self.resource_availability[resource] = available

    def schedule(self) -> Dict:
        """Schedule tasks respecting resource constraints"""
        schedule = {}

        for task in self.tasks:
            # Check resource availability
            can_schedule = all(
                self.resource_availability.get(res, 0) >= count
                for res, count in task.resources_required.items()
            )

            if can_schedule:
                schedule[task.task_id] = {
                    'name': task.name,
                    'duration': task.estimated_duration_hours,
                    'status': 'scheduled'
                }

                # Allocate resources
                for res, count in task.resources_required.items():
                    self.resource_availability[res] -= count
            else:
                schedule[task.task_id] = {
                    'name': task.name,
                    'status': 'blocked_on_resources'
                }

        return schedule


class MilestoneTracker:
    """Track major milestones in plan"""

    def __init__(self):
        """Initialize tracker"""
        self.milestones: List[Dict] = []

    def add_milestone(self, name: str, target_date: datetime, tasks: List[Task]):
        """Add a milestone"""
        self.milestones.append({
            'name': name,
            'target_date': target_date,
            'tasks': tasks,
            'status': 'pending'
        })

    def update_progress(self, milestone_name: str, progress: float):
        """Update milestone progress (0-1)"""
        for milestone in self.milestones:
            if milestone['name'] == milestone_name:
                milestone['progress'] = progress
                milestone['status'] = 'in_progress' if 0 < progress < 1 else 'completed'

    def get_critical_milestones(self) -> List[Dict]:
        """Get milestones at risk"""
        now = datetime.now()
        at_risk = []

        for milestone in self.milestones:
            days_until = (milestone['target_date'] - now).days
            if 0 <= days_until <= 3:
                at_risk.append(milestone)

        return at_risk

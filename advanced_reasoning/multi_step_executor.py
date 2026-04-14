"""Multi-Step Reasoning Executor

Decomposes complex tasks into subtasks,
tracks dependencies, and executes in optimal order.
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class TaskStep:
    """A single step in task decomposition"""

    index: int
    description: str
    dependencies: Set[int]  # Which steps must complete first
    result: Optional[str] = None
    confidence: float = 0.5
    status: str = "pending"  # pending, executing, completed, failed


@dataclass
class ExecutionPlan:
    """Plan for executing a multi-step task"""

    task: str
    steps: List[TaskStep]
    dependency_graph: Dict[int, Set[int]]
    execution_order: List[List[int]]  # Batches that can run in parallel
    total_steps: int


class TaskDecomposer:
    """Break complex tasks into subtasks"""

    def __init__(self, model=None):
        """Initialize task decomposer"""
        self.model = model

    def decompose(self, task: str) -> List[str]:
        """Break task into subtasks
        
        Args:
            task: Complex task description
            
        Returns:
            List of subtask descriptions

        """
        # If model available, use it
        if self.model:
            return self._decompose_with_model(task)
        else:
            return self._decompose_heuristic(task)

    def _decompose_with_model(self, task: str) -> List[str]:
        """Decompose using LLM"""
        prompt = f"""Break this task into atomic steps that can be solved sequentially:

Task: {task}

List numbered steps, one per line. Each step should be solvable independently."""

        try:
            response = self.model.generate(prompt)
            steps = self._parse_steps(response)
            return steps
        except Exception:
            return self._decompose_heuristic(task)

    def _decompose_heuristic(self, task: str) -> List[str]:
        """Decompose using heuristics"""
        steps = []

        # Split by common keywords
        keywords = ['then', 'next', 'after', 'finally', 'also', ',']

        current_step = task
        for keyword in keywords:
            if keyword in current_step.lower():
                parts = re.split(f'(?i){keyword}', current_step)
                for part in parts:
                    part = part.strip()
                    if part:
                        steps.append(part)
                        current_step = ""
                break

        if current_step:
            steps.append(current_step)

        # If only one step found, try splitting by punctuation
        if len(steps) == 1:
            parts = [s.strip() for s in current_step.split('.') if s.strip()]
            if len(parts) > 1:
                steps = parts

        return steps if steps else [task]

    def _parse_steps(self, text: str) -> List[str]:
        """Extract steps from model output"""
        lines = text.strip().split('\n')
        steps = []

        for line in lines:
            line = line.strip()
            # Remove numbering
            line = re.sub(r'^\d+[\.\)]\s*', '', line)
            if line and any(c.isalpha() for c in line):
                steps.append(line)

        return steps


class DependencyAnalyzer:
    """Analyze dependencies between task steps"""

    @staticmethod
    def analyze(steps: List[str]) -> Dict[int, Set[int]]:
        """Determine which steps depend on which
        
        Args:
            steps: List of step descriptions
            
        Returns:
            Dict mapping step index to set of dependency indices

        """
        dependencies = {i: set() for i in range(len(steps))}

        for i, step in enumerate(steps):
            step_lower = step.lower()

            # Check for references to previous steps
            reference_words = ['previous', 'above', 'result of', 'from step', 'the', 'this']

            for ref_word in reference_words:
                if ref_word in step_lower:
                    # Likely depends on previous step
                    if i > 0:
                        dependencies[i].add(i - 1)
                    break

        return dependencies

    @staticmethod
    def validate_no_cycles(dependencies: Dict[int, Set[int]]) -> bool:
        """Check that dependency graph has no cycles"""
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in dependencies.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in dependencies:
            if node not in visited:
                if has_cycle(node):
                    return False

        return True

    @staticmethod
    def compute_execution_batches(dependencies: Dict[int, Set[int]]) -> List[List[int]]:
        """Compute batches of steps that can run in parallel
        
        Args:
            dependencies: Step dependencies
            
        Returns:
            List of batches; steps in same batch can run in parallel

        """
        batches = []
        completed = set()

        while len(completed) < len(dependencies):
            batch = []

            for step_id in dependencies:
                if step_id not in completed:
                    # Check if all dependencies are completed
                    deps = dependencies[step_id]
                    if all(d in completed for d in deps):
                        batch.append(step_id)

            if not batch:
                # No progress - likely circular dependency
                break

            batches.append(batch)
            completed.update(batch)

        return batches


class MultiStepExecutor:
    """Execute multi-step reasoning"""

    def __init__(self, model=None):
        """Initialize executor"""
        self.model = model
        self.decomposer = TaskDecomposer(model)
        self.analyzer = DependencyAnalyzer()

    def create_plan(self, task: str) -> ExecutionPlan:
        """Create execution plan for task
        
        Args:
            task: Complex task description
            
        Returns:
            ExecutionPlan with steps and order

        """
        # Decompose task
        step_descriptions = self.decomposer.decompose(task)

        # Analyze dependencies
        dependencies = self.analyzer.analyze(step_descriptions)

        # Validate no cycles
        if not self.analyzer.validate_no_cycles(dependencies):
            raise ValueError("Circular dependency detected in task decomposition")

        # Compute execution batches
        execution_batches = self.analyzer.compute_execution_batches(dependencies)

        # Create TaskStep objects
        steps = []
        for i, desc in enumerate(step_descriptions):
            step = TaskStep(
                index=i,
                description=desc,
                dependencies=dependencies[i]
            )
            steps.append(step)

        return ExecutionPlan(
            task=task,
            steps=steps,
            dependency_graph=dependencies,
            execution_order=execution_batches,
            total_steps=len(steps)
        )

    def execute(self, task: str) -> Dict:
        """Execute multi-step task
        
        Args:
            task: Complex task description
            
        Returns:
            Dict with steps, results, and final answer

        """
        # Create execution plan
        plan = self.create_plan(task)

        # Execute batches
        results = {}

        for batch_idx, batch in enumerate(plan.execution_order):
            for step_id in batch:
                step = plan.steps[step_id]

                # Build context from previous results
                context = self._build_context(plan.steps, results, task)

                # Execute step
                result = self._execute_step(step, context)
                results[step_id] = result
                step.result = result
                step.status = "completed"

        # Combine results into final answer
        final_answer = self._combine_results(plan.steps, results)

        return {
            'task': task,
            'plan': plan,
            'steps': [s.description for s in plan.steps],
            'results': [plan.steps[i].result for i in range(len(plan.steps))],
            'answer': final_answer,
            'num_steps': len(plan.steps),
            'execution_batches': plan.execution_order
        }

    def _execute_step(self, step: TaskStep, context: str) -> str:
        """Execute a single step"""
        if self.model is None:
            return f"[Execution of: {step.description}]"

        prompt = f"""{context}

Step {step.index + 1}: {step.description}

Answer:"""

        try:
            result = self.model.generate(prompt, max_tokens=150)
            return result.strip()
        except Exception as e:
            step.status = "failed"
            return f"Error: {str(e)}"

    def _build_context(self, steps: List[TaskStep], results: Dict,
                      original_task: str) -> str:
        """Build context from previous results"""
        context = f"Task: {original_task}\n\n"

        for step_id, result in sorted(results.items()):
            context += f"Step {step_id + 1} ({steps[step_id].description}):\n"
            context += f"{result}\n\n"

        return context

    def _combine_results(self, steps: List[TaskStep], results: Dict) -> str:
        """Combine step results into final answer"""
        if not results:
            return "No results"

        # Simple approach: return last step result
        last_step_id = max(results.keys())
        return results[last_step_id]


class ReasoningOptimizer:
    """Optimize multi-step reasoning execution"""

    @staticmethod
    def estimate_complexity(steps: List[str]) -> str:
        """Estimate task complexity"""
        num_steps = len(steps)

        if num_steps <= 2:
            return "simple"
        elif num_steps <= 5:
            return "moderate"
        else:
            return "complex"

    @staticmethod
    def should_use_parallel(execution_plan: ExecutionPlan) -> bool:
        """Decide if parallel execution is beneficial"""
        # Check if any batch has > 1 step
        for batch in execution_plan.execution_order:
            if len(batch) > 1:
                return True
        return False

    @staticmethod
    def should_cache_results(num_steps: int) -> bool:
        """Decide if result caching is beneficial"""
        return num_steps > 3


# Example usage
if __name__ == "__main__":
    task = "Calculate 15% of 200, then add 50 to get the final result"

    decomposer = TaskDecomposer()
    steps = decomposer.decompose(task)
    print("Decomposed steps:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

    # Analyze dependencies
    analyzer = DependencyAnalyzer()
    deps = analyzer.analyze(steps)
    print(f"\nDependencies: {deps}")

    # Create execution plan
    executor = MultiStepExecutor()
    plan = executor.create_plan(task)
    print(f"\nExecution batches: {plan.execution_order}")

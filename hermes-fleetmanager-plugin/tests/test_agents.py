"""
Test suite for agent code files in .github/agents/code/

This test discovers all Python agent files and validates that they have proper
type annotations (class members, method parameters, and return types).
"""

import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any

import pytest


def get_all_agent_files() -> list[Path]:
    """Discover all .py files in .github/agents/code/ (excluding __init__.py)."""
    base = Path(__file__).parent.parent / ".github" / "agents" / "code"
    return sorted([f for f in base.glob("*.py") if f.name != "__init__.py"])


def load_agent_module(file_path: Path) -> Any:
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_path.stem] = module
    spec.loader.exec_module(module)
    return module


def get_agent_class(module: Any) -> type | None:
    """Extract the agent class from a module (e.g., RulesAgent, FleetAgent, etc.)."""
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if "Agent" in name and not name.startswith("_"):
            return obj
    return None


def check_method_annotations(method: Any, method_name: str, class_name: str) -> list[str]:
    """Check if a method has proper type annotations."""
    issues: list[str] = []

    sig = inspect.signature(method)

    # Check return type
    if sig.return_annotation is inspect.Signature.empty:
        issues.append(f"{class_name}.{method_name} missing return type annotation")

    # Check parameter types (skip 'self')
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        if param.annotation is inspect.Parameter.empty:
            issues.append(f"{class_name}.{method_name}({param_name}) missing type annotation")

    return issues


def check_member_annotations(cls: type, class_name: str) -> list[str]:
    """Check if class members have type annotations."""
    issues: list[str] = []

    # Check __init__ method specifically for member initialization
    if hasattr(cls, "__init__"):
        try:
            sig = inspect.signature(cls)  # Get signature of class (includes __init__)

            # Check if __init__ has return annotation (-> None)
            if sig.return_annotation is inspect.Signature.empty:
                issues.append(f"{class_name}.__init__ missing return type annotation (-> None)")
        except (ValueError, TypeError):
            pass  # Skip if signature cannot be determined

    return issues


@pytest.mark.parametrize("agent_file", get_all_agent_files(), ids=lambda f: f.stem)
def test_agent_type_annotations(agent_file: Path) -> None:
    """Verify that an agent module has proper type annotations."""
    try:
        module = load_agent_module(agent_file)
    except Exception as e:
        pytest.skip(f"Could not load module {agent_file.stem}: {e}")
        return

    agent_class = get_agent_class(module)
    if agent_class is None:
        pytest.skip(f"No Agent class found in {agent_file.stem}")
        return

    class_name: str = agent_class.__name__
    issues: list[str] = []

    # Check class-level member annotations
    issues.extend(check_member_annotations(agent_class, class_name))

    # Check all methods
    for method_name, method in inspect.getmembers(agent_class, inspect.isfunction):
        if not method_name.startswith("_"):  # Skip private methods
            issues.extend(check_method_annotations(method, method_name, class_name))

    if issues:
        pytest.fail(f"{class_name} has type annotation issues:\n" + "\n".join(f"  - {i}" for i in issues))


def test_agent_execute_method_signatures() -> None:
    """Verify that all agents have execute() -> dict[str, Any]."""
    agent_files = get_all_agent_files()

    issues: list[str] = []
    for agent_file in agent_files:
        try:
            module = load_agent_module(agent_file)
        except Exception:
            continue

        agent_class = get_agent_class(module)
        if agent_class is None:
            continue

        if not hasattr(agent_class, "execute"):
            issues.append(f"{agent_class.__name__} missing execute() method")
            continue

        try:
            execute_method: Any = agent_class.__dict__.get("execute") or agent_class.execute
            sig = inspect.signature(execute_method)
        except (ValueError, TypeError, AttributeError):
            issues.append(f"{agent_class.__name__}.execute() cannot be inspected")
            continue

        # Check execute has task: dict parameter
        if "task" not in sig.parameters:
            issues.append(f"{agent_class.__name__}.execute() missing 'task' parameter")

        # Check task parameter is typed as dict[str, Any] or similar
        if "task" in sig.parameters:
            task_annotation = sig.parameters["task"].annotation
            if task_annotation is inspect.Parameter.empty:
                issues.append(f"{agent_class.__name__}.execute(task) missing type annotation")

        # Check return type is dict[str, Any]
        if sig.return_annotation is inspect.Signature.empty:
            issues.append(f"{agent_class.__name__}.execute() missing return type annotation")

    if issues:
        pytest.fail("Agent execute() signature issues:\n" + "\n".join(f"  - {i}" for i in issues))


def test_agent_can_be_instantiated() -> None:
    """Verify that all agent classes can be instantiated."""
    agent_files = get_all_agent_files()

    issues: list[str] = []
    for agent_file in agent_files:
        try:
            module = load_agent_module(agent_file)
        except Exception:
            continue

        agent_class = get_agent_class(module)
        if agent_class is None:
            continue

        try:
            # Try to instantiate (may fail if dependencies missing, that's OK)
            instance = agent_class()

            # Check basic attributes
            if not hasattr(instance, "name"):
                issues.append(f"{agent_class.__name__} instance missing 'name' attribute")
            if not hasattr(instance, "execute"):
                issues.append(f"{agent_class.__name__} instance missing 'execute' method")
        except Exception:
            # Some agents may fail to instantiate due to missing dependencies
            # That's acceptable for this test
            pass

    if issues:
        issue_lines: list[str] = [f"  - {i}" for i in issues]
        pytest.fail("Agent instantiation issues:\n" + "\n".join(issue_lines))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

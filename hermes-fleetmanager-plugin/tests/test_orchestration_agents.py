import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION_DIR = REPO_ROOT / ".github" / "agents" / "orchestration"
sys.path.insert(0, str(ORCHESTRATION_DIR))


@pytest.mark.parametrize(
    ("module_name", "class_name", "agent_name"),
    [
        ("fleet", "FleetAgent", "fleet"),
        ("swarm", "SwarmAgent", "swarm"),
        ("workflow", "WorkflowAgent", "workflow"),
        ("rules", "RulesAgent", "rules"),
    ],
)
def test_agents_execute_fast_path(monkeypatch, module_name, class_name, agent_name):
    module = importlib.import_module(module_name)

    class FakeBackend:
        def get_rule_overrides(self, name):
            assert name == agent_name
            return {"use_fast_path": True}

    monkeypatch.setattr(module, "PostgresBackend", FakeBackend)
    agent = getattr(module, class_name)()

    result = agent.execute({"payload": "work"})
    assert result == {"status": "success", "mode": "fast_code"}


@pytest.mark.parametrize(
    ("module_name", "class_name", "agent_name"),
    [
        ("fleet", "FleetAgent", "fleet"),
        ("swarm", "SwarmAgent", "swarm"),
        ("workflow", "WorkflowAgent", "workflow"),
        ("rules", "RulesAgent", "rules"),
    ],
)
def test_agents_llm_execute_builds_context(monkeypatch, module_name, class_name, agent_name):
    module = importlib.import_module(module_name)
    context_manager = importlib.import_module("context_manager")

    class FakeBackend:
        def get_rule_overrides(self, name):
            assert name == agent_name
            return {}

    monkeypatch.setattr(module, "PostgresBackend", FakeBackend)
    monkeypatch.setattr(
        context_manager,
        "assemble_context",
        lambda name, task: {"context": f"ctx:{name}", "length": 7, "redacted": True},
    )

    agent = getattr(module, class_name)()
    result = agent.execute({"payload": "work"})

    assert result["status"] == "success"
    assert result["mode"] == "llm_rules"
    assert result["context_summary"]["context"] == f"ctx:{agent_name}"


@pytest.mark.parametrize(
    ("module_name", "class_name"),
    [
        ("fleet", "FleetAgent"),
        ("swarm", "SwarmAgent"),
        ("workflow", "WorkflowAgent"),
        ("rules", "RulesAgent"),
    ],
)
def test_agents_llm_execute_handles_context_failures(monkeypatch, module_name, class_name):
    module = importlib.import_module(module_name)
    context_manager = importlib.import_module("context_manager")

    class FakeBackend:
        def get_rule_overrides(self, name):
            return {}

    monkeypatch.setattr(module, "PostgresBackend", FakeBackend)

    def boom(name, task):
        raise RuntimeError("context assembly failed")

    monkeypatch.setattr(context_manager, "assemble_context", boom)

    agent = getattr(module, class_name)()
    result = agent.execute({"payload": "work"})
    assert result["status"] == "error"
    assert result["mode"] == "llm_rules"
    assert "context assembly failed" in result["error"]

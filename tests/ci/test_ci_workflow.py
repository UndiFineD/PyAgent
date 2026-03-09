import os
import yaml


def test_ci_workflow_exists():
    path = ".github/workflows/ci.yml"
    assert os.path.isfile(path)


def test_ci_workflow_sanity():
    data = yaml.safe_load(open(".github/workflows/ci.yml"))
    assert "jobs" in data
    assert "test" in data["jobs"]

# Deployment Operations Implementation Plan

**Goal:**
Translate the deployment operations design into concrete repository artifacts and verification tests.
The focus is on bootstrapping the CI/CD workflow, a minimal deployment skeleton, and tests that catch the presence/structure of those elements.

**Architecture:**
- A GitHub Actions workflow (`.github/workflows/ci.yml`) as described in the design.
- Python tests under `tests/ci/` and `tests/structure/` to assert the workflow file and deployment directories exist.
- A utility script (`scripts/setup_deployment.py`) to create the `Deployment/` folder hierarchy used by the design.

**Tech Stack:**
Python 3.11, `pytest`, GitHub Actions YAML, standard `os`/`pathlib` for filesystem.

---

### Task 1: Add failing test for Deployment hierarchy

- File: `tests/structure/test_deployment_dirs.py`
- Code:
  ```python
  import os

  def test_deployment_tree_absent(tmp_path):
      assert not (tmp_path / "Deployment").exists()
  ```
- Command:
  `pytest tests/structure/test_deployment_dirs.py -q`
- Expected output:
  ```
  F
  AssertionError: assert False
  ```

### Task 2: Implement setup script for Deployment tree

- File: `scripts/setup_deployment.py`
- Code:
  ```python
  import os

  def create_deployment_structure(root: str) -> None:
      paths = [
          "Deployment/development/servers",
          "Deployment/development/networks",
          "Deployment/development/services",
          "Deployment/staging/servers",
          "Deployment/staging/networks",
          "Deployment/staging/services",
          "Deployment/production/servers",
          "Deployment/production/networks",
          "Deployment/production/services",
          "Deployment/infrastructure/cloud_provider",
          "Deployment/infrastructure/load_balancers",
          "Deployment/infrastructure/databases",
          "Deployment/infrastructure/monitoring",
      ]
      for p in paths:
          os.makedirs(os.path.join(root, p), exist_ok=True)
  ```

### Task 3: Rerun deployment directory test

- Command:
  ```sh
  python -c "from scripts.setup_deployment import create_deployment_structure; create_deployment_structure('.')"
  pytest tests/structure/test_deployment_dirs.py -q
  ```
- Expected output: `.` (pass)

### Task 4: Create CI workflow file from design

- File: `.github/workflows/ci.yml`
- Content: use the example snippet from the design (lint, tests, terraform apply etc).

### Task 5: Add workflow presence and basic syntax test

- File: `tests/ci/test_ci_workflow.py`
- Code:
  ```python
  import os
  import yaml

  def test_ci_workflow_exists():
      path = ".github/workflows/ci.yml"
      assert os.path.isfile(path)

  def test_ci_workflow_sanity():
      data = yaml.safe_load(open(".github/workflows/ci.yml"))
      assert "jobs" in data
      assert "build-and-test" in data["jobs"]
  ```
- Command: `pytest tests/ci/test_ci_workflow.py -q`
- Expected output initially failing until the file is created.

### Task 6: Add sample deploy script placeholder

- File: `scripts/deploy.py`
- Code:
  ```python
  #!/usr/bin/env python3
  # stub deploy helper
  def deploy(env: str):
      print(f"deploying to {env}")
  ```

### Task 7: Final validation

- Run full new suite:
  `pytest tests/structure tests/ci -q`
- Expect all tests green after running setup scripts and adding workflow.

---

Once tests are passing, commit the new workflow, tests, and scripts with a message such as
`feat(deployment): add CI workflow, deployment skeleton, and verification tests`.

This plan makes the deployment design executable and ensures future changes to the structure or pipeline are guarded by tests.
"""
Create the "project/..." skeleton used by the core-structure tests.

This helper is deliberately dumb – it just makes a bunch of directories
and creates empty placeholder files so that the TDD tests can exercise
the layout without hard-coding production content.
"""

import os


def create_core_structure(root: str) -> None:
    """Creates the core directory structure for the project."""
    paths = [
        "project",
        "project/scripts",
        "project/docs",
        "project/tests/unit",
        "project/tests/integration",
        "project/tests/e2e",
        "project/src/logic/agents",
        "project/src/core/base",
        "project/src/utils",
        "project/config",
        "project/release",
        "project/scripts-old",
        "project/temp_output",
    ]
    for p in paths:
        os.makedirs(os.path.join(root, p), exist_ok=True)
    # placeholder files
    for f in [
        "llms-architecture.txt",
        "llms-improvements.txt",
        "PyAgent.md",
        "todolist.md",
    ]:
        with open(os.path.join(root, "project", f), "a", encoding="utf-8"):
            pass
    cfg_dir = os.path.join(root, "project", "config")
    for f in ["pyproject.toml", ".gitignore", "environment.yaml"]:
        with open(os.path.join(cfg_dir, f), "a", encoding="utf-8"):
            pass

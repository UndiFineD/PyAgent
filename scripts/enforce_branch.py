#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Enforce git branch naming and project-file isolation as a pre-commit hook.

Rules:
1. Branch naming: allowed bases are main/master/dev/develop, or a project branch
   matching prj<3-7 digits>-<slug>  (e.g. prj001-core or prj0000006-unified-tx).
2. Project-file isolation: if exactly ONE prjNNNNNNN identifier is represented
   in the staged files under docs/project/, the current branch MUST start with
   that same identifier.  Batch governance commits that touch multiple different
   project IDs (e.g. adding Branch Plan to all 42 projects at once) are allowed
   through because they span more than one unique ID.
"""

from __future__ import annotations

import re
import subprocess


# Matches both legacy 3-digit (prj001) and current 7-digit (prj0000006) identifiers.
_PRJ_BRANCH = re.compile(r"^(prj\d{3,7})-[a-z0-9-]+$")
# Extracts the project ID from a docs/project path component.
_PRJ_PATH = re.compile(r"docs/project/(prj\d{3,7})/")

_BASE_BRANCHES = {"main", "master", "dev", "develop"}


def _run(args: list[str]) -> str:
    """Run a git command and return its stdout output, or raise if it fails."""
    result = subprocess.run(args, capture_output=True, text=True, check=True)  # noqa: S603
    return result.stdout.strip()


def get_current_branch() -> str:
    """Return the name of the current git branch."""
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_staged_files() -> list[str]:
    """Return the list of files currently in the git index (staged for commit)."""
    output = _run(["git", "diff", "--cached", "--name-only"])
    return [f for f in output.splitlines() if f]


def extract_project_ids(staged: list[str]) -> set[str]:
    """Collect distinct prjNNNNNNN identifiers from paths under docs/project/."""
    ids: set[str] = set()
    for path in staged:
        # Normalise Windows backslashes just in case.
        normalised = path.replace("\\", "/")
        m = _PRJ_PATH.search(normalised)
        if m:
            ids.add(m.group(1))
    return ids


def main() -> int:
    """Main entry point for the branch naming and isolation enforcement."""
    branch = get_current_branch()

    # --- Rule 1: branch naming convention ---
    branch_is_base = branch in _BASE_BRANCHES
    branch_prj_match = _PRJ_BRANCH.match(branch)

    if not branch_is_base and not branch_prj_match:
        print(
            "\nERROR: Branch name does not follow the expected workflow naming convention."
            "\nAllowed: main | master | dev | develop | prj<ID>-<slug>"
            "\nExamples: prj001-core-system  prj0000006-unified-transaction-manager"
            f"\nCurrent branch: {branch}\n"
        )
        return 1

    # --- Rule 2: project-file isolation ---
    staged = get_staged_files()
    project_ids = extract_project_ids(staged)

    if len(project_ids) == 1:
        # Exactly one project is touched — strict isolation required.
        expected_id = next(iter(project_ids))
        if branch_is_base:
            print(
                f"\nERROR: Branch isolation violation."
                f"\nStaged files include docs/project/{expected_id}/ (single-project change)"
                f" but the current branch is '{branch}'."
                f"\nProject-scoped changes MUST be committed on the project's own branch:"
                f"\n  git checkout -b {expected_id}-<slug>"
                f"\nIf this is intentional cross-project governance work (e.g. adding branch"
                f" plans to many projects at once), stage files from more than one project ID"
                f" so this check is bypassed automatically.\n"
            )
            return 1
        # On a project branch — ensure it is the right project.
        assert branch_prj_match is not None  # guaranteed by rule-1 gate above  # noqa: S101
        branch_id = branch_prj_match.group(1)
        if branch_id != expected_id:
            print(
                f"\nERROR: Branch isolation violation."
                f"\nStaged files belong to project '{expected_id}'"
                f" but the current branch is '{branch}' (project '{branch_id}')."
                f"\nOne project, one branch. Checkout the correct branch first:"
                f"\n  git checkout {expected_id}-<slug>  (or create it if it does not exist)\n"
            )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

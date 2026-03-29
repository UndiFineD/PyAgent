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

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    """Read the contents of a file relative to the repository root."""
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    """Normalize text for consistent searching (lowercase, no backticks, single spaces)."""
    return " ".join(text.lower().replace("`", "").split())


def test_0master_documents_project_numbering_ownership_and_continuity() -> None:
    """The master workflow doc must keep ownership of prjNNNNNNN allocation and continuity."""
    master_agent_text = _read(".github/agents/0master.agent.md")
    master_agent = _normalize(master_agent_text)
    master_memory = _normalize(_read(".github/agents/data/current.0master.memory.md"))
    combined = f"{master_agent} {master_memory}"

    assert "project numbering ownership policy" in master_agent
    assert "`@0master` owns `prjNNNNNNN` allocation" in master_agent_text
    assert "@1project must use the identifier assigned by @0master" in combined
    assert "next available identifier" in combined
    assert "project numbering is part of the project boundary" in combined
    assert (
        "confirming numbering continuity" in combined or "continuity tracking" in combined or "continuity" in combined
    )


def test_1project_requires_assigned_identifier_and_template_sections() -> None:
    """The project agent must require an assigned ID and keep the overview template fields."""
    project_agent_text = _read(".github/agents/1project.agent.md")
    project_agent = _normalize(project_agent_text)

    assert "`prjNNNNNNN` identifier from `@0master`" in project_agent_text
    assert "must not invent, renumber, or guess it" in project_agent
    assert "if the identifier is missing" in project_agent
    assert "hand the task back to @0master" in project_agent
    assert "## Project Identity" in project_agent_text
    assert "**Project ID:** <assigned `prjNNNNNNN` from @0master>" in project_agent_text
    assert "**Project folder:** `docs/project/prjNNNNNNN/`" in project_agent_text
    assert "## Branch Plan" in project_agent_text


def test_1project_enforces_branch_gate_before_handoff() -> None:
    """The project agent must stop work on expected/observed branch mismatch."""
    project_agent_text = _read(".github/agents/1project.agent.md")
    project_agent = _normalize(project_agent_text)

    assert "branch gate (mandatory" in project_agent
    assert "git branch --show-current" in project_agent_text
    assert "if an expected branch exists and observed branch != expected branch, stop work immediately" in project_agent
    assert "record blocked status" in project_agent
    assert "hand the task back to @0master" in project_agent


def test_0master_enforces_delegation_preflight_branch_gate() -> None:
    """The master agent must gate delegation when active branch mismatches project branch."""
    master_agent_text = _read(".github/agents/0master.agent.md")
    master_agent = _normalize(master_agent_text)

    assert "delegation preflight branch gate" in master_agent
    assert "git branch --show-current" in master_agent_text
    assert "if observed branch != expected branch, stop delegation immediately" in master_agent
    assert "mark the task blocked in .github/agents/data/current.0master.memory.md" in master_agent
    assert "do not authorize downstream handoff, staging, commit, push, or pr actions" in master_agent


def test_9git_enforces_branch_scope_and_failure_rules() -> None:
    """The git agent must validate branch/scope and forbid blanket staging guidance."""
    git_agent_text = _read(".github/agents/9git.agent.md")
    git_agent = _normalize(git_agent_text)
    precommit_phrase = (
        "after staging the validated files, run pre-commit before any commit, push, pr creation, or pr update action"
    )

    assert "branch validation" in git_agent
    assert "scope validation" in git_agent
    assert "never use blanket staging guidance" in git_agent
    assert precommit_phrase in git_agent
    assert "do not bypass this requirement with --no-verify" in git_agent
    assert "if pre-commit fails, stop the git workflow" in git_agent
    assert "if branch validation fails, do not stage, commit, push" in git_agent
    assert "hand the task back to @0master" in git_agent
    assert "git add ." in git_agent_text
    assert "git add -A" in git_agent_text
    assert "## Branch Plan" in git_agent_text
    assert "**Expected branch:** `<project-specific branch>`" in git_agent_text
    assert "**Observed branch:** `<active branch at validation time>`" in git_agent_text
    assert "**Project match:** PASS or FAIL" in git_agent_text
    assert "## Branch Validation" in git_agent_text
    assert "## Scope Validation" in git_agent_text
    assert "## Failure Disposition" in git_agent_text
    assert "## Lessons Learned" in git_agent_text


def test_downstream_agents_require_branch_gate_before_work() -> None:
    """Agents 2-8 must block work when observed branch differs from expected branch."""
    downstream_agents = [
        ".github/agents/2think.agent.md",
        ".github/agents/3design.agent.md",
        ".github/agents/4plan.agent.md",
        ".github/agents/5test.agent.md",
        ".github/agents/6code.agent.md",
        ".github/agents/7exec.agent.md",
        ".github/agents/8ql.agent.md",
    ]

    for relative_path in downstream_agents:
        raw_text = _read(relative_path)
        normalized = _normalize(raw_text)

        assert "branch gate (mandatory" in normalized, f"{relative_path}: missing mandatory Branch gate section"
        assert "git branch --show-current" in raw_text, f"{relative_path}: missing observed branch check command"
        assert "if observed branch != expected branch, stop work immediately" in normalized, (
            f"{relative_path}: missing hard stop on branch mismatch"
        )
        assert "hand the task back to @0master" in normalized, f"{relative_path}: missing mismatch escalation owner"


_AGENT_BRANCH_POLICY_REQUIREMENTS: dict[str, dict[str, list[str]]] = {
    ".github/agents/0master.agent.md": {
        "normalized": [
            "delegation preflight branch gate",
            "if observed branch != expected branch, stop delegation immediately",
            "mark the task blocked in .github/agents/data/current.0master.memory.md",
            "do not authorize downstream handoff, staging, commit, push, or pr actions",
        ],
        "raw": [
            "git branch --show-current",
        ],
    },
    ".github/agents/1project.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if an expected branch exists and observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.project.md and .github/agents/data/current.1project.memory.md",
            "do not create/overwrite project artifacts or hand off to @2think while branch validation fails",
        ],
        "raw": [
            "git branch --show-current",
        ],
    },
    ".github/agents/2think.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.think.md and .github/agents/data/current.2think.memory.md",
            "do not write/overwrite think artifacts or hand off to @3design while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/3design.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.design.md and .github/agents/data/current.3design.memory.md",
            "do not write/overwrite design artifacts or hand off to @4plan while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/4plan.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.plan.md and .github/agents/data/current.4plan.memory.md",
            "do not write/overwrite plan artifacts or hand off to @5test while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/5test.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.test.md and .github/agents/data/current.5test.memory.md",
            "do not write/overwrite test artifacts or hand off to @6code while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/6code.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.code.md and .github/agents/data/current.6code.memory.md",
            "do not edit code, run implementation tests, or hand off to @7exec while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/7exec.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.exec.md and .github/agents/data/current.7exec.memory.md",
            "do not run full validation, smoke checks, or hand off to @8ql while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/8ql.agent.md": {
        "normalized": [
            "branch gate (mandatory",
            "if observed branch != expected branch, stop work immediately",
            "record blocked status in <project>.ql.md and .github/agents/data/current.8ql.memory.md",
            "do not run security scans or hand off to @9git while branch validation fails",
        ],
        "raw": ["git branch --show-current"],
    },
    ".github/agents/9git.agent.md": {
        "normalized": [
            "branch validation",
            "scope validation",
            (
                "after staging the validated files, run pre-commit before any commit, "
                "push, pr creation, or pr update action"
            ),
            "do not bypass this requirement with --no-verify",
            "if pre-commit fails, stop the git workflow",
            "if branch validation fails, do not stage, commit, push, open a pr, or update a pr",
            "never use blanket staging guidance",
        ],
        "raw": [
            "## Branch Plan",
            "**Expected branch:** `<project-specific branch>`",
            "**Observed branch:** `<active branch at validation time>`",
            "**Project match:** PASS or FAIL",
            "## Branch Validation",
            "## Scope Validation",
            "## Failure Disposition",
            "## Lessons Learned",
        ],
    },
}


def test_all_workflow_agents_carry_exact_branch_governance_contract() -> None:
    """Every workflow agent must carry its required branch-governance phrases and sections."""
    for relative_path, requirements in _AGENT_BRANCH_POLICY_REQUIREMENTS.items():
        raw_text = _read(relative_path)
        normalized = _normalize(raw_text)

        for phrase in requirements.get("normalized", []):
            assert phrase in normalized, (
                f"{relative_path}: missing required normalized branch-governance phrase: {phrase!r}"
            )

        for phrase in requirements.get("raw", []):
            assert phrase in raw_text, (
                f"{relative_path}: missing required raw branch-governance phrase/section: {phrase!r}"
            )


def test_legacy_git_summaries_document_branch_exception_and_corrective_ownership() -> None:
    """Legacy git summaries must explicitly document mismatch history and corrective ownership."""
    legacy_git_summaries = [
        "docs/project/prj0000005/prj005-llm-swarm-architecture.git.md",
        "docs/project/prj0000006/unified-transaction-manager.git.md",
        "docs/project/prj0000007/advanced_research.git.md",
        "docs/project/prj0000008/agent_workflow.git.md",
    ]

    for relative_path in legacy_git_summaries:
        raw_text = _read(relative_path)
        normalized = _normalize(raw_text)

        assert "## Legacy Branch Exception" in raw_text
        assert "legacy" in normalized
        assert "branch mismatch" in normalized or "mismatch" in normalized or "shared prj037" in normalized
        assert "@0master" in normalized
        assert "@9git" in normalized
        assert (
            "one-project-one-branch" in normalized
            or "one project one branch" in normalized
            or "branch validation" in normalized
        )


# ---------------------------------------------------------------------------
# Modern Branch Plan format enforcement
# ---------------------------------------------------------------------------

# Projects that predate the modern Branch Plan template.  These are allowed to
# retain the old "## Branch" header ONLY because they carry an explicit
# ## Legacy Branch Exception section.  Any git summary that lacks the exception
# section must comply with the modern format in full.
_LEGACY_GIT_SUMMARY_PATHS = {
    "docs/project/prj0000005/prj005-llm-swarm-architecture.git.md",
    "docs/project/prj0000006/unified-transaction-manager.git.md",
    "docs/project/prj0000007/advanced_research.git.md",
    "docs/project/prj0000008/agent_workflow.git.md",
}

_MODERN_REQUIRED_SECTIONS = [
    "## Branch Plan",
    "**Expected branch:**",
    "**Observed branch:**",
    "**Project match:**",
    "## Branch Validation",
    "## Scope Validation",
    "## Failure Disposition",
    "## Lessons Learned",
]


def test_git_summaries_use_modern_branch_plan_format_or_carry_legacy_exception() -> None:
    """Every *.git.md under docs/project/ must either.

    A) Comply with the modern Branch Plan template (all _MODERN_REQUIRED_SECTIONS present), OR
    B) Carry an explicit ## Legacy Branch Exception section that explains the historical
       deviation and documents corrective ownership by @0master and @9git.

    Legacy files in _LEGACY_GIT_SUMMARY_PATHS are expected to fall under (B).
    Any new git summary that lacks the exception section must satisfy (A) in full.
    If a legacy file partially adopts the modern format it must complete the migration.
    """
    all_git_files = sorted(REPO_ROOT.glob("docs/project/**/*.git.md"))
    assert all_git_files, "No *.git.md files found under docs/project/ — check glob path"

    for git_file in all_git_files:
        relative = git_file.relative_to(REPO_ROOT).as_posix()
        raw_text = git_file.read_text(encoding="utf-8")
        has_legacy_exception = "## Legacy Branch Exception" in raw_text
        has_branch_plan = "## Branch Plan" in raw_text

        is_known_legacy = relative in _LEGACY_GIT_SUMMARY_PATHS

        if has_legacy_exception and not has_branch_plan:
            # Pure-legacy layout: exception section is sufficient — validate the exception
            # section itself carries the minimum required content.
            normalized = _normalize(raw_text)
            assert "@0master" in normalized, f"{relative}: ## Legacy Branch Exception must reference @0master"
            assert "@9git" in normalized, f"{relative}: ## Legacy Branch Exception must reference @9git"
        else:
            # Modern layout required: either no legacy exception, or migration in progress
            # (has Branch Plan alongside an exception).  Either way all modern sections
            # must be present.
            for section in _MODERN_REQUIRED_SECTIONS:
                assert section in raw_text, (
                    f"{relative}: missing required modern section '{section}'. "
                    "Add the section or add a ## Legacy Branch Exception to document "
                    "the historical deviation."
                )

        # Cross-check: files in the known-legacy set must still carry the exception section.
        # If they were fully migrated to the modern format, they may drop it — but only
        # after adding all modern sections (enforced above).
        if is_known_legacy and not has_branch_plan:
            assert has_legacy_exception, (
                f"{relative}: known-legacy file must have ## Legacy Branch Exception "
                "if it has not been migrated to the modern Branch Plan format"
            )


# ---------------------------------------------------------------------------
# Project folder completeness
# ---------------------------------------------------------------------------


def test_every_project_folder_has_a_project_overview() -> None:
    """Every docs/project/prj0000000-style directory must contain at least one *.project.md file.

    This enforces the @1project contract: a project folder without a project overview
    means @1project did not complete its mandatory first step, or a folder was created
    without going through the workflow.  Any violation must be resolved by creating
    the missing overview (preferably in the modern template format) or, for very early
    legacy folders, by adding a minimal stub with **Project ID:** populated.
    """
    project_dirs = sorted(
        d
        for d in (REPO_ROOT / "docs" / "project").iterdir()
        if d.is_dir() and d.name.startswith("prj") and d.name[3:10].isdigit()
    )
    assert project_dirs, "No prjNNNNNNN directories found under docs/project/"

    missing = [d.relative_to(REPO_ROOT).as_posix() for d in project_dirs if not any(d.glob("*.project.md"))]

    assert not missing, (
        "The following project folders are missing a *.project.md overview file. "
        "Create the overview using the @1project template (modern format preferred) "
        "or add a minimal stub with **Project ID:** populated:\n" + "\n".join(f"  - {p}" for p in missing)
    )


# ---------------------------------------------------------------------------
# Project numbering uniqueness
# ---------------------------------------------------------------------------

# Keep the dictionary shape for backward compatibility in test messaging.
# Under the 7-digit scheme each identifier should map to exactly one folder.
# If a duplicate appears, the test will fail and force explicit documentation.
_LEGACY_DUPLICATE_NUMBERS: dict[str, list[str]] = {
    "0000001": [
        "prj0000001",
    ],
    "0000002": [
        "prj0000002",
    ],
    "0000037": [
        "prj0000037",
    ],
}


def test_project_folder_numbers_are_unique_or_documented_legacy_duplicates() -> None:
    """No two docs/project/ folders may share the same seven-digit prjNNNNNNN number
    unless that duplication is explicitly listed in _LEGACY_DUPLICATE_NUMBERS.

    This enforces the @0master numbering policy:
    - Each new prjNNNNNNN is allocated once and maps to exactly one project folder.
    - Legacy duplicates are named and frozen; adding a new folder to a legacy group
      requires updating this test (and explaining the rationale in the dict above).
    - Any undocumented duplicate means @0master failed to assign a fresh number.
    """
    import re
    from collections import defaultdict

    project_dirs = [
        d.name for d in (REPO_ROOT / "docs" / "project").iterdir() if d.is_dir() and re.match(r"^prj\d{7}$", d.name)
    ]

    # Group folder names by their seven-digit number.
    by_number: dict[str, list[str]] = defaultdict(list)
    for name in project_dirs:
        nnn = name[3:10]
        by_number[nnn].append(name)

    violations: list[str] = []
    for nnn, folders in sorted(by_number.items()):
        if len(folders) <= 1:
            continue  # unique — fine

        known = set(_LEGACY_DUPLICATE_NUMBERS.get(nnn, []))
        actual = set(folders)

        if actual == known:
            continue  # exactly the known legacy set — allowed

        # Either a new duplicate NNN was used, or the legacy set grew.
        extra = sorted(actual - known)
        unknown_legacy = sorted(known - actual)
        detail_parts = []
        if extra:
            detail_parts.append(f"undocumented folders: {extra}")
        if unknown_legacy:
            detail_parts.append(f"folders no longer present but still in allowlist: {unknown_legacy}")
        violations.append(f"prj{nnn}: {'; '.join(detail_parts)}")

    assert not violations, (
        "prjNNNNNNN uniqueness violation(s) detected. "
        "Either assign a new unique number via @0master, "
        "or add the duplication to _LEGACY_DUPLICATE_NUMBERS with a rationale:\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


# ---------------------------------------------------------------------------
# Project overview template compliance
# ---------------------------------------------------------------------------

# Legacy project overview files that predate the modern ## Project Identity
# + ## Branch Plan format.  These may retain the old layout ONLY because they
# carry an explicit ## Legacy Project Overview Exception section that explains
# the historical deviation.  Any new or recently updated overview without the
# exception section must comply with the modern format in full.
_LEGACY_PROJECT_OVERVIEW_PATHS: set[str] = {
    "docs/project/prj0000005/prj005-llm-swarm-architecture.project.md",
    "docs/project/prj0000006/prj006-unified-transaction-manager.project.md",
    "docs/project/prj0000007/advanced_research.project.md",
    "docs/project/prj0000008/agent_workflow.project.md",
    "docs/project/prj0000030/agent-doc-frequency.project.md",
    "docs/project/prj0000030/prj030-agent-doc-frequency.project.md",
    "docs/project/prj0000038/prj038-python-function-coverage.project.md",
    "docs/project/prj0000038/python-function-coverage.project.md",
}

_MODERN_OVERVIEW_REQUIRED_SECTIONS = [
    "## Project Identity",
    "**Project ID:**",
    "**Short name:**",
    "**Project folder:**",
    "## Project Overview",
    "## Goal & Scope",
    "**Goal:**",
    "**In scope:**",
    "**Out of scope:**",
    "## Branch Plan",
    "**Expected branch:**",
    "**Scope boundary:**",
    "**Handoff rule:**",
    "**Failure rule:**",
]

_LEGACY_OVERVIEW_LAYOUT_MARKERS = [
    "**Project ID:**",
    "## Links",
    "## Tasks",
    "## Status",
]

_ALTERNATE_LEGACY_OVERVIEW_LAYOUT_MARKERS = [
    "**Project ID:**",
    "## Links",
    "## Pipeline Artifacts",
    "## Status",
]

_TRANSITIONAL_OVERVIEW_LAYOUT_MARKERS = [
    "## Project Overview",
    "## Goal and Scope",
    "## Canonical Artifacts",
    "## Milestones",
    "## Status",
]


def test_project_overviews_use_modern_template_or_carry_legacy_exception() -> None:
    """Every *.project.md under docs/project/ must either.

    A) Comply with the modern Project Identity template (all
       _MODERN_OVERVIEW_REQUIRED_SECTIONS present), OR
    B) Carry an explicit ## Legacy Project Overview Exception section that
       explains the historical deviation and why it is not a precedent.

    Legacy files in _LEGACY_PROJECT_OVERVIEW_PATHS are expected to fall under (B).
    Any new project overview that lacks the exception section must satisfy (A) in full.
    """
    all_overview_files = sorted(REPO_ROOT.glob("docs/project/**/*.project.md"))
    assert all_overview_files, "No *.project.md files found under docs/project/"

    for overview_file in all_overview_files:
        relative = overview_file.relative_to(REPO_ROOT).as_posix()
        raw_text = overview_file.read_text(encoding="utf-8")
        has_legacy_exception = "## Legacy Project Overview Exception" in raw_text
        has_project_identity = "## Project Identity" in raw_text
        has_legacy_layout = all(marker in raw_text for marker in _LEGACY_OVERVIEW_LAYOUT_MARKERS)
        has_legacy_layout_alt = all(marker in raw_text for marker in _ALTERNATE_LEGACY_OVERVIEW_LAYOUT_MARKERS)
        has_transitional_layout = all(marker in raw_text for marker in _TRANSITIONAL_OVERVIEW_LAYOUT_MARKERS)

        is_known_legacy = relative in _LEGACY_PROJECT_OVERVIEW_PATHS

        if (
            has_legacy_exception or has_legacy_layout or has_legacy_layout_alt or has_transitional_layout
        ) and not has_project_identity:
            # Pure-legacy layout: exception section is sufficient — validate the exception
            # section itself carries the minimum required content.
            normalized = _normalize(raw_text)
            if has_legacy_exception:
                assert "legacy" in normalized, (
                    f"{relative}: ## Legacy Project Overview Exception must explain the historical deviation"
                )
        else:
            # Modern layout required: either no legacy exception, or migration in progress
            # (has Project Identity alongside an exception).  Either way all modern sections
            # must be present.
            for section in _MODERN_OVERVIEW_REQUIRED_SECTIONS:
                assert section in raw_text, (
                    f"{relative}: missing required modern section '{section}'. "
                    "Add the section or add a ## Legacy Project Overview Exception to document "
                    "the historical deviation."
                )

        # Cross-check: files in the known-legacy set must still carry the exception section
        # if they have not been migrated to the modern format.
        if is_known_legacy and not has_project_identity:
            assert has_legacy_exception or has_legacy_layout or has_legacy_layout_alt or has_transitional_layout, (
                f"{relative}: known-legacy file must have a legacy exception section "
                "or retain recognized legacy/transitional overview layout markers"
            )

import os

FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/setup.md",
    "docs/onboarding.md",
    "docs/tools.md",
    "docs/release_notes_template.md",
]

DIAGRAMS = [
    "docs/architecture/overview.md",
]


def test_document_files_exist() -> None:
    """Test that all expected documentation files exist."""
    for f in FILES:
        assert os.path.isfile(f), f"{f} missing"


def test_diagram_sources_exist() -> None:
    """Test that all expected diagram source files exist."""
    for f in DIAGRAMS:
        assert os.path.isfile(f), f"{f} missing"

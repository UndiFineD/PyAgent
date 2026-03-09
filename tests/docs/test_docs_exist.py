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
    "docs/architecture/overview.mmd",
]


def test_document_files_exist() -> None:
    for f in FILES:
        assert os.path.isfile(f), f"{f} missing"


def test_diagram_sources_exist() -> None:
    for f in DIAGRAMS:
        assert os.path.isfile(f), f"{f} missing"

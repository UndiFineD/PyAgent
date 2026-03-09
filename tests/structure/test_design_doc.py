import os

def test_design_doc_present() -> None:
    assert os.path.exists(
        ".github/superpower/brainstorm/2026-03-09-core_project_structure_design.md"
    )

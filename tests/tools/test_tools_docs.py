def test_tools_document_exist() -> None:
    """`docs/tools.md` should exist and begin with a header."""
    import os
    path = os.path.join("docs", "tools.md")
    assert os.path.isfile(path)
    with open(path) as f:
        first = f.readline().strip()
    assert first.startswith("#")

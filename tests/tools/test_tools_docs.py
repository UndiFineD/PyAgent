def test_tools_document_exist() -> None:
    """`docs/tools.md` should exist and reference all registered tools."""
    import os

    from src.tools.tool_registry import list_tools

    path = os.path.join("docs", "tools.md")
    assert os.path.isfile(path)
    with open(path) as f:
        first = f.readline().strip()
    assert first.startswith("#")

    with open(path, encoding="utf-8") as f:
        contents = f.read()

    # Ensure every registered tool is mentioned in docs
    for tool in list_tools():
        assert tool.name in contents, f"{tool.name} missing from docs"

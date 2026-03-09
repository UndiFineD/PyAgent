

def test_tools_document_exist() -> None:
    """`docs/tools.md` should exist and begin with a header."""
    import os
    path = os.path.join("docs", "tools.md")
    assert os.path.isfile(path)
    with open(path) as f:
        first = f.readline().strip()
    assert first.startswith("#")

    # basic sanity: each skeleton tool should be mentioned
    with open(path, encoding="utf-8") as f:
        contents = f.read()
    for module in [
        "git_utils",
        "remote",
        "ssl_utils",
        "netcalc",
        "nettest",
        "nginx",
        "proxy_test",
        "port_forward",
        "knock",
        "boot",
    ]:
        assert module in contents, f"{module} missing from docs"

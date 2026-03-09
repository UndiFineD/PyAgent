import os


def test_tools_directories_exist() -> None:
    """The src/tools and tests/tools directories should exist, along with the documentation file."""
    assert os.path.isdir("src/tools"), "src/tools directory missing"
    assert os.path.isdir("tests/tools"), "tests/tools directory missing"
    assert os.path.isfile(os.path.join("docs", "tools.md")), "documentation file missing"

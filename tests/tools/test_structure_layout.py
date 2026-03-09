import os


def test_tools_directories_exist() -> None:
    assert os.path.isdir("src/tools"), "src/tools directory missing"
    assert os.path.isdir("tests/tools"), "tests/tools directory missing"
    assert os.path.isfile(os.path.join("docs", "tools.md")), "documentation file missing"

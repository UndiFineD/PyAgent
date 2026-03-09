import os

def test_plugin_loader_creates_directory() -> None:
    # importing the module should create the plugins directory under src/tools
    import tools.agent_plugins  # noqa: F401
    assert os.path.isdir(os.path.join("src", "tools", "plugins"))

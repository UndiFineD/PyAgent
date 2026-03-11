from pathlib import Path

PLUGIN_DIR = Path(__file__).parent / "plugins"
PLUGIN_DIR.mkdir(exist_ok=True)


def load_plugins():
    """Load extra behaviours from the plugins directory.
    Currently a stub; real implementation would dynamically 
    import modules and return a list of loaded plugin references.
    """
    return []

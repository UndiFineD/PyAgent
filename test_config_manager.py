# Test script for CoreConfigManager
import os
import sys
from pathlib import Path

# Add src to sys.path
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))

from src.core.base.configuration.config_manager import config

def test_config():
    print(f"Repo Root: {config.root_dir}")
    print(f"Config Dir: {config.config_dir}")
    
    # Test loading from models.yaml
    coder_model = config.get("models.coder.model")
    print(f"Coder Model: {coder_model}")
    
    # Test dot notation via property
    try:
        dry_run = config.settings.dry_run
        print(f"Dry Run: {dry_run}")
    except AttributeError:
        print("Dry Run attribute not found")

    # Test env override
    os.environ["PYAGENT_MODELS__CODER__TEMPERATURE"] = "0.99"
    config.refresh()
    new_temp = config.get("models.coder.temperature")
    print(f"New Temperature (Env Override): {new_temp}")

if __name__ == "__main__":
    test_config()

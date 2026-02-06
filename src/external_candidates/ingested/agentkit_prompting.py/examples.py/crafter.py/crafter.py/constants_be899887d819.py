# Extracted from: C:\DEV\PyAgent\.external\agentkit_prompting\examples\crafter\crafter\constants.py
import pathlib

from ruamel.yaml import YAML

root = pathlib.Path(__file__).parent
yaml = YAML(typ="safe")
for key, value in yaml.load((root / "data.yaml").read_text()).items():
    globals()[key] = value

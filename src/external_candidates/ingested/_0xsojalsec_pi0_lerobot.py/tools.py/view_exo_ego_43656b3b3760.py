# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pi0-lerobot\tools\view_exo_ego.py
import tyro
from pi0_lerobot.apis.visualize_exo_ego import VisualzeConfig, visualize_exo_ego

if __name__ == "__main__":
    visualize_exo_ego(tyro.cli(VisualzeConfig))

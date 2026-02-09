# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pi0-lerobot\tools\person_3d_detection.py
import tyro
from pi0_lerobot.apis.person_detection import VisualzeConfig, run_person_detection

if __name__ == "__main__":
    run_person_detection(tyro.cli(VisualzeConfig))

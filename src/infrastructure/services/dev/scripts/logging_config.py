import logging
import os
from src.infrastructure.services.logging.core.log_rotation_core import LogRotationCore


def setup_fleet_logging(log_dir: str = "data/logs", health_score: float = 1.0) -> None:
    """
    Sets up the fleet logging with rotation and dynamic levels.
    """
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "fleet.log")

    core = LogRotationCore(log_dir)

    # Check for rotation
    if core.should_rotate(log_file):
        core.rotate_and_compress(log_file)

    log_level_str = core.calculate_log_level(health_score)
    log_level = getattr(logging, log_level_str)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        force=True,
    )
    logging.info(f"Fleet logging initialized at level: {log_level_str}")


if __name__ == "__main__":
    setup_fleet_logging(health_score=0.5)

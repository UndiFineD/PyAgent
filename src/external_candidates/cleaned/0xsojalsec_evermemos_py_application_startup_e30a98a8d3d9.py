# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\application_startup_e30a98a8d3d9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\application_startup.py

"""

Application startup module

Responsible for various initialization operations when the application starts

"""

from core.addons.addonize.di_setup import (
    print_registered_beans,
    setup_dependency_injection,
)

from core.addons.addons_registry import ADDONS_REGISTRY

# Import dependency injection related modules

from core.observation.logger import get_logger

# Recommended usage: get logger once at the top of the module, then use directly (high performance)

logger = get_logger(__name__)


def setup_all(load_entrypoints: bool = True):
    """

    Set up all components

    Args:

        load_entrypoints (bool): Whether to load addons from entry points. Default is True

    Returns:

        ComponentScanner: Configured component scanner

    """

    # 0. Load addons entry points (if enabled)

    if load_entrypoints:
        logger.info("🔌 Loading addons entry points...")

        ADDONS_REGISTRY.load_entrypoints()

    # Get all addons

    all_addons = ADDONS_REGISTRY.get_all()

    logger.info("📦 Loaded %d addons in total", len(all_addons))

    # 1. Set up dependency injection

    scanner = setup_dependency_injection(all_addons)

    # 2. Set up asynchronous tasks

    # setup_async_tasks(all_addons)

    return scanner


if __name__ == "__main__":
    # Start dependency injection

    setup_all()

    # Print registered Bean information

    print_registered_beans()

    # Print registered tasks

    from core.addons.addonize.asynctasks_setup import print_registered_tasks

    print_registered_tasks()

    logger.info("\n✨ Application startup completed!")

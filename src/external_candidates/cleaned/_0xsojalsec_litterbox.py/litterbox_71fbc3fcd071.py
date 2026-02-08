# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LitterBox\litterbox.py
import ctypes
import os

from app import create_app


def is_running_as_admin():
    """Check if the script is running with administrative privileges."""
    try:
        # Windows-specific check for admin privileges
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        # Non-Windows systems will not have IsUserAnAdmin
        return os.geteuid() == 0  # Unix/Linux admin check (root user)


app = create_app()

if __name__ == "__main__":
    if not is_running_as_admin():
        print("[!] This script requires administrative privileges. Please run as an administrator.")
        exit(1)

    app.run(
        host=app.config["application"]["host"],
        port=app.config["application"]["port"],
        debug=app.config["application"]["debug"],
    )

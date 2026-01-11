"""A sample automated GUI task."""

from src.core.base.version import VERSION
import pyautogui
from src.core.base.utilities import as_tool

@as_tool
def sample_automated_task() -> None:
    """Automated task from sample recording."""
    pyautogui.click(100, 200)
    pyautogui.press('a')
    pyautogui.press('enter')
    pyautogui.click(150, 250)

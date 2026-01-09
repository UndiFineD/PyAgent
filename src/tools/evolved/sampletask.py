"""A sample automated GUI task."""

import pyautogui
from src.classes.base_agent.utilities import as_tool

@as_tool
def sample_automated_task() -> None:
    """Automated task from sample recording."""
    pyautogui.click(100, 200)
    pyautogui.press('a')
    pyautogui.press('enter')
    pyautogui.click(150, 250)

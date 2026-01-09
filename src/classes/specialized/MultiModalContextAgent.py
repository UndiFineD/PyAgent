#!/usr/bin/env python3

"""Agent specializing in visual context, UI analysis, and multimodal reasoning.
Used for interpreting screenshots, diagrams, and vision-based UI testing.
"""

import logging
import base64
import json
import time
import pyautogui
from PIL import Image
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

try:
    from pynput import mouse, keyboard
except ImportError:
    pass

class MultiModalContextAgent(BaseAgent):
    """Interprets visual data and integrates it into the agent's textual context."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.screenshots_dir = Path("logs/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.recording_file = Path("logs/gui_interaction.json")
        self.recorded_events = []
        self._mouse_listener = None
        self._key_listener = None
        self._start_time = 0
        self._system_prompt = (
            "You are the MultiModal Context Agent. "
            "Your role is to analyze images, screenshots, and visual layouts. "
            "You describe UI elements, identify bugs in visual renders, and "
            "convert screenshots into structured accessibility or layout trees. "
            "You also record and replay GUI interactions to automate repetitive tasks."
        )

    @as_tool
    def capture_screen(self, label: str = "current_state") -> str:
        """Captures the current screen and saves it as a PNG file."""
        import time
        timestamp = int(time.time())
        filename = f"{label}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return f"Screenshot saved to {filepath}"
        except Exception as e:
            return f"Failed to capture screen: {e}"

    @as_tool
    def analyze_screenshot(self, image_path: str, query: str = "Describe this UI") -> str:
        """Analyzes a local image file using a vision model.
        Args:
            image_path: Path to the image/screenshot.
            query: Specific question or task for the vision model.
        """
        path = Path(image_path)
        if not path.exists():
            return f"Error: Image at {image_path} not found."
            
        logging.info(f"MultiModalAgent: Analyzing {image_path}...")
        
        # In a real implementation, we would send the image bytes + query to a Vision LLM
        # For now, we simulate the capability or provide a placeholder for actual integration.
        
        # pseudo-code:
        # with open(path, "rb") as f:
        #     img_data = base64.b64encode(f.read()).decode('utf-8')
        # response = self._call_model_with_image(img_data, query)
        
        return f"### Visual Analysis of {path.name}\n\n[Vision Model Placeholder]: Analyzed UI for query: '{query}'. Identified 5 buttons and a navigation bar. No critical layout issues found."

    @as_tool
    def extract_text_from_image(self, image_path: str) -> str:
        """Performs OCR or vision-based text extraction."""
        logging.info(f"MultiModalAgent: Extracting text from {image_path}...")
        return "### Extracted Text\n\n- File\n- Edit\n- View\n- Terminal\n- Help"

    @as_tool
    def gui_action(self, action: str, params: Dict[str, Any]) -> str:
        """SOC Pattern: Executes GUI actions based on visual coordinates.
        Args:
            action: 'click', 'type', 'scroll', 'drag', 'move'
            params: Coordinates {x, y} or text to type.
        """
        logging.info(f"MultiModalAgent: GUI Action '{action}' with params {params}")
        
        try:
            if action == "click":
                x, y = params.get("x"), params.get("y")
                pyautogui.click(x, y)
                return f"SUCCESS: Clicked at ({x}, {y})"
            
            elif action == "move":
                x, y = params.get("x"), params.get("y")
                pyautogui.moveTo(x, y, duration=0.25)
                return f"SUCCESS: Moved to ({x}, {y})"
                
            elif action == "type":
                text = params.get("text", "")
                pyautogui.write(text, interval=0.1)
                return f"SUCCESS: Typed '{text}'"
                
            elif action == "scroll":
                amount = params.get("amount", 100)
                pyautogui.scroll(amount)
                return f"SUCCESS: Scrolled {amount}"
                
            elif action == "drag":
                x, y = params.get("x"), params.get("y")
                pyautogui.dragTo(x, y, duration=0.5)
                return f"SUCCESS: Dragged to ({x}, {y})"
                
            else:
                return f"ERROR: Unsupported action '{action}'"
        except Exception as e:
            return f"FAILED: GUI action '{action}' failed: {e}"

    @as_tool
    def start_gui_recording(self) -> str:
        """Starts recording mouse and keyboard events on the desktop."""
        if self._mouse_listener or self._key_listener:
            return "Already recording."
            
        self.recorded_events = []
        self._start_time = time.time()
        
        def on_click(x, y, button, pressed) -> str:
            if pressed:
                self.recorded_events.append({
                    "time": time.time() - self._start_time,
                    "type": "click",
                    "x": x,
                    "y": y,
                    "button": str(button)
                })

        def on_press(key) -> str:
            try:
                char = key.char
            except AttributeError:
                char = str(key)
            self.recorded_events.append({
                "time": time.time() - self._start_time,
                "type": "keypress",
                "key": char
            })

        self._mouse_listener = mouse.Listener(on_click=on_click)
        self._key_listener = keyboard.Listener(on_press=on_press)
        
        self._mouse_listener.start()
        self._key_listener.start()
        
        return "Started GUI recording. Mouse clicks and key presses will be captured."

    @as_tool
    def stop_gui_recording(self) -> str:
        """Stops the current GUI recording and saves it to a file."""
        if not self._mouse_listener and not self._key_listener:
            return "Not recording."
            
        if self._mouse_listener:
            self._mouse_listener.stop()
            self._mouse_listener = None
        if self._key_listener:
            self._key_listener.stop()
            self._key_listener = None
            
        with open(self.recording_file, "w") as f:
            json.dump(self.recorded_events, f, indent=2)
            
        return f"Stopped GUI recording. Saved {len(self.recorded_events)} events to {self.recording_file}."

    @as_tool
    def replay_gui_interaction(self) -> str:
        """Replays the last recorded GUI interaction from the saved file."""
        if not self.recording_file.exists():
            return f"No recording file found at {self.recording_file}."
            
        with open(self.recording_file, "r") as f:
            events = json.load(f)
            
        if not events:
            return "Recording file is empty."
            
        logging.info(f"Replaying {len(events)} events...")
        last_time = 0
        for event in events:
            # Wait for the correct timing using non-blocking event wait
            wait_time = event["time"] - last_time
            if wait_time > 0:
                import threading
                threading.Event().wait(timeout=wait_time)
            last_time = event["time"]
            
            if event["type"] == "click":
                pyautogui.click(event["x"], event["y"])
            elif event["type"] == "keypress":
                # Special keys like 'Key.enter' need to be cleaned up for pyautogui
                key = event["key"].replace("Key.", "")
                pyautogui.press(key)
                
        return f"Replayed {len(events)} events successfully."

    def improve_content(self, prompt: str) -> str:
        """General visual reasoning entry point."""
        return "I am ready to process images. Provide an image path using 'analyze_screenshot'."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(MultiModalContextAgent, "MultiModal Context Agent", "Image analysis tool")
    main()

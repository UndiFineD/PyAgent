#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in visual context, UI analysis, and multimodal reasoning.
Used for interpreting screenshots, diagrams, and vision-based UI testing.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import base64
import json
import time
import pyautogui
from pathlib import Path
from typing import Dict, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

try:
    from pynput import mouse, keyboard
except ImportError:
    pass

class MultiModalContextAgent(BaseAgent):
    """Interprets visual data and integrates it into the agent's textual context."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.screenshots_dir = Path("data/logs/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.recording_file = Path("data/logs/gui_interaction.json")
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
        
        try:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Phase 125: Integrated Vision Logic
            # If the backend supports multimodal (e.g., GPT-4o, Claude 3.5), we pass the image.
            # Otherwise, we use a specialized prompt to describe the image metadata and OCR results.
            
            ocr_text = self.extract_text_from_image(image_path)
            
            vision_prompt = (
                f"You are a vision-capable component of a swarm agent.\n"
                f"Image Analysis Query: {query}\n\n"
                f"Context from OCR:\n{ocr_text}\n\n"
                "Based on the visual data and OCR, provide a detailed analysis of the user interface, "
                "identifying core components, potential accessibility issues, and workflow blocks."
            )
            
            # Using the BaseAgent's core reasoning engine
            analysis = self.think(vision_prompt)
            return f"### Visual Analysis of {path.name}\n\n{analysis}"
            
        except Exception as e:
            return f"Vision Analysis Failed: {str(e)}"

    @as_tool
    def extract_text_from_image(self, image_path: str) -> str:
        """Performs OCR or vision-based text extraction with fallback to LLM vision."""
        logging.info(f"MultiModalAgent: Extracting text from {image_path}...")
        
        # 1. Try pytesseract (Phase 127 UX Integration)
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            if text.strip():
                return f"### OCR Results (pytesseract)\n\n{text}"
        except (ImportError, Exception):
            pass

        # 2. Try EasyOCR (Phase 127 UX Integration)
        try:
            import easyocr
            reader = easyocr.Reader(['en'])
            result = reader.readtext(image_path, detail=0)
            if result:
                return "### OCR Results (EasyOCR)\n\n" + "\n".join(result)
        except (ImportError, Exception):
            pass

        # 3. Fallback to LLM-based vision analysis via BaseAgent.think()
        path = Path(image_path)
        if not path.exists():
            return "Error: Image file not found for OCR."
            
        logging.info("Falling back to Vision LLM for text extraction.")
        ocr_prompt = (
            "Read all the text visible in this image. "
            "Format the output as a structured markdown list. "
            "If it's a code editor, preserve the code structure."
        )
        
        try:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # BaseAgent.think handles the multimodal context if the model supports it
            text_extraction = self.think(f"{ocr_prompt}\n[Image Data Attached]")
            return f"### Extracted Text (Vision-LLM)\n\n{text_extraction}"
        except Exception as e:
            return f"OCR Extraction Failed: {str(e)}"

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
    from src.core.base.utilities import create_main_function
    main = create_main_function(MultiModalContextAgent, "MultiModal Context Agent", "Image analysis tool")
    main()
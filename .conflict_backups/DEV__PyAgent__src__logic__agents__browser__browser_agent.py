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


"""

Browser Agent - Web automation and information extraction

[Brief Summary]
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate BrowserAgent(headless=...) in an application or test, call setup_browser(), use navigate_to_url(url) and extract_text_content() for data extraction, call take_screenshot("desc") to capture visual state, and finish with cleanup_browser() to release resources.

WHAT IT DOES:
Provides a Playwright-backed agent for automated web browsing, navigation, screenshot capture, and basic page text extraction organized per-session with screenshot management and simple logging.

WHAT IT SHOULD DO BETTER:
- Add robust error handling and retries for navigation and evaluation failures, with configurable timeouts.
- Improve extraction to use heuristics (readability library or content scoring) and return structured outputs (title, main text, metadata, links).
- Expose async/await variants and support for persistent contexts, proxy/auth configuration, and more granular screenshot options (full page, clip, quality).
- Integrate safe shutdown hooks and better test coverage for edge cases (popups, redirects, infinite loads).

FILE CONTENT SUMMARY:
Browser Agent - Web automation and information extraction
========================================================

Inspired by big-3-super-agent's GeminiBrowserAgent.
Provides web browsing capabilities with screenshot capture and interaction.
"""

import time
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from playwright.sync_api import sync_playwright
from rich.console import Console

from src.core.base.base_agent import BaseAgent
from src.core.base.common.models.communication_models import CascadeContext



class BrowserAgent(BaseAgent):
    """
    Web browser automation agent inspired by big-3-super-agent.

    Features:
    - Playwright-based browser control
    - Screenshot capture and management
    - Web page interaction and data extraction
    - Session-based organization
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger("BrowserAgent")
        self.console = Console()

        # Browser state
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        # Screenshot management
        self.session_id = str(uuid.uuid4())[:8]
        self.screenshot_dir = Path("browser_screenshots") / self.session_id
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_counter = 0

        # Browser configuration
        self.screen_width = 1440
        self.screen_height = 900
        self.headless = kwargs.get("headless", True)  # Default to headless for server use

    def setup_browser(self):
        """Initialize Playwright browser."""
        try:
            self.logger.info("Initializing browser...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context(
                viewport={"width": self.screen_width, "height": self.screen_height}
            )
            self.page = self.context.new_page()
            self.logger.info(f"Browser ready! Session: {self.session_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            raise

    def cleanup_browser(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.logger.info("Browser cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Browser cleanup failed: {e}")

    def take_screenshot(self, description: str = "") -> str:
        """Take a screenshot and return the file path."""
        timestamp = datetime.now().strftime("%H%M%S")
        desc_suffix = f"_{description.replace(' ', '_')}" if description else ""
        screenshot_path = (
            self.screenshot_dir / f"screenshot_{self.screenshot_counter:03d}_{timestamp}{desc_suffix}.png"
        )

        try:
            self.page.screenshot(path=str(screenshot_path))
            self.screenshot_counter += 1
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""

    def navigate_to_url(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to a URL."""
        try:
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until=wait_until, timeout=30000)
            self.take_screenshot("navigation")
            return True
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            return False

    def extract_text_content(self) -> str:
        """Extract main text content from the current page."""
        try:
            # Get text from body, excluding scripts and styles
            text_content = self.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('body *');
                    let text = '';
                    for (let el of elements) {
                        if (el.tagName !== 'SCRIPT' && el.tagName !== 'STYLE' &&
                            el.offsetParent !== null && el.textConte
"""

import time
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from playwright.sync_api import sync_playwright
from rich.console import Console

from src.core.base.base_agent import BaseAgent
from src.core.base.common.models.communication_models import CascadeContext



class BrowserAgent(BaseAgent):
    """
    Web browser automation agent inspired by big-3-super-agent.

    Features:
    - Playwright-based browser control
    - Screenshot capture and management
    - Web page interaction and data extraction
    - Session-based organization
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger("BrowserAgent")
        self.console = Console()

        # Browser state
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        # Screenshot management
        self.session_id = str(uuid.uuid4())[:8]
        self.screenshot_dir = Path("browser_screenshots") / self.session_id
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_counter = 0

        # Browser configuration
        self.screen_width = 1440
        self.screen_height = 900
        self.headless = kwargs.get("headless", True)  # Default to headless for server use

    def setup_browser(self):
        """Initialize Playwright browser."""
        try:
            self.logger.info("Initializing browser...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context(
                viewport={"width": self.screen_width, "height": self.screen_height}
            )
            self.page = self.context.new_page()
            self.logger.info(f"Browser ready! Session: {self.session_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            raise

    def cleanup_browser(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.logger.info("Browser cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Browser cleanup failed: {e}")

    def take_screenshot(self, description: str = "") -> str:
        """Take a screenshot and return the file path."""
        timestamp = datetime.now().strftime("%H%M%S")
        desc_suffix = f"_{description.replace(' ', '_')}" if description else ""
        screenshot_path = (
            self.screenshot_dir / f"screenshot_{self.screenshot_counter:03d}_{timestamp}{desc_suffix}.png"
        )

        try:
            self.page.screenshot(path=str(screenshot_path))
            self.screenshot_counter += 1
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""

    def navigate_to_url(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to a URL."""
        try:
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until=wait_until, timeout=30000)
            self.take_screenshot("navigation")
            return True
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            return False

    def extract_text_content(self) -> str:
        """Extract main text content from the current page."""
        try:
            # Get text from body, excluding scripts and styles
            text_content = self.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('body *');
                    let text = '';
                    for (let el of elements) {
                        if (el.tagName !== 'SCRIPT' && el.tagName !== 'STYLE' &&
                            el.offsetParent !== null && el.textContent.trim()) {
                            text += el.textContent.trim() + ' ';
                        }
                    }
                    return text.replace(/\\s+/g, ' ').trim();
                }
            """)
            return text_content
        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return ""

    def search_on_page(self, query: str) -> Dict[str, Any]:
        """Search for text on the current page."""
        try:
            # Highlight search results
            result = self.page.evaluate("""
                (query) => {
                    const elements = document.querySelectorAll('*');
                    let matches = [];
                    const regex = new RegExp(query, 'gi');

                    for (let el of elements) {
                        if (el.offsetParent !== null && el.textContent) {
                            const text = el.textContent;
                            if (regex.test(text)) {
                                matches.push({
                                    text: text.trim(),
                                    tagName: el.tagName,
                                    className: el.className
                                });
                                // Highlight the element
                                el.style.backgroundColor = 'yellow';
                            }
                        }
                    }

                    return {
                        found: matches.length > 0,
                        count: matches.length,
                        matches: matches.slice(0, 10) // Limit results
                    };
                }
            """, query)

            if result["found"]:
                self.take_screenshot(f"search_{query.replace(' ', '_')}")

            return result
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return {"found": False, "error": str(e)}

    def click_element(self, selector: str) -> bool:
        """Click an element by CSS selector."""
        try:
            self.page.click(selector, timeout=5000)
            self.take_screenshot("click")
            return True
        except Exception as e:
            self.logger.error(f"Click failed for selector '{selector}': {e}")
            return False

    def fill_form(self, selector: str, value: str) -> bool:
        """Fill a form field by CSS selector."""
        try:
            self.page.fill(selector, value)
            self.take_screenshot("form_fill")
            return True
        except Exception as e:
            self.logger.error(f"Form fill failed for selector '{selector}': {e}")
            return False

    def scroll_page(self, direction: str = "down", amount: int = 500) -> bool:
        """Scroll the page."""
        try:
            if direction == "down":
                self.page.evaluate(f"window.scrollBy(0, {amount})")
            elif direction == "up":
                self.page.evaluate(f"window.scrollBy(0, -{amount})")
            elif direction == "top":
                self.page.evaluate("window.scrollTo(0, 0)")
            elif direction == "bottom":
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            time.sleep(0.5)  # Allow time for scroll to complete
            self.take_screenshot(f"scroll_{direction}")
            return True
        except Exception as e:
            self.logger.error(f"Scroll failed: {e}")
            return False

    async def execute(self, context: CascadeContext, **kwargs) -> Any:
        """
        Execute browser automation tasks.

        Args:
            url: Website URL to visit
            task: Description of what to do
            search_query: Text to search for on the page
            extract_text: Whether to extract text content
        """
        url = kwargs.get("url")
        # task = kwargs.get("task", "")  # Reserved for future reasoning integration
        search_query = kwargs.get("search_query")
        extract_text = kwargs.get("extract_text", False)

        # Initialize browser if not already done
        if not self.browser:
            self.setup_browser()

        results = {
            "session_id": self.session_id,
            "screenshots": [],
            "actions": []
        }

        try:
            # Navigate to URL if provided
            if url:
                if self.navigate_to_url(url):
                    results["actions"].append({"action": "navigate", "url": url, "success": True})
                    current_url = self.page.url
                    results["current_url"] = current_url
                else:
                    results["error"] = f"Failed to navigate to {url}"
                    return results

            # Search for text if requested
            if search_query:
                search_results = self.search_on_page(search_query)
                results["search_results"] = search_results
                results["actions"].append({
                    "action": "search",
                    "query": search_query,
                    "found": search_results.get("found", False)
                })

            # Extract text content if requested
            if extract_text:
                text_content = self.extract_text_content()
                results["text_content"] = text_content[:5000]  # Limit content length
                results["actions"].append({"action": "extract_text", "length": len(text_content)})

            # Take final screenshot
            final_screenshot = self.take_screenshot("final")
            results["screenshots"].append(final_screenshot)

            results["success"] = True
            results["message"] = f"Browser task completed. Session: {self.session_id}"

        except Exception as e:
            self.logger.error(f"Browser task failed: {e}")
            results["success"] = False
            results["error"] = str(e)

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get browser agent status."""
        return {
            "browser_active": self.browser is not None,
            "page_loaded": self.page is not None,
            "session_id": self.session_id,
            "screenshots_taken": self.screenshot_counter,
            "screenshot_dir": str(self.screenshot_dir),
            "current_url": self.page.url if self.page else None
        }

    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup_browser()

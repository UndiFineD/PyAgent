# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\agent.py\web.py\context.py\views_faa41799a660.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\agent\web\context\views.py

from dataclasses import dataclass, field

from typing import Optional

from playwright.async_api import BrowserContext as PlaywrightBrowserContext

from playwright.async_api import Page

from src.agent.web.dom.views import DOMState


@dataclass
class Tab:
    id: int

    url: str

    title: str

    page: Page

    def to_string(self) -> str:

        return f"{self.id} - Title: {self.title} - URL: {self.url}"


@dataclass
class BrowserState:
    current_tab: Optional[Tab] = None

    tabs: list[Tab] = field(default_factory=list)

    screenshot: Optional[str] = None

    dom_state: DOMState = field(default_factory=DOMState([]))

    def tabs_to_string(self) -> str:

        return "\n".join([tab.to_string() for tab in self.tabs])


@dataclass
class BrowserSession:
    context: PlaywrightBrowserContext

    current_page: Page

    state: BrowserState

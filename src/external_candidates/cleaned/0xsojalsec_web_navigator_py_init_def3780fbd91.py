# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_web_navigator.py\src.py\agent.py\web.py\history.py\init_def3780fbd91.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\agent\web\history\__init__.py

from hashlib import sha256

from src.agent.web.dom.views import DOMElementNode

from src.agent.web.history.views import DOMHistoryElementNode, HashElement


class History:
    def convert_dom_element_to_history_element(self, element: DOMElementNode) -> DOMHistoryElementNode:

        return DOMHistoryElementNode(**element.to_dict())

    def compare_dom_element_with_history_element(
        self, element: DOMElementNode, history_element: DOMHistoryElementNode
    ) -> bool:

        hash_dom_element = self.hash_element(element)

        hash_history_element = self.hash_element(history_element)

        return hash_dom_element == hash_history_element

    def hash_element(self, element: DOMElementNode | DOMHistoryElementNode):

        element: dict = element.to_dict()

        attributes = sha256(str(element.get("attributes")).encode()).hexdigest()

        xpath = sha256(str(element.get("xpath")).encode()).hexdigest()

        return HashElement(attributes=attributes, xpath=xpath)

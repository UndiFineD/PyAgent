"""Integration for component_1493."""
import pytest
from module import Component


class Test:
    def test_workflow(self):
        c = Component("t")
        assert c.state.component_id == "t"
        c.execute({"op": 1})

    def test_state(self):
        c = Component("t")
        c.state.status = "running"
        c.state.data = {"x": 1}
        d = c.state.to_dict()
        assert d["data"]["x"] == 1

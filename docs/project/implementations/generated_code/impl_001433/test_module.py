"""Unit tests for component_1433."""
import pytest
from module import Component


def test_init():
    c = Component("t")
    assert c.state.status == "initialized"

def test_exec():
    c = Component("t")
    r = c.execute({"a": "b"})
    assert r["result"] == "success"

def test_state():
    from module import ComponentState
    s = ComponentState("c1", "active")
    d = s.to_dict()
    assert d["id"] == "c1"

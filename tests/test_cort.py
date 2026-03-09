from context_manager import ContextManager
from cort import ChainOfThought

def test_cort_simple_branching():
    cm = ContextManager(max_tokens=10)
    cort = ChainOfThought(cm)
    root = cort.new_node("start")
    child = root.fork("step1")
    child.add("detail")
    assert "detail" in cm.snapshot()

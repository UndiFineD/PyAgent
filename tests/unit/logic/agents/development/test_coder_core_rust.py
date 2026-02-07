
import pytest
from src.logic.agents.development.coder_core import CoderCore
from src.core.base.common.types.code_language import CodeLanguage

def test_coder_core_rust_metrics():
    core = CoderCore(CodeLanguage.PYTHON)
    content = """def hello():
    # This is a comment
    if True:
        print('hi')
    import os
    """
    metrics = core.calculate_metrics(content)
    
    assert metrics.lines_of_code >= 3
    assert metrics.import_count >= 1
    assert metrics.cyclomatic_complexity >= 2
    
def test_coder_core_rust_dependencies():
    core = CoderCore(CodeLanguage.PYTHON)
    content = "import os\nfrom pathlib import Path\n"
    deps = core.get_dependencies(content)
    assert "os" in deps
    assert "pathlib" in deps

def test_coder_core_rust_smells():
    core = CoderCore(CodeLanguage.PYTHON)
    # A blocking sleep is an optimization pattern in rust_core
    content = "import time\ntime.sleep(10)\n"
    smells = core.detect_code_smells(content)
    
    perf_smells = [s for s in smells if s.category == "performance"]
    assert len(perf_smells) > 0
    assert "time.sleep" in perf_smells[0].description.lower() or "blocking" in perf_smells[0].description.lower()

def test_coder_core_quality_score():
    core = CoderCore(CodeLanguage.PYTHON)
    content = """def hello():
    # TODO: implement this
    pass
    """
    metrics = core.calculate_metrics(content)
    smells = core.detect_code_smells(content)
    score = core.calculate_quality_score(metrics, [], smells, 0.0, content=content)
    
    assert score.technical_debt < 100.0
    assert any("Tech Debt" in issue for issue in score.issues)

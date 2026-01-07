
import pytest
from pathlib import Path
import os
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from classes.improvements.ImprovementsAgent import ImprovementsAgent
from classes.improvements.ImprovementPriority import ImprovementPriority
from classes.improvements.ImprovementCategory import ImprovementCategory
from classes.improvements.ImprovementStatus import ImprovementStatus

def test_improvements_agent_round_trip(tmp_path):
    """Test that ImprovementsAgent can save and reload improvements correctly."""
    test_file = tmp_path / "test.improvements.md"
    agent = ImprovementsAgent(str(test_file))
    
    # Add improvements
    imp1 = agent.add_improvement(
        title="Fix bug 1",
        description="Priority high fix",
        priority=ImprovementPriority.HIGH,
        category=ImprovementCategory.SECURITY
    )
    
    imp2 = agent.add_improvement(
        title="Refactor core",
        description="Maintainability improvement\nWith multiple lines",
        priority=ImprovementPriority.MEDIUM,
        category=ImprovementCategory.MAINTAINABILITY
    )
    agent.update_status(imp2.id, ImprovementStatus.COMPLETED)
    
    # Save
    agent.save()
    
    # Create new agent and load
    agent2 = ImprovementsAgent(str(test_file))
    agent2.load()
    
    loaded = agent2.get_improvements()
    assert len(loaded) == 2
    
    # Verify imp1
    l1 = next(i for i in loaded if i.title == "Fix bug 1")
    assert l1.id == imp1.id
    assert l1.priority == ImprovementPriority.HIGH
    assert l1.category == ImprovementCategory.SECURITY
    assert l1.status == ImprovementStatus.PROPOSED
    assert l1.description == "Priority high fix"
    
    # Verify imp2
    l2 = next(i for i in loaded if i.title == "Refactor core")
    assert l2.id == imp2.id
    assert l2.priority == ImprovementPriority.MEDIUM
    assert l2.category == ImprovementCategory.MAINTAINABILITY
    assert l2.status == ImprovementStatus.COMPLETED
    assert "multiple lines" in l2.description

def test_improvements_agent_discovery(tmp_path, caplog):
    """Test that ImprovementsAgent can find associated code files."""
    # Create a code file in a 'src' directory
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    code_file = src_dir / "my_module.py"
    code_file.write_text("# code here")
    
    # Create improvements file in a 'docs' directory
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    imp_file = docs_dir / "my_module.improvements.md"
    
    # The agent should search adjacent and parent directories
    agent = ImprovementsAgent(str(imp_file))
    
    # Let's verify it finds it if we trigger it
    caplog.clear()
    agent._check_associated_file()
    assert "Could not find associated code file" not in caplog.text

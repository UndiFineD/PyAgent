"""Unit tests for KnowledgeGraph and KnowledgeAgent indexing."""
from typing import List
from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent
from pathlib import Path
import os
import logging

def test_knowledge_graph() -> None:
    logging.basicConfig(level=logging.INFO)
    # Create some dummy notes for testing links
    note1 = Path("Note1.md")
    note2 = Path("Note2.md")
    
    note1.write_text("# Note 1\nLink to [[Note2]]", encoding="utf-8")
    note2.write_text("# Note 2\nBacklink here", encoding="utf-8")
    
    ka = KnowledgeAgent(Path("."))
    ka.build_index()
    
    backlinks: List[str] = ka.find_backlinks("Note2.md")
    print(f"Backlinks for Note2: {backlinks}")
    assert "Note1.md" in backlinks
    
    mermaid: str = ka.get_graph_mermaid()
    print(f"Mermaid Graph:\n{mermaid}")
    assert "Note1 --> Note2" in mermaid
    
    # Cleanup
    note1.unlink()
    note2.unlink()
    if ka.index_file.exists():
        ka.index_file.unlink()

if __name__ == "__main__":
    try:
        test_knowledge_graph()
        print("\nKnowledgeAgent Graph/Backlinks Sanity Check: PASSED")
    except Exception as e:
        print(f"\nKnowledgeAgent Graph/Backlinks Sanity Check: FAILED: {e}")
        import traceback
        traceback.print_exc()

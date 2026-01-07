
import pytest
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from classes.context.SemanticSearchEngine import SemanticSearchEngine
from classes.context.SearchAlgorithm import SearchAlgorithm

def test_semantic_search_engine_integration():
    """Test that SemanticSearchEngine uses ChromaDB for semantic search."""
    engine = SemanticSearchEngine() # Memory-based by default
    
    # 1. Add documents
    engine.add_document("file1.py", "def calculate_risk(data): return data * 0.5")
    engine.add_document("file2.py", "def save_user_profile(user): pass # write to database")
    
    # 2. Test Keyword search
    engine.set_algorithm(SearchAlgorithm.KEYWORD)
    results = engine.search("risk")
    assert len(results) > 0
    assert results[0].file_path == "file1.py"
    
    # 3. Test Semantic search
    engine.set_algorithm(SearchAlgorithm.SEMANTIC)
    # "storing people's info" should match "save_user_profile"
    results = engine.search("storing people's info")
    assert len(results) > 0
    # Semantic similarity should favor file2.py
    assert results[0].file_path == "file2.py"
    assert results[0].similarity_score > 0

def test_semantic_search_clear():
    """Test that clearing the engine works."""
    engine = SemanticSearchEngine()
    engine.add_document("test.txt", "some content")
    assert len(engine.documents) == 1
    
    engine.clear()
    assert len(engine.documents) == 0
    results = engine.search("content", algorithm=SearchAlgorithm.SEMANTIC)
    assert len(results) == 0

#!/usr/bin/env python3
""
Minimal parser-safe tests for RAGCore.""
import importlib


def test_rag_core_importable():
    mod = importlib.import_module('src.core.base.logic.core.rag_core')
    assert hasattr(mod, 'RAGCore')


def test_rag_core_basic_instantiation():
    mod = importlib.import_module('src.core.base.logic.core.rag_core')
    core = mod.RAGCore()
    assert hasattr(core, 'register_vector_store')
    assert hasattr(core, 'create_rag_tool')

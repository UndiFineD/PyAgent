#!/usr/bin/env python3
""
Minimal parser-safe tests for E2EEncryptionCore.""
import importlib


def test_e2e_core_importable():
    mod = importlib.import_module('src.core.base.logic.security.e2e_encryption_core')
    assert hasattr(mod, 'E2EEncryptionCore')


def test_e2e_core_basic_usage(tmp_path):
    mod = importlib.import_module('src.core.base.logic.security.e2e_encryption_core')
    core = mod.E2EEncryptionCore(storage_path=tmp_path)
    assert hasattr(core, 'generate_identity_keypair')

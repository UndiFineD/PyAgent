#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

"""Sanity tests for module-level docstrings.

This test ensures that a prioritized list of modules flagged by the
self-improvement analyzer have non-empty module-level docstrings. This
helps achieve Phase parity for documentation and makes the project
more approachable for maintainers and auditors.
"""

from importlib import import_module

MODULES_TO_CHECK = [
    "src.core.lazy_loader",
    "src.core.base.common.base_utilities",
    "src.core.base.common.multimodal_logic",
    "src.core.base.common.utils.dynamic_importer",
    "src.core.base.common.utils.func_utils",
    "src.core.base.common.utils.math_utils",
    "src.core.base.lifecycle.agent_core",
    "src.core.base.lifecycle.agent_update_manager",
    "src.core.base.logic.core.cuda_stream_pool",
    "src.core.base.logic.core.micro_batch_context",
    "src.core.base.logic.structures.staged_batch_writer",
    "src.core.base.logic.structures.uva_buffer_pool",
    "src.infrastructure",
    "src.infrastructure.lazy",
    "src.infrastructure.engine.multimodal.encoder_cache_manager",
    "src.infrastructure.compute.backend.async_microbatcher",
    "src.infrastructure.compute.backend.llm_client",
    "src.infrastructure.engine.sampling.penalty_engine",
    "src.infrastructure.engine.sampling.rejection_sampler",
    "src.core.base.common.utils.jsontree.meta",
]


def test_modules_have_docstrings():
    missing = []
    for mod_name in MODULES_TO_CHECK:
        try:
            mod = import_module(mod_name)
        except Exception as e:  # pragma: no cover - import issues should be reported
            missing.append((mod_name, f"import_error: {e}"))
            continue
        doc = getattr(mod, "__doc__", None)
        if not doc or len(doc.strip()) < 30:
            missing.append((mod_name, "doc_missing_or_too_short"))

    assert not missing, f"Modules missing docstrings or import failures: {missing}"

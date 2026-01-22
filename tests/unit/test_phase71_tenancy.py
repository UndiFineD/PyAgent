#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import pytest
from src.infrastructure.engine.kv_cache.context_sharder import ContextShardManager

def test_tenant_isolation_gate():
    """Verifies that context shards are inaccessible to wrong tenants."""
    manager = ContextShardManager(block_size=512)
    
    # User Alpha creates a context
    manager.shard_context(
        context_id="context_101", 
        total_tokens=1024, 
        available_ranks=[0, 1],
        tenant_id="alpha"
    )
    
    # 1. Success case: Alpha accesses their own shard
    rank = manager.get_rank_for_token("context_101", 100, tenant_id="alpha")
    assert rank == 0
    
    # 2. Failure case: Beta tries to access Alpha's shard
    rank_beta = manager.get_rank_for_token("context_101", 100, tenant_id="beta")
    assert rank_beta is None
    
    print("\nPhase 71: Tenant context isolation verified.")

def test_cascade_context_tenant_propagation():
    """Verifies that tenant_id is preserved across agent delegation."""
    from src.core.base.common.models.communication_models import CascadeContext
    
    ctx = CascadeContext(tenant_id="enterprise_client_x", security_scope=["read:docs"])
    
    # Child context should inherit tenant and scope
    child_ctx = ctx.next_level(agent_id="agent_coder")
    
    assert child_ctx.tenant_id == "enterprise_client_x"
    assert "read:docs" in child_ctx.security_scope
    assert child_ctx.cascade_depth == 1
    
    print("Phase 71: Tenant propagation in CascadeContext verified.")

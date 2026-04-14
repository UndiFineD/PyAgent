#!/usr/bin/env python3
"""Vision module for PyAgent."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def get_template() -> str:
    """Return a markdown template for the PyAgent vision statement."""
    return """\
# Vision

**PyAgent** is an autonomous multi-agent swarm system designed to continuously
improve software quality, security, and developer productivity without human
intervention.

## Core Principles

1. **Autonomy** — agents discover, analyse, and fix issues without prompting.
2. **Safety** — every change goes through a `@8ql` security gate and `@9git`
   branch isolation before reaching `main`.
3. **Transparency** — all decisions are recorded in `docs/agents/*.memory.md`
   and project artifacts in `docs/project/prjNNNNNNN/`.
4. **Composability** — agents communicate via structured task lineage
   (`ContextTransaction`) and never bypass the registry.

## Strategic Goals

- Achieve 80 %+ test coverage across `src/` by end of Phase 5.
- Rust-accelerate the top-3 hot paths (metrics, file IO, complexity analysis).
- Ship a fully functional Fleet Load Balancer WebSocket backend.
- Integrate CodeQL scanning into every PR via the `@8ql` agent.

## Non-Goals

- Replace human architecture decisions.
- Run without a human-in-the-loop for production deployments.
"""

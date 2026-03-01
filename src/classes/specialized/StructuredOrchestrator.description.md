# StructuredOrchestrator

**File**: `src\classes\specialized\StructuredOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 206  
**Complexity**: 12 (moderate)

## Overview

Agent specializing in structured multi-agent orchestration patterns.
Supports Supervisor, Debate, Voting, Pipeline, and MapReduce patterns.
Inspired by multi-agent-generator and LangGraph.

## Classes (1)

### `PatternOrchestrator`

**Inherits from**: BaseAgent

Orchestrates multi-agent teams using battle-tested coordination patterns.
Phase 283: Implemented concrete orchestration with actual delegation calls.

**Methods** (12):
- `__init__(self, file_path)`
- `_determine_track_from_phase(self, phase)`
- `_apply_vibe_persona(self)`
- `set_vibe_track(self, track_name)`
- `get_track_guidance(self)`
- `orchestrate_supervisor(self, goal, specialists)`
- `orchestrate_debate(self, topic, pro_agent, con_agent)`
- `orchestrate_consensus_voting(self, task, solutions)`
- `orchestrate_pipeline(self, data, chain)`
- `orchestrate_mapreduce(self, file_path, chunk_size)`
- ... and 2 more methods

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `logging`
- `math`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.delegation.AgentDelegator`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.EVOLUTION_PHASE`
- `src.core.base.version.VERSION`
- `src.logic.cognitive.prompt_templates.VIBE_CODING_2025_TRACKS`
- `typing.List`

---
*Auto-generated documentation*

# VisualizerAgent

**File**: `src\classes\specialized\VisualizerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 247  
**Complexity**: 11 (moderate)

## Overview

Agent specializing in mapping and visualizing the internal dependencies of the Agent OS.
Inspired by system-design-visualizer and FalkorDB.

## Classes (1)

### `VisualizerAgent`

**Inherits from**: BaseAgent

Maps relationships and handles Visual Workflow Export/Import (cc-wf-studio pattern).

**Methods** (11):
- `__init__(self, file_path)`
- `spatial_reasoning(self, objects, query)`
- `video_grounding(self, frames, event_query)`
- `export_visual_workflow(self, workflow_name, tasks)`
- `import_visual_workflow(self, file_name)`
- `set_memory_agent(self, agent)`
- `visualize_knowledge_graph(self)`
- `generate_fleet_map(self)`
- `generate_call_graph(self, filter_term)`
- `generate_3d_swarm_data(self)`
- ... and 1 more methods

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.GraphMemoryAgent.GraphMemoryAgent`
- `src.logic.agents.cognitive.context.engines.GraphContextEngine.GraphContextEngine`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*

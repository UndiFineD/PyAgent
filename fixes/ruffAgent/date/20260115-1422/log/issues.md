## Issues found by ruffAgent at 20260115-1422

```
E402 Module level import not at top of file
  --> debug_registry.py:32:1
   |
32 | from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> debug_registry_v2.py:41:1
   |
41 | from src.infrastructure.fleet.AgentRegistry import LazyAgentMap
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
42 | from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap
   |

E402 Module level import not at top of file
  --> debug_registry_v2.py:42:1
   |
41 | from src.infrastructure.fleet.AgentRegistry import LazyAgentMap
42 | from src.infrastructure.fleet.OrchestratorRegistry import LazyOrchestratorMap
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> debug_registry_v3.py:39:1
   |
39 | from src.infrastructure.fleet.AgentRegistry import LazyAgentMap
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:276:45
    |
274 |                 from src.logic.agents.cognitive.context.engines.GlobalContextEngine import GlobalContextEngine
275 |                 self._local_global_context = GlobalContextEngine(self._workspace_root)
276 |             except (ImportError, ValueError): pass
    |                                             ^
277 |         return self._local_global_context
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:284:24
    |
283 |     def register_tools(self, registry: ToolRegistry) -> None:
284 |         if not registry: return
    |                        ^
285 |         for method, cat, prio in self.agent_logic_core.collect_tools(self):
286 |             # Fix: Correct order is (owner_name, func, category, priority)
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:363:43
    |
361 |                 loop.run_until_complete(coro)
362 |
363 |             if not self._is_stop_requested: self.update_file()
    |                                           ^
364 |             webhooks = getattr(self, '_webhooks', [])
365 |             for url in webhooks:
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:486:20
    |
484 |     async def run_subagent(self, description: str, prompt: str, original_content: str = "") -> str:
485 |         exceeded, reason = self.quotas.check_quotas()
486 |         if exceeded: raise CycleInterrupt(reason)
    |                    ^
487 |
488 |         try:
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:497:26
    |
495 |         self.quotas.update_usage(len(prompt)//4, len(result or "")//4 if result else 0)
496 |
497 |         if result is None: return original_content or self._get_fallback_response()
    |                          ^
498 |         return result
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:558:20
    |
556 |         """Saves a diff for verification without modifying the file."""
557 |         diff = self.get_diff()
558 |         if not diff: return True
    |                    ^
559 |
560 |         dry_run_dir = Path("temp/dry_runs")
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:699:41
    |
697 |     @classmethod
698 |     def register_hook(cls, event: EventType, callback: EventHook) -> None:
699 |         if event not in cls._event_hooks: cls._event_hooks[event] = []
    |                                         ^
700 |         cls._event_hooks[event].append(callback)
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\BaseAgent.py:711:25
    |
709 |             if hasattr(self, "recorder") and self.recorder:
710 |                 self.recorder.record_interaction(provider, model, prompt, result, meta)
711 |         except Exception: pass
    |                         ^
712 |
713 |     def _trigger_event(self, event: EventType, data: dict[str, Any]) -> None:
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\NeuralPruningEngine.py:104:31
    |
103 |         for i in range(n):
104 |             if labels[i] != -1: continue
    |                               ^
105 |
106 |             # Find neighbors
    |

E701 Multiple statements on one line (colon)
   --> src\core\base\NeuralPruningEngine.py:124:32
    |
122 |         res: dict[Any, Any] = {}
123 |         for i, label in enumerate(labels):
124 |             if label not in res: res[label] = []
    |                                ^
125 |             res[label].append(agents[i])
    |

F841 Local variable `processed_pairs` is assigned to but never used
   --> src\core\base\NeuralPruningEngine.py:167:9
    |
166 |         # Basic similarity check (heuristic: symbol overlap)
167 |         processed_pairs: set[Any] = set()
    |         ^^^^^^^^^^^^^^^
168 |         definitions = self._discover_definitions(search_root)
    |
help: Remove assignment to unused variable `processed_pairs`

F811 Redefinition of unused `right_to_be_forgotten` from line 108
   --> src\core\base\ShardedKnowledgeCore.py:160:15
    |
158 |         await self.create_index_snapshot()
159 |
160 |     async def right_to_be_forgotten(self, entity_name: str) -> bool:
    |               ^^^^^^^^^^^^^^^^^^^^^ `right_to_be_forgotten` redefined here
161 |         """
162 |         Removes an entity from the knowledge store across all shards
    |
   ::: src\core\base\ShardedKnowledgeCore.py:108:15
    |
106 |         return stable
107 |
108 |     async def right_to_be_forgotten(self, entity_name: str) -> bool:
    |               --------------------- previous definition of `right_to_be_forgotten` here
109 |         """
110 |         Phase 238: Prunes all knowledge associated with a specific entity (user/project)
    |
help: Remove definition: `right_to_be_forgotten`

F401 `.AgentPluginBase.AgentPluginBase` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\__init__.py:29:30
   |
27 | from .models import AgentConfig as AgentConfig, AgentState as AgentState, ResponseQuality as ResponseQuality, PromptTemplate as Prompt…
28 | from .interfaces import AgentInterface as AgentInterface, OrchestratorInterface as OrchestratorInterface
29 | from .AgentPluginBase import AgentPluginBase
   |                              ^^^^^^^^^^^^^^^
30 | from .models.enums import HealthStatus
   |
help: Use an explicit re-export: `AgentPluginBase as AgentPluginBase`

F401 `.models.enums.HealthStatus` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\__init__.py:30:27
   |
28 | from .interfaces import AgentInterface as AgentInterface, OrchestratorInterface as OrchestratorInterface
29 | from .AgentPluginBase import AgentPluginBase
30 | from .models.enums import HealthStatus
   |                           ^^^^^^^^^^^^
31 |
32 | __version__ = VERSION
   |
help: Use an explicit re-export: `HealthStatus as HealthStatus`

F401 [*] `typing.List` imported but unused
 --> src\core\base\core\AutonomyCore.py:3:20
  |
2 | from __future__ import annotations
3 | from typing import List
  |                    ^^^^
  |
help: Remove unused import: `typing.List`

F401 [*] `typing.Dict` imported but unused
  --> src\core\base\core\ErrorMappingCore.py:16:20
   |
15 | from __future__ import annotations
16 | from typing import Dict
   |                    ^^^^
   |
help: Remove unused import: `typing.Dict`

F841 Local variable `registry` is assigned to but never used
  --> src\core\base\delegation.py:63:9
   |
62 |         # Check registry for existing instance of this type to avoid redundant spawns
63 |         registry = AgentRegistry()
   |         ^^^^^^^^
64 |         type_clean = agent_type.replace("Agent", "").lower()
   |
help: Remove assignment to unused variable `registry`

F841 Local variable `type_clean` is assigned to but never used
  --> src\core\base\delegation.py:64:9
   |
62 |         # Check registry for existing instance of this type to avoid redundant spawns
63 |         registry = AgentRegistry()
64 |         type_clean = agent_type.replace("Agent", "").lower()
   |         ^^^^^^^^^^
65 |
66 |         if context.cascade_depth > 5:
   |
help: Remove assignment to unused variable `type_clean`

F401 `.base_models._empty_list_str` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:54:5
   |
52 |     DiffResult,
53 |     EventHook,
54 |     _empty_list_str,
   |     ^^^^^^^^^^^^^^^
55 |     _empty_list_int,
56 |     _empty_list_float,
   |
help: Add unused import `_empty_list_str` to __all__

F401 `.base_models._empty_list_int` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:55:5
   |
53 |     EventHook,
54 |     _empty_list_str,
55 |     _empty_list_int,
   |     ^^^^^^^^^^^^^^^
56 |     _empty_list_float,
57 |     _empty_list_dict_str_any,
   |
help: Add unused import `_empty_list_int` to __all__

F401 `.base_models._empty_list_float` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:56:5
   |
54 |     _empty_list_str,
55 |     _empty_list_int,
56 |     _empty_list_float,
   |     ^^^^^^^^^^^^^^^^^
57 |     _empty_list_dict_str_any,
58 |     _empty_dict_str_float,
   |
help: Add unused import `_empty_list_float` to __all__

F401 `.base_models._empty_list_dict_str_any` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:57:5
   |
55 |     _empty_list_int,
56 |     _empty_list_float,
57 |     _empty_list_dict_str_any,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
58 |     _empty_dict_str_float,
59 |     _empty_dict_str_any,
   |
help: Add unused import `_empty_list_dict_str_any` to __all__

F401 `.base_models._empty_dict_str_float` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:58:5
   |
56 |     _empty_list_float,
57 |     _empty_list_dict_str_any,
58 |     _empty_dict_str_float,
   |     ^^^^^^^^^^^^^^^^^^^^^
59 |     _empty_dict_str_any,
60 |     _empty_dict_str_int,
   |
help: Add unused import `_empty_dict_str_float` to __all__

F401 `.base_models._empty_dict_str_any` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:59:5
   |
57 |     _empty_list_dict_str_any,
58 |     _empty_dict_str_float,
59 |     _empty_dict_str_any,
   |     ^^^^^^^^^^^^^^^^^^^
60 |     _empty_dict_str_int,
61 |     _empty_dict_str_str,
   |
help: Add unused import `_empty_dict_str_any` to __all__

F401 `.base_models._empty_dict_str_int` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:60:5
   |
58 |     _empty_dict_str_float,
59 |     _empty_dict_str_any,
60 |     _empty_dict_str_int,
   |     ^^^^^^^^^^^^^^^^^^^
61 |     _empty_dict_str_str,
62 |     _empty_dict_str_callable_any_any,
   |
help: Add unused import `_empty_dict_str_int` to __all__

F401 `.base_models._empty_dict_str_str` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:61:5
   |
59 |     _empty_dict_str_any,
60 |     _empty_dict_str_int,
61 |     _empty_dict_str_str,
   |     ^^^^^^^^^^^^^^^^^^^
62 |     _empty_dict_str_callable_any_any,
63 |     _empty_dict_str_quality_criteria,
   |
help: Add unused import `_empty_dict_str_str` to __all__

F401 `.base_models._empty_dict_str_callable_any_any` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:62:5
   |
60 |     _empty_dict_str_int,
61 |     _empty_dict_str_str,
62 |     _empty_dict_str_callable_any_any,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
63 |     _empty_dict_str_quality_criteria,
64 |     _empty_dict_str_health_checks,
   |
help: Add unused import `_empty_dict_str_callable_any_any` to __all__

F401 `.base_models._empty_dict_str_quality_criteria` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:63:5
   |
61 |     _empty_dict_str_str,
62 |     _empty_dict_str_callable_any_any,
63 |     _empty_dict_str_quality_criteria,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
64 |     _empty_dict_str_health_checks,
65 |     _empty_dict_str_configprofile,
   |
help: Add unused import `_empty_dict_str_quality_criteria` to __all__

F401 `.base_models._empty_dict_str_health_checks` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:64:5
   |
62 |     _empty_dict_str_callable_any_any,
63 |     _empty_dict_str_quality_criteria,
64 |     _empty_dict_str_health_checks,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
65 |     _empty_dict_str_configprofile,
66 |     _empty_agent_event_handlers,
   |
help: Add unused import `_empty_dict_str_health_checks` to __all__

F401 `.base_models._empty_dict_str_configprofile` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:65:5
   |
63 |     _empty_dict_str_quality_criteria,
64 |     _empty_dict_str_health_checks,
65 |     _empty_dict_str_configprofile,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
66 |     _empty_agent_event_handlers,
67 |     _empty_routes_list,
   |
help: Add unused import `_empty_dict_str_configprofile` to __all__

F401 `.base_models._empty_agent_event_handlers` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:66:5
   |
64 |     _empty_dict_str_health_checks,
65 |     _empty_dict_str_configprofile,
66 |     _empty_agent_event_handlers,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
67 |     _empty_routes_list,
68 |     _empty_dict_str_filepriority,
   |
help: Add unused import `_empty_agent_event_handlers` to __all__

F401 `.base_models._empty_routes_list` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:67:5
   |
65 |     _empty_dict_str_configprofile,
66 |     _empty_agent_event_handlers,
67 |     _empty_routes_list,
   |     ^^^^^^^^^^^^^^^^^^
68 |     _empty_dict_str_filepriority,
69 |     _empty_dict_str_modelconfig
   |
help: Add unused import `_empty_routes_list` to __all__

F401 `.base_models._empty_dict_str_filepriority` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:68:5
   |
66 |     _empty_agent_event_handlers,
67 |     _empty_routes_list,
68 |     _empty_dict_str_filepriority,
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
69 |     _empty_dict_str_modelconfig
70 | )
   |
help: Add unused import `_empty_dict_str_filepriority` to __all__

F401 `.base_models._empty_dict_str_modelconfig` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
  --> src\core\base\models\__init__.py:69:5
   |
67 |     _empty_routes_list,
68 |     _empty_dict_str_filepriority,
69 |     _empty_dict_str_modelconfig
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
70 | )
   |
help: Add unused import `_empty_dict_str_modelconfig` to __all__

F821 Undefined name `sys`
   --> src\core\base\utils\DiffGenerator.py:139:17
    |
137 |         for line in diff_result.diff_lines:
138 |             if line.startswith('+') and not line.startswith('+++'):
139 |                 sys.stdout.write(f"\033[92m{line}\033[0m")  # Green
    |                 ^^^
140 |             elif line.startswith('-') and not line.startswith('---'):
141 |                 sys.stdout.write(f"\033[91m{line}\033[0m")  # Red
    |

F821 Undefined name `sys`
   --> src\core\base\utils\DiffGenerator.py:141:17
    |
139 |                 sys.stdout.write(f"\033[92m{line}\033[0m")  # Green
140 |             elif line.startswith('-') and not line.startswith('---'):
141 |                 sys.stdout.write(f"\033[91m{line}\033[0m")  # Red
    |                 ^^^
142 |             elif line.startswith('@@'):
143 |                 sys.stdout.write(f"\033[96m{line}\033[0m")  # Cyan
    |

F821 Undefined name `sys`
   --> src\core\base\utils\DiffGenerator.py:143:17
    |
141 |                 sys.stdout.write(f"\033[91m{line}\033[0m")  # Red
142 |             elif line.startswith('@@'):
143 |                 sys.stdout.write(f"\033[96m{line}\033[0m")  # Cyan
    |                 ^^^
144 |             else:
145 |                 sys.stdout.write(line)
    |

F821 Undefined name `sys`
   --> src\core\base\utils\DiffGenerator.py:145:17
    |
143 |                 sys.stdout.write(f"\033[96m{line}\033[0m")  # Cyan
144 |             else:
145 |                 sys.stdout.write(line)
    |                 ^^^
146 |         sys.stdout.flush()
    |

F821 Undefined name `sys`
   --> src\core\base\utils\DiffGenerator.py:146:9
    |
144 |             else:
145 |                 sys.stdout.write(line)
146 |         sys.stdout.flush()
    |         ^^^
    |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:35:1
   |
33 |     sys.path.insert(0, project_root)
34 |
35 | from src.core.base.version import VERSION
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
36 | import json
37 | import time
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:36:1
   |
35 | from src.core.base.version import VERSION
36 | import json
   | ^^^^^^^^^^^
37 | import time
38 | import logging
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:37:1
   |
35 | from src.core.base.version import VERSION
36 | import json
37 | import time
   | ^^^^^^^^^^^
38 | import logging
39 | import argparse
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:38:1
   |
36 | import json
37 | import time
38 | import logging
   | ^^^^^^^^^^^^^^
39 | import argparse
40 | import subprocess
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:39:1
   |
37 | import time
38 | import logging
39 | import argparse
   | ^^^^^^^^^^^^^^^
40 | import subprocess
41 | import re
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:40:1
   |
38 | import logging
39 | import argparse
40 | import subprocess
   | ^^^^^^^^^^^^^^^^^
41 | import re
42 | from pathlib import Path
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:41:1
   |
39 | import argparse
40 | import subprocess
41 | import re
   | ^^^^^^^^^
42 | from pathlib import Path
43 | from typing import Any
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:42:1
   |
40 | import subprocess
41 | import re
42 | from pathlib import Path
   | ^^^^^^^^^^^^^^^^^^^^^^^^
43 | from typing import Any
44 | from src.infrastructure.fleet.FleetManager import FleetManager
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:43:1
   |
41 | import re
42 | from pathlib import Path
43 | from typing import Any
   | ^^^^^^^^^^^^^^^^^^^^^^
44 | from src.infrastructure.fleet.FleetManager import FleetManager
45 | from src.observability.StructuredLogger import StructuredLogger
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:44:1
   |
42 | from pathlib import Path
43 | from typing import Any
44 | from src.infrastructure.fleet.FleetManager import FleetManager
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
45 | from src.observability.StructuredLogger import StructuredLogger
   |

E402 Module level import not at top of file
  --> src\infrastructure\dev\scripts\run_fleet_self_improvement.py:45:1
   |
43 | from typing import Any
44 | from src.infrastructure.fleet.FleetManager import FleetManager
45 | from src.observability.StructuredLogger import StructuredLogger
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
46 |
47 | # Phase 120: Load environment variables if available
   |

F821 Undefined name `loop`
   --> src\infrastructure\orchestration\ConsensusOrchestrator.py:128:24
    |
126 |                     # Agent critiques and improves its own proposal based on others
127 |                     coro = self.fleet.call_by_capability(f"{p['agent']}.refine", context=context)
128 |                     if loop.is_running():
    |                        ^^^^
129 |                         coro.close()
130 |                         refined = f"[DEFERRED] {p['agent']} refine"
    |

F821 Undefined name `loop`
   --> src\infrastructure\orchestration\ConsensusOrchestrator.py:132:35
    |
130 |                         refined = f"[DEFERRED] {p['agent']} refine"
131 |                     else:
132 |                         refined = loop.run_until_complete(coro)
    |                                   ^^^^
133 |
134 |                     new_proposals.append({
    |

F821 Undefined name `AsyncGenerator`
  --> src\infrastructure\orchestration\LockManager.py:66:106
   |
65 |     @asynccontextmanager
66 |     async def acquire_async(self, resource_id: str, lock_type: str = "memory", timeout: float = 10.0) -> AsyncGenerator[None, None]:
   |                                                                                                          ^^^^^^^^^^^^^^
67 |         """Phase 152: Async-native lock acquisition."""
68 |         if lock_type == "file":
   |

F821 Undefined name `Generator`
   --> src\infrastructure\orchestration\LockManager.py:133:94
    |
132 |     @contextmanager
133 |     def acquire(self, resource_id: str, lock_type: str = "memory", timeout: float = 10.0) -> Generator[None, None, None]:
    |                                                                                              ^^^^^^^^^
134 |         """Generic lock acquisition helper."""
135 |         if lock_type == "file":
    |

F841 Local variable `new_content` is assigned to but never used
   --> src\infrastructure\orchestration\core\SelfImprovementCore.py:139:9
    |
137 |         Applies non-AI assisted simple fixes.
138 |         """
139 |         new_content = content
    |         ^^^^^^^^^^^
140 |
141 |         if issue_type == "Robustness Issue":
    |
help: Remove assignment to unused variable `new_content`

F821 Undefined name `logging`
   --> src\logic\agents\cognitive\HierarchicalMemoryAgent.py:108:17
    |
106 |                     promoted_count += 1
107 |             except Exception as e:
108 |                 logging.error(f"Failed to promote {mem_file}: {e}")
    |                 ^^^^^^^
109 |
110 |         return f"Consolidation complete. Promoted {promoted_count} memory fragments."
    |

E701 Multiple statements on one line (colon)
   --> src\logic\agents\cognitive\KnowledgeAgent.py:110:34
    |
108 |             temp_path.replace(idx_path)
109 |         except Exception:
110 |             if temp_path.exists(): temp_path.unlink()
    |                                  ^
111 |             raise
    |

E701 Multiple statements on one line (colon)
   --> src\logic\agents\cognitive\VisualizerAgent.py:135:34
    |
133 |             temp_path.replace(output_path)
134 |         except Exception:
135 |             if temp_path.exists(): temp_path.unlink()
    |                                  ^
136 |             raise
    |

F401 `src.logic.agents.compliance.core.ComplianceCore.ComplianceIssue` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> src\logic\agents\compliance\ComplianceAgent.py:9:81
   |
 7 | # Ensure relative or absolute import matches structure
 8 | try:
 9 |     from src.logic.agents.compliance.core.ComplianceCore import ComplianceCore, ComplianceIssue
   |                                                                                 ^^^^^^^^^^^^^^^
10 | except ImportError:
11 |     # If core doesn't exist yet, we might need to mock or it is in a different place
   |
help: Remove unused import: `src.logic.agents.compliance.core.ComplianceCore.ComplianceIssue`

F821 Undefined name `all_issues`
  --> src\logic\agents\compliance\ComplianceAgent.py:41:13
   |
39 |         for path, content in file_map.items():
40 |             issues = self.core.audit_content(content, path)
41 |             all_issues.extend(issues)
   |             ^^^^^^^^^^
42 |
43 |         score = self.core.aggregate_score(all_issues)
   |

F821 Undefined name `all_issues`
  --> src\logic\agents\compliance\ComplianceAgent.py:43:43
   |
41 |             all_issues.extend(issues)
42 |
43 |         score = self.core.aggregate_score(all_issues)
   |                                           ^^^^^^^^^^
44 |
45 |         report = {
   |

F821 Undefined name `all_issues`
  --> src\logic\agents\compliance\ComplianceAgent.py:47:32
   |
45 |         report = {
46 |             "score": score,
47 |             "issue_count": len(all_issues),
   |                                ^^^^^^^^^^
48 |             "critical_violations": [i.message for i in all_issues if i.severity == "CRITICAL"],
49 |             "status": "PASS" if score > 0.8 else "FAIL"
   |

F821 Undefined name `all_issues`
  --> src\logic\agents\compliance\ComplianceAgent.py:48:56
   |
46 |             "score": score,
47 |             "issue_count": len(all_issues),
48 |             "critical_violations": [i.message for i in all_issues if i.severity == "CRITICAL"],
   |                                                        ^^^^^^^^^^
49 |             "status": "PASS" if score > 0.8 else "FAIL"
50 |         }
   |

F821 Undefined name `time`
   --> src\logic\agents\swarm\FleetDeployerAgent.py:123:26
    |
121 |             "type": agent_type,
122 |             "status": "provisioning",
123 |             "timestamp": time.time() if 'time' in globals() else 0
    |                          ^^^^
124 |         }
    |

E701 Multiple statements on one line (colon)
  --> src\logic\agents\swarm\SwarmArbitratorAgent.py:88:24
   |
87 |     def _update_reputation(self, agent_id: str, delta: float) -> None:
88 |         if not agent_id: return
   |                        ^
89 |         self.reputation_scores[agent_id] = self.reputation_scores.get(agent_id, 1.0) + delta
90 |         # Clamp between 0.0 (Malicious/Incompetent) and 2.0 (Highly Trusted)
   |

F401 `typing.Optional` imported but unused
  --> src\logic\strategies\__init__.py:24:20
   |
22 | from __future__ import annotations
23 | from src.core.base.version import VERSION as VERSION
24 | from typing import Optional, List, Dict
   |                    ^^^^^^^^
25 | from collections.abc import Callable
26 | from .AgentStrategy import AgentStrategy as AgentStrategy
   |
help: Remove unused import

F401 `typing.List` imported but unused
  --> src\logic\strategies\__init__.py:24:30
   |
22 | from __future__ import annotations
23 | from src.core.base.version import VERSION as VERSION
24 | from typing import Optional, List, Dict
   |                              ^^^^
25 | from collections.abc import Callable
26 | from .AgentStrategy import AgentStrategy as AgentStrategy
   |
help: Remove unused import

F401 `typing.Dict` imported but unused
  --> src\logic\strategies\__init__.py:24:36
   |
22 | from __future__ import annotations
23 | from src.core.base.version import VERSION as VERSION
24 | from typing import Optional, List, Dict
   |                                    ^^^^
25 | from collections.abc import Callable
26 | from .AgentStrategy import AgentStrategy as AgentStrategy
   |
help: Remove unused import

F401 [*] `os` imported but unused
 --> src\maintenance\agents.py:1:8
  |
1 | import os
  |        ^^
2 | import json
3 | import asyncio
  |
help: Remove unused import: `os`

F401 [*] `json` imported but unused
 --> src\maintenance\agents.py:2:8
  |
1 | import os
2 | import json
  |        ^^^^
3 | import asyncio
4 | import sys
  |
help: Remove unused import: `json`

F401 [*] `pathlib.Path` imported but unused
 --> src\maintenance\agents.py:5:21
  |
3 | import asyncio
4 | import sys
5 | from pathlib import Path
  |                     ^^^^
6 | from typing import List, Dict, Any, Annotated
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import: `pathlib.Path`

F401 [*] `typing.List` imported but unused
 --> src\maintenance\agents.py:6:20
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                    ^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Dict` imported but unused
 --> src\maintenance\agents.py:6:26
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                          ^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Any` imported but unused
 --> src\maintenance\agents.py:6:32
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                                ^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `typing.Annotated` imported but unused
 --> src\maintenance\agents.py:6:37
  |
4 | import sys
5 | from pathlib import Path
6 | from typing import List, Dict, Any, Annotated
  |                                     ^^^^^^^^^
7 | from .utils import setup_fix_directory, run_command, GitManager, get_timestamp
  |
help: Remove unused import

F401 [*] `sys` imported but unused
 --> src\maintenance\orchestrator.py:2:8
  |
1 | import asyncio
2 | import sys
  |        ^^^
3 | from .utils import GitManager, get_timestamp
4 | from .agents import PytestAgent, MypyAgent, RuffAgent, Flake8Agent, UnittestAgent
  |
help: Remove unused import: `sys`

F541 [*] f-string without any placeholders
  --> src\maintenance\orchestrator.py:35:19
   |
33 |             print("\n--- Some maintenance tasks failed. ---")
34 |             # In a real run, we would interact or log more
35 |             print(f"Check the 'fixes/' directory for logs.")
   |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
36 |
37 | if __name__ == "__main__":
   |
help: Remove extraneous `f` prefix

F821 Undefined name `total`
   --> src\observability\improvements\ImprovementManager.py:255:16
    |
253 |             created_at=datetime.now().isoformat()
254 |         )
255 |         return total
    |                ^^^^^
256 |
257 |     def export_markdown(self) -> str:
    |

F811 Redefinition of unused `calculate` from line 257
   --> src\observability\stats\MetricsCore.py:306:9
    |
304 |         return metric
305 |
306 |     def calculate(self, name: str, context: dict[str, float]) -> float:
    |         ^^^^^^^^^ `calculate` redefined here
307 |         if name not in self.derived_metrics:
308 |             return 0.0
    |
   ::: src\observability\stats\MetricsCore.py:257:9
    |
255 |             raise TypeError(f"Unsupported operation: {type(node)}")
256 |
257 |     def calculate(self, metric_name: str, context: dict[str, float]) -> float:
    |         --------- previous definition of `calculate` here
258 |         """Calculate derived metric value."""
259 |         if metric_name not in self.derived_metrics:
    |
help: Remove definition: `calculate`

E701 Multiple statements on one line (colon)
  --> src\observability\stats\ab_engine.py:74:20
   |
72 |     def add_metric(self, comparison_id: str, version: str, metric_name: str, value: float) -> bool:
73 |         comp = self.comparisons.get(comparison_id)
74 |         if not comp: return False
   |                    ^
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\ab_engine.py:97:26
   |
95 |             target = comp.metrics_b
96 |
97 |         if target is None: return False
   |                          ^
98 |
99 |         target[metric_name] = value
   |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:105:20
    |
103 |         """Get summary of comparison."""
104 |         comp = self.comparisons.get(comparison_id)
105 |         if not comp: return None
    |                    ^
106 |         return {
107 |             "id": comp.id,
    |

F821 Undefined name `version`
   --> src\observability\stats\ab_engine.py:119:12
    |
117 |             "metrics_count": len(comp.metrics_a) + len(comp.metrics_b)
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
    |            ^^^^^^^
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
121 |         else: return False
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:119:34
    |
117 |             "metrics_count": len(comp.metrics_a) + len(comp.metrics_b)
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
    |                                  ^
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
121 |         else: return False
    |

F821 Undefined name `metric_name`
   --> src\observability\stats\ab_engine.py:119:51
    |
117 |             "metrics_count": len(comp.metrics_a) + len(comp.metrics_b)
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
    |                                                   ^^^^^^^^^^^
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
121 |         else: return False
    |

F821 Undefined name `value`
   --> src\observability\stats\ab_engine.py:119:66
    |
117 |             "metrics_count": len(comp.metrics_a) + len(comp.metrics_b)
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
    |                                                                  ^^^^^
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
121 |         else: return False
    |

F821 Undefined name `version`
   --> src\observability\stats\ab_engine.py:120:14
    |
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
    |              ^^^^^^^
121 |         else: return False
122 |         return True
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:120:36
    |
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
    |                                    ^
121 |         else: return False
122 |         return True
    |

F821 Undefined name `metric_name`
   --> src\observability\stats\ab_engine.py:120:53
    |
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
    |                                                     ^^^^^^^^^^^
121 |         else: return False
122 |         return True
    |

F821 Undefined name `value`
   --> src\observability\stats\ab_engine.py:120:68
    |
118 |         }
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
    |                                                                    ^^^^^
121 |         else: return False
122 |         return True
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:121:13
    |
119 |         if version.lower() == "a": comp.metrics_a[metric_name] = value
120 |         elif version.lower() == "b": comp.metrics_b[metric_name] = value
121 |         else: return False
    |             ^
122 |         return True
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:126:20
    |
124 |     def calculate_winner(self, comparison_id: str, metric_name: str, higher_is_better: bool = True) -> dict[str, Any]:
125 |         comp = self.comparisons.get(comparison_id)
126 |         if not comp: return {"error": "Comparison not found"}
    |                    ^
127 |         val_a, val_b = comp.metrics_a.get(metric_name, 0), comp.metrics_b.get(metric_name, 0)
128 |         if val_a == val_b: winner = "tie"
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:128:26
    |
126 |         if not comp: return {"error": "Comparison not found"}
127 |         val_a, val_b = comp.metrics_a.get(metric_name, 0), comp.metrics_b.get(metric_name, 0)
128 |         if val_a == val_b: winner = "tie"
    |                          ^
129 |         elif higher_is_better: winner = "a" if val_a > val_b else "b"
130 |         else: winner = "a" if val_a < val_b else "b"
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:129:30
    |
127 |         val_a, val_b = comp.metrics_a.get(metric_name, 0), comp.metrics_b.get(metric_name, 0)
128 |         if val_a == val_b: winner = "tie"
129 |         elif higher_is_better: winner = "a" if val_a > val_b else "b"
    |                              ^
130 |         else: winner = "a" if val_a < val_b else "b"
131 |         improvement = abs(val_b - val_a) / val_a * 100 if val_a != 0 else 0
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\ab_engine.py:130:13
    |
128 |         if val_a == val_b: winner = "tie"
129 |         elif higher_is_better: winner = "a" if val_a > val_b else "b"
130 |         else: winner = "a" if val_a < val_b else "b"
    |             ^
131 |         improvement = abs(val_b - val_a) / val_a * 100 if val_a != 0 else 0
132 |         return {"metric": metric_name, "version_a": val_a, "version_b": val_b, "winner": winner, "improvement_percent": improvement}
    |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\access.py:20:40
   |
19 |     def can_access(self, user: str, resource: str, required_level: str = "read") -> bool:
20 |         if user not in self.permissions: return False
   |                                        ^
21 |         req = required_level.lower()
22 |         for pat, granted in self.permissions[user].items():
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\access.py:25:60
   |
23 |             if fnmatch.fnmatch(resource, pat):
24 |                 g = granted.lower()
25 |                 if req == "read" and g in ("read", "write"): return True
   |                                                            ^
26 |                 if req == "write" and g == "write": return True
27 |         return False
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\access.py:26:51
   |
24 |                 g = granted.lower()
25 |                 if req == "read" and g in ("read", "write"): return True
26 |                 if req == "write" and g == "write": return True
   |                                                   ^
27 |         return False
   |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\alerting.py:106:29
    |
104 |         actual_ts = timestamp if timestamp is not None else ts
105 |         actual_val = value if value is not None else val
106 |         if actual_ts is None: actual_ts = datetime.now().timestamp()
    |                             ^
107 |
108 |         if name not in self.data:
    |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\api.py:50:53
   |
48 |     def handle_request(self, path: str, method: str = "GET", params: dict[str, Any] | None = None) -> dict[str, Any]:
49 |         endpoint = self.endpoints.get(path)
50 |         if not endpoint or endpoint.method != method: return {"error": "Not Found", "status": 404}
   |                                                     ^
51 |         if path == "/api / stats" and self.stats_agent: return {"data": self.stats_agent.calculate_stats(), "status": 200}
52 |         return {"data": {}, "status": 200}
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\api.py:51:55
   |
49 |         endpoint = self.endpoints.get(path)
50 |         if not endpoint or endpoint.method != method: return {"error": "Not Found", "status": 404}
51 |         if path == "/api / stats" and self.stats_agent: return {"data": self.stats_agent.calculate_stats(), "status": 200}
   |                                                       ^
52 |         return {"data": {}, "status": 200}
   |

F401 `.ProfilingCore.ProfilingCore` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
 --> src\observability\stats\core\__init__.py:2:28
  |
2 | from .ProfilingCore import ProfilingCore, ProfileStats
  |                            ^^^^^^^^^^^^^
3 | from .StabilityCore import StabilityCore, FleetMetrics
4 | from .TracingCore import TracingCore
  |
help: Use an explicit re-export: `ProfilingCore as ProfilingCore`

F401 `.ProfilingCore.ProfileStats` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
 --> src\observability\stats\core\__init__.py:2:43
  |
2 | from .ProfilingCore import ProfilingCore, ProfileStats
  |                                           ^^^^^^^^^^^^
3 | from .StabilityCore import StabilityCore, FleetMetrics
4 | from .TracingCore import TracingCore
  |
help: Use an explicit re-export: `ProfileStats as ProfileStats`

F401 `.StabilityCore.StabilityCore` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
 --> src\observability\stats\core\__init__.py:3:28
  |
2 | from .ProfilingCore import ProfilingCore, ProfileStats
3 | from .StabilityCore import StabilityCore, FleetMetrics
  |                            ^^^^^^^^^^^^^
4 | from .TracingCore import TracingCore
  |
help: Use an explicit re-export: `StabilityCore as StabilityCore`

F401 `.StabilityCore.FleetMetrics` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
 --> src\observability\stats\core\__init__.py:3:43
  |
2 | from .ProfilingCore import ProfilingCore, ProfileStats
3 | from .StabilityCore import StabilityCore, FleetMetrics
  |                                           ^^^^^^^^^^^^
4 | from .TracingCore import TracingCore
  |
help: Use an explicit re-export: `FleetMetrics as FleetMetrics`

F401 `.TracingCore.TracingCore` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
 --> src\observability\stats\core\__init__.py:4:26
  |
2 | from .ProfilingCore import ProfilingCore, ProfileStats
3 | from .StabilityCore import StabilityCore, FleetMetrics
4 | from .TracingCore import TracingCore
  |                          ^^^^^^^^^^^
  |
help: Use an explicit re-export: `TracingCore as TracingCore`

F401 `opentelemetry.sdk.trace.export.BatchSpanProcessor` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> src\observability\stats\exporters\OTelManager.py:39:9
   |
37 |     from opentelemetry.sdk.trace import TracerProvider
38 |     from opentelemetry.sdk.trace.export import (
39 |         BatchSpanProcessor,
   |         ^^^^^^^^^^^^^^^^^^
40 |         ConsoleSpanExporter,
41 |     )
   |
help: Remove unused import

F401 `opentelemetry.sdk.trace.export.ConsoleSpanExporter` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> src\observability\stats\exporters\OTelManager.py:40:9
   |
38 |     from opentelemetry.sdk.trace.export import (
39 |         BatchSpanProcessor,
40 |         ConsoleSpanExporter,
   |         ^^^^^^^^^^^^^^^^^^^
41 |     )
42 |     from opentelemetry.sdk.resources import Resource
   |
help: Remove unused import

F841 Local variable `total_latency` is assigned to but never used
   --> src\observability\stats\exporters\OTelManager.py:147:13
    |
145 |                 raw_span.attributes.update(attributes)
146 |
147 |             total_latency = raw_span.end_time - raw_span.start_time
    |             ^^^^^^^^^^^^^
148 |             # ... existing logic for completed_spans could go here if needed for export_spans()
149 |             self.completed_spans.append(raw_span)
    |
help: Remove assignment to unused variable `total_latency`

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:31:16
   |
29 |         self.sources[name] = source
30 |         self._last_sync[name] = datetime.min
31 |         if data: source.metrics.update({k: float(v) for k, v in data.items()})
   |                ^
32 |
33 |     def remove_source(self, name: str) -> bool:
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:40:70
   |
39 |     def sync_source(self, name: str) -> dict[str, float]:
40 |         if name not in self.sources or not self.sources[name].enabled: return {}
   |                                                                      ^
41 |         source = self.sources[name]
42 |         if source.api_endpoint.startswith(("http", "https")):
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:70:50
   |
68 |         total = 0.0
69 |         if values:
70 |             if aggregation == AggregationType.SUM: total = float(sum(values))
   |                                                  ^
71 |             elif aggregation == AggregationType.AVG: total = float(sum(values) / len(values))
72 |             elif aggregation == AggregationType.MIN: total = float(min(values))
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:71:52
   |
69 |         if values:
70 |             if aggregation == AggregationType.SUM: total = float(sum(values))
71 |             elif aggregation == AggregationType.AVG: total = float(sum(values) / len(values))
   |                                                    ^
72 |             elif aggregation == AggregationType.MIN: total = float(min(values))
73 |             elif aggregation == AggregationType.MAX: total = float(max(values))
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:72:52
   |
70 |             if aggregation == AggregationType.SUM: total = float(sum(values))
71 |             elif aggregation == AggregationType.AVG: total = float(sum(values) / len(values))
72 |             elif aggregation == AggregationType.MIN: total = float(min(values))
   |                                                    ^
73 |             elif aggregation == AggregationType.MAX: total = float(max(values))
74 |             elif aggregation == AggregationType.COUNT: total = float(len(values))
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:73:52
   |
71 |             elif aggregation == AggregationType.AVG: total = float(sum(values) / len(values))
72 |             elif aggregation == AggregationType.MIN: total = float(min(values))
73 |             elif aggregation == AggregationType.MAX: total = float(max(values))
   |                                                    ^
74 |             elif aggregation == AggregationType.COUNT: total = float(len(values))
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\federation.py:74:54
   |
72 |             elif aggregation == AggregationType.MIN: total = float(min(values))
73 |             elif aggregation == AggregationType.MAX: total = float(max(values))
74 |             elif aggregation == AggregationType.COUNT: total = float(len(values))
   |                                                      ^
75 |
76 |         return AggregationResult(total, total=total, failed_sources=failed, source_count=len(values), metric_name=metric_name)
   |

F401 [*] `typing.Dict` imported but unused
  --> src\observability\stats\metrics_engine.py:16:20
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                    ^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `typing.List` imported but unused
  --> src\observability\stats\metrics_engine.py:16:26
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                          ^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `typing.Optional` imported but unused
  --> src\observability\stats\metrics_engine.py:16:37
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                                     ^^^^^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `typing.Tuple` imported but unused
  --> src\observability\stats\metrics_engine.py:16:47
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                                               ^^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `typing.Union` imported but unused
  --> src\observability\stats\metrics_engine.py:16:54
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                                                      ^^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `typing.Type` imported but unused
  --> src\observability\stats\metrics_engine.py:16:61
   |
14 | from datetime import datetime
15 | from dataclasses import dataclass, field, asdict
16 | from typing import Dict, List, Any, Optional, Tuple, Union, Type
   |                                                             ^^^^
17 | from collections.abc import Callable
18 | from pathlib import Path
   |
help: Remove unused import

F401 [*] `.MetricsCore.CorrelationCore` imported but unused
  --> src\observability\stats\metrics_engine.py:46:5
   |
44 |     DerivedMetricCalculator,
45 |     StatsRollupCore,
46 |     CorrelationCore,
   |     ^^^^^^^^^^^^^^^
47 |     ABTestCore,
48 | )
   |
help: Remove unused import

F401 [*] `.MetricsCore.ABTestCore` imported but unused
  --> src\observability\stats\metrics_engine.py:47:5
   |
45 |     StatsRollupCore,
46 |     CorrelationCore,
47 |     ABTestCore,
   |     ^^^^^^^^^^
48 | )
49 | try:
   |
help: Remove unused import

F401 [*] `.analysis.MODEL_COSTS` imported but unused
  --> src\observability\stats\metrics_engine.py:53:27
   |
51 |     import psutil
52 | except ImportError:
53 |     from .analysis import MODEL_COSTS, HAS_PSUTIL
   |                           ^^^^^^^^^^^
54 |     psutil = None
55 | from .exporters import PrometheusExporter, OTelManager, MetricsExporter
   |
help: Remove unused import: `.analysis.MODEL_COSTS`

F811 Redefinition of unused `DerivedMetricCalculator` from line 44
   --> src\observability\stats\metrics_engine.py:284:7
    |
284 | class DerivedMetricCalculator:
    |       ^^^^^^^^^^^^^^^^^^^^^^^ `DerivedMetricCalculator` redefined here
285 |     """Calculate derived metrics from dependencies using safe AST evaluation."""
    |
   ::: src\observability\stats\metrics_engine.py:44:5
    |
 42 |     TokenCostCore,
 43 |     ModelFallbackCore,
 44 |     DerivedMetricCalculator,
    |     ----------------------- previous definition of `DerivedMetricCalculator` here
 45 |     StatsRollupCore,
 46 |     CorrelationCore,
    |
help: Remove definition: `DerivedMetricCalculator`

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:30:26
   |
28 |     def get_current_stats(self) -> dict[str, Any]:
29 |         stats = {"platform": platform.platform(), "cpu_usage_pct": 0, "memory_usage_pct": 0, "disk_free_gb": 0, "status": "UNAVAILABLE…
30 |         if not HAS_PSUTIL: return stats
   |                          ^
31 |         try:
32 |             stats["cpu_usage_pct"] = psutil.cpu_percent(interval=None)
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:36:77
   |
34 |             disk = psutil.disk_usage(str(self.workspace_root))
35 |             stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
36 |             if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90: stats["status"] = "CRITICAL"
   |                                                                             ^
37 |             elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70: stats["status"] = "WARNING"
38 |             else: stats["status"] = "HEALTHY"
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:37:79
   |
35 |             stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
36 |             if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90: stats["status"] = "CRITICAL"
37 |             elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70: stats["status"] = "WARNING"
   |                                                                               ^
38 |             else: stats["status"] = "HEALTHY"
39 |         except Exception as e:
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:38:17
   |
36 |             if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90: stats["status"] = "CRITICAL"
37 |             elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70: stats["status"] = "WARNING"
38 |             else: stats["status"] = "HEALTHY"
   |                 ^
39 |         except Exception as e:
40 |             logger.error(f"Failed to gather resource stats: {e}")
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:47:41
   |
45 |         stats = self.get_current_stats()
46 |         mult = 1.0
47 |         if stats["status"] == "CRITICAL": mult = 3.0
   |                                         ^
48 |         elif stats["status"] == "WARNING": mult = 1.5
49 |         return mult
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\monitoring.py:48:42
   |
46 |         mult = 1.0
47 |         if stats["status"] == "CRITICAL": mult = 3.0
48 |         elif stats["status"] == "WARNING": mult = 1.5
   |                                          ^
49 |         return mult
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\namespaces.py:19:52
   |
18 |     def create_namespace(self, name: str, description: str = "", parent: str | None = None, tags: dict[str, str] | None = None) -> Met…
19 |         if parent and parent not in self.namespaces: raise ValueError("Parent missing")
   |                                                    ^
20 |         ns = MetricNamespace(name=name, description=description, parent=parent, tags=tags or {})
21 |         self.namespaces[name] = ns
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\namespaces.py:33:44
   |
32 |     def assign_metric(self, metric_name: str, namespace: str) -> bool:
33 |         if namespace not in self.namespaces: return False
   |                                            ^
34 |         if metric_name not in self.metrics_by_namespace[namespace]:
35 |             self.metrics_by_namespace[namespace].append(metric_name)
   |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\storage_engine.py:195:23
    |
193 |         payload = zlib.decompress(data)
194 |         tag, body = payload[:1], payload[1:]
195 |         if tag == b"b": return body
    |                       ^
196 |         if tag == b"j": return json.loads(body.decode("utf-8"))
197 |         try: return json.loads(payload.decode("utf-8"))
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\storage_engine.py:196:23
    |
194 |         tag, body = payload[:1], payload[1:]
195 |         if tag == b"b": return body
196 |         if tag == b"j": return json.loads(body.decode("utf-8"))
    |                       ^
197 |         try: return json.loads(payload.decode("utf-8"))
198 |         except Exception: return payload
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\storage_engine.py:197:12
    |
195 |         if tag == b"b": return body
196 |         if tag == b"j": return json.loads(body.decode("utf-8"))
197 |         try: return json.loads(payload.decode("utf-8"))
    |            ^
198 |         except Exception: return payload
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\storage_engine.py:198:25
    |
196 |         if tag == b"j": return json.loads(body.decode("utf-8"))
197 |         try: return json.loads(payload.decode("utf-8"))
198 |         except Exception: return payload
    |                         ^
    |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\streaming.py:35:47
   |
33 |     def add_data(self, data: Any) -> None:
34 |         self.buffer.append(data)
35 |         if len(self.buffer) > self.buffer_size: self.buffer.pop(0)
   |                                               ^
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\streaming.py:60:32
   |
59 |     def publish(self, name: str, data: Any) -> None:
60 |         if name in self.streams: self.streams[name].add_data(data)
   |                                ^
61 |         for cb in self.subscribers.get(name, []):
62 |             try: cb(data)
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\streaming.py:62:16
   |
60 |         if name in self.streams: self.streams[name].add_data(data)
61 |         for cb in self.subscribers.get(name, []):
62 |             try: cb(data)
   |                ^
63 |             except Exception: pass
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\streaming.py:63:29
   |
61 |         for cb in self.subscribers.get(name, []):
62 |             try: cb(data)
63 |             except Exception: pass
   |                             ^
64 |
65 |     def subscribe(self, name: str, callback: Callable[[Any], None]) -> None:
   |

E701 Multiple statements on one line (colon)
  --> src\observability\stats\streaming.py:91:58
   |
89 |         if not self._connected:
90 |             self.buffer.append(metric)
91 |             if len(self.buffer) > self.config.buffer_size: self.buffer.pop(0)
   |                                                          ^
92 |             return False
93 |         return True
   |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\subs_engine.py:175:20
    |
173 |         if isinstance(value, (int, float)):
174 |             for cb in self.subscribers.get(metric, []):
175 |                 try: cb(float(value))
    |                    ^
176 |                 except Exception: pass
177 |             return
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\subs_engine.py:176:33
    |
174 |             for cb in self.subscribers.get(metric, []):
175 |                 try: cb(float(value))
176 |                 except Exception: pass
    |                                 ^
177 |             return
178 |         import fnmatch
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\subs_engine.py:183:24
    |
181 |                 handler = self._delivery_handlers.get(sub.delivery_method)
182 |                 if handler:
183 |                     try: handler(str(value))
    |                        ^
184 |                     except Exception: pass
    |

E701 Multiple statements on one line (colon)
   --> src\observability\stats\subs_engine.py:184:37
    |
182 |                 if handler:
183 |                     try: handler(str(value))
184 |                     except Exception: pass
    |                                     ^
    |

E701 Multiple statements on one line (colon)
  --> temp\better_fix_pytest.py:41:40
   |
41 |             if not file.endswith(".py"): continue
   |                                        ^
42 |             full_path = os.path.join(root, file)
43 |             # We want path relative to src for importlib
   |

F841 Local variable `content` is assigned to but never used
   --> temp\better_fix_pytest.py:136:5
    |
135 |     # Read current file
136 |     content = conftest_path.read_text("utf-8")
    |     ^^^^^^^
    |
help: Remove assignment to unused variable `content`

F841 Local variable `pattern` is assigned to but never used
   --> temp\better_fix_pytest.py:145:5
    |
143 |     # Simple replace of the function
144 |     # We look for the decorator and the function def
145 |     pattern = r'@pytest\.fixture\(name="agent_backend_module"\)\s*\ndef agent_backend_module\(\):[\s\S]*?return [^\n]*'
    |     ^^^^^^^
146 |     # Need to match strictly to avoid eating too much if there's code after
147 |     # But usually it is the end or followed by skipped lines.
    |
help: Remove assignment to unused variable `pattern`

E701 Multiple statements on one line (colon)
   --> temp\better_fix_pytest.py:252:24
    |
250 |             break
251 |
252 |     if start_line == -1: return
    |                        ^
253 |
254 |     # Find end line
    |

F841 Local variable `pattern` is assigned to but never used
   --> temp\better_fix_pytest.py:297:5
    |
295 |     # Match the fixture function
296 |     # We match @pytest.fixture and the function definition
297 |     pattern = r'(@pytest\.fixture(?:.*\n)*def base_agent_module\(\).*:(?:\n\s+.*)+)'
    |     ^^^^^^^
298 |     # This greedy match might eat too much.
    |
help: Remove assignment to unused variable `pattern`

F841 Local variable `in_target` is assigned to but never used
   --> temp\better_fix_pytest.py:307:5
    |
305 |     new_lines = []
306 |
307 |     in_target = False
    |     ^^^^^^^^^
308 |     replaced = False
    |
help: Remove assignment to unused variable `in_target`

E701 Multiple statements on one line (colon)
   --> temp\better_fix_pytest.py:328:34
    |
326 |                   # Skip lines until end of function
327 |                 i += 1  # skip decorator
328 |                 if i < len(lines): i += 1  # skip def
    |                                  ^
329 |
330 |                   # Skip body (indented or empty lines)
    |

E701 Multiple statements on one line (colon)
  --> temp\debug_fix.py:36:30
   |
34 |     while other_lines and (other_lines[0].strip().startswith('#') or not other_lines[0].strip()):
35 |         line = other_lines.pop(0)
36 |         if line.strip() == "": continue
   |                              ^
37 |         first_block_comments.append(line)
   |

E741 Ambiguous variable name: `l`
  --> temp\debug_fix.py:44:13
   |
42 |     if other_lines and (other_lines[0].strip().startswith('"""') or other_lines[0].strip().startswith("'''")):
43 |         while other_lines:
44 |             l = other_lines.pop(0)
   |             ^
45 |             final_output.append(l)
46 |             if '"""' in l or "'''" in l:
   |

E701 Multiple statements on one line (colon)
  --> temp\find_class_locations.py:32:40
   |
30 |     for root, dirs, files in os.walk(root_dir):
31 |         for file in files:
32 |             if not file.endswith(".py"): continue
   |                                        ^
33 |             full_path = os.path.join(root, file)
34 |             rel_path = os.path.relpath(full_path, base_path).replace("\\", "/")
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:11:20
   |
 9 | …     # Remove docstrings from body for checking
10 | …     body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value,…
11 | …     if not body: return True
   |                  ^
12 | …     if len(body) > 1: return False
13 | …     stmt = body[0]
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:12:25
   |
10 | …     body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value,…
11 | …     if not body: return True
12 | …     if len(body) > 1: return False
   |                       ^
13 | …     stmt = body[0]
14 | …     if isinstance(stmt, ast.Pass): return True
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:14:38
   |
12 |         if len(body) > 1: return False
13 |         stmt = body[0]
14 |         if isinstance(stmt, ast.Pass): return True
   |                                      ^
15 |         if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis: return True
16 |         if isinstance(stmt, ast.Raise):
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:15:112
   |
13 |         stmt = body[0]
14 |         if isinstance(stmt, ast.Pass): return True
15 |         if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis: return True
   |                                                                                                                ^
16 |         if isinstance(stmt, ast.Raise):
17 |             exc_name = ""
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:18:86
   |
16 |         if isinstance(stmt, ast.Raise):
17 |             exc_name = ""
18 |             if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name): exc_name = stmt.exc.func.id
   |                                                                                      ^
19 |             elif isinstance(stmt.exc, ast.Name): exc_name = stmt.exc.id
20 |             if exc_name == "NotImplementedError": return True
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:19:48
   |
17 |             exc_name = ""
18 |             if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name): exc_name = stmt.exc.func.id
19 |             elif isinstance(stmt.exc, ast.Name): exc_name = stmt.exc.id
   |                                                ^
20 |             if exc_name == "NotImplementedError": return True
21 |         return False
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:20:49
   |
18 |             if isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name): exc_name = stmt.exc.func.id
19 |             elif isinstance(stmt.exc, ast.Name): exc_name = stmt.exc.id
20 |             if exc_name == "NotImplementedError": return True
   |                                                 ^
21 |         return False
22 |     if isinstance(node, ast.ClassDef):
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:35:77
   |
34 |         for base in node.bases:
35 |             if isinstance(base, ast.Name) and base.id in ('ABC', 'Protocol'): return "IS_ABC"
   |                                                                             ^
36 |             if isinstance(base, ast.Attribute) and base.attr in ('ABC', 'Protocol'): return "IS_ABC"
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:36:84
   |
34 |         for base in node.bases:
35 |             if isinstance(base, ast.Name) and base.id in ('ABC', 'Protocol'): return "IS_ABC"
36 |             if isinstance(base, ast.Attribute) and base.attr in ('ABC', 'Protocol'): return "IS_ABC"
   |                                                                                    ^
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:45:20
   |
43 | …     # Check all members
44 | …     body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value,…
45 | …     if not body: return True
   |                  ^
46 | …     if len(body) == 1 and isinstance(body[0], ast.Pass): return True
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:46:60
   |
44 | …     body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value,…
45 | …     if not body: return True
46 | …     if len(body) == 1 and isinstance(body[0], ast.Pass): return True
   |                                                          ^
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:57:32
   |
55 |             if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
56 |                 res = check_node(item)
57 |                 if res is False: return False
   |                                ^
58 |                 if res == "IS_ABC": return "IS_ABC"
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:58:35
   |
56 |                 res = check_node(item)
57 |                 if res is False: return False
58 |                 if res == "IS_ABC": return "IS_ABC"
   |                                   ^
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:64:44
   |
64 |             elif isinstance(item, ast.Pass): continue
   |                                            ^
65 |             else: return False
66 |         return True
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:65:17
   |
64 |             elif isinstance(item, ast.Pass): continue
65 |             else: return False
   |                 ^
66 |         return True
67 |     return True
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:73:47
   |
72 | def is_stub_file(path):
73 |     if os.path.basename(path) == "__init__.py": return False
   |                                               ^
74 |     try:
75 |         with open(path, 'r', encoding='utf-8') as f:
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:86:55
   |
86 |                     if res is False or res == "IS_ABC": return False
   |                                                       ^
87 |                 elif isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
88 |                     continue
   |

E722 Do not use bare `except`
  --> temp\find_stubs_v3.py:94:5
   |
92 |                     return False
93 |             return has_definition
94 |     except: return False
   |     ^^^^^^
   |

E701 Multiple statements on one line (colon)
  --> temp\find_stubs_v3.py:94:11
   |
92 |                     return False
93 |             return has_definition
94 |     except: return False
   |           ^
   |

E701 Multiple statements on one line (colon)
  --> temp\fix_broken_imports.py:26:40
   |
25 |         for file in files:
26 |             if not file.endswith(".py"): continue
   |                                        ^
27 |             file_path = Path(root) / file
   |

E701 Multiple statements on one line (colon)
  --> temp\fix_broken_imports_v2.py:24:40
   |
23 |         for file in files:
24 |             if not file.endswith(".py"): continue
   |                                        ^
25 |             file_path = Path(root) / file
   |

F841 Local variable `docstring_end_idx` is assigned to but never used
  --> temp\fix_e402_and_headers_v4.py:47:9
   |
45 |     if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, (ast.Constant, ast.Str)):
46 |         # It's a docstring
47 |         docstring_end_idx = tree.body[0].end_lineno - 1  # 0-indexed index in original lines
   |         ^^^^^^^^^^^^^^^^^
48 |
49 |     # 5. Reconstruct file
   |
help: Remove assignment to unused variable `docstring_end_idx`

E701 Multiple statements on one line (colon)
  --> temp\fix_e402_and_headers_v4.py:62:30
   |
60 |     while other_lines and (other_lines[0].strip().startswith('#') or not other_lines[0].strip()):
61 |         line = other_lines.pop(0)
62 |         if line.strip() == "": continue  # Skip empty lines in header for now
   |                              ^
63 |         first_block_comments.append(line)
   |

E741 Ambiguous variable name: `l`
  --> temp\fix_e402_and_headers_v4.py:76:13
   |
74 |     if other_lines and (other_lines[0].strip().startswith('"""') or other_lines[0].strip().startswith("'''")):
75 |         while other_lines:
76 |             l = other_lines.pop(0)
   |             ^
77 |             final_output.append(l)
78 |             if '"""' in l or "'''" in l:
   |

F841 Local variable `docstring_node` is assigned to but never used
  --> temp\fix_e402_docstrings.py:23:13
   |
21 |         if isinstance(val, ast.Str) or (isinstance(val, ast.Constant) and isinstance(val.value, str)):
22 |             # It's already at the top
23 |             docstring_node = tree.body[0]
   |             ^^^^^^^^^^^^^^
24 |
25 |     # Look for a string literal that is NOT at the top
   |
help: Remove assignment to unused variable `docstring_node`

F841 Local variable `new_lines` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:15:5
   |
13 |         return False
14 |
15 |     new_lines = []
   |     ^^^^^^^^^
16 |     import_lines = []
17 |     other_lines = []
   |
help: Remove assignment to unused variable `new_lines`

F841 Local variable `import_lines` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:16:5
   |
15 |     new_lines = []
16 |     import_lines = []
   |     ^^^^^^^^^^^^
17 |     other_lines = []
   |
help: Remove assignment to unused variable `import_lines`

F841 Local variable `other_lines` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:17:5
   |
15 |     new_lines = []
16 |     import_lines = []
17 |     other_lines = []
   |     ^^^^^^^^^^^
18 |
19 |     # We want to find all import statements and move them to the top,
   |
help: Remove assignment to unused variable `other_lines`

F841 Local variable `footer` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:24:5
   |
22 |     # First, separate docstrings and __future__ imports.
23 |     header = []
24 |     footer = []
   |     ^^^^^^
25 |     middle = []
   |
help: Remove assignment to unused variable `footer`

F841 Local variable `middle` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:25:5
   |
23 |     header = []
24 |     footer = []
25 |     middle = []
   |     ^^^^^^
26 |
27 |     found_first_import = False
   |
help: Remove assignment to unused variable `middle`

F841 Local variable `current_import` is assigned to but never used
  --> temp\fix_e402_versions_v2.py:58:5
   |
56 |     others = []
57 |
58 |     current_import = []
   |     ^^^^^^^^^^^^^^
59 |     for i, line in enumerate(lines):
60 |         if i <= docstring_end:
   |
help: Remove assignment to unused variable `current_import`

F841 Local variable `modified` is assigned to but never used
   --> temp\fix_e402_versions_v2.py:132:5
    |
130 |     # We want to move these assignments after the imports.
131 |
132 |     modified = False
    |     ^^^^^^^^
    |
help: Remove assignment to unused variable `modified`

F841 Local variable `version_block` is assigned to but never used
   --> temp\fix_e402_versions_v2.py:143:9
    |
141 |     match = pattern.search(content)
142 |     if match:
143 |         version_block = match.group(1)
    |         ^^^^^^^^^^^^^
144 |         # Find if there are more imports after this block
145 |         rest = content[match.end():]
    |
help: Remove assignment to unused variable `version_block`

F841 Local variable `comment` is assigned to but never used
  --> temp\fix_f401_inits_v2.py:29:21
   |
27 |                     indent = line[:line.find('from')]
28 |                     # Preserve trailing comments if any
29 |                     comment = ""
   |                     ^^^^^^^
30 |                     if '#' in name:
31 |                         # This shouldn't happen with stripped and no space, but let's be safe
   |
help: Remove assignment to unused variable `comment`

E701 Multiple statements on one line (colon)
  --> temp\fix_flake8_issues.py:49:24
   |
47 |             # Strip ANSI codes immediately
48 |             line = ansi_escape.sub('', line).strip()
49 |             if not line: continue
   |                        ^
50 |
51 |             # Standard flake8 format: path:line:col: CODE message
   |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:98:36
    |
 96 | def fix_unsed_import(lines, line_num, code, message):
 97 |     idx = line_num - 1
 98 |     if idx < 0 or idx >= len(lines): return False
    |                                    ^
 99 |     line = lines[idx]
100 |     if line is None: return False
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:100:20
    |
 98 |     if idx < 0 or idx >= len(lines): return False
 99 |     line = lines[idx]
100 |     if line is None: return False
    |                    ^
101 |
102 |     match = re.search(r"'([^']+)' imported but unused", message)
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:103:17
    |
102 |     match = re.search(r"'([^']+)' imported but unused", message)
103 |     if not match: return False
    |                 ^
104 |     pkg = match.group(1)
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:138:34
    |
136 |     for file_rel in files:
137 |         file_path = WS_ROOT / file_rel
138 |         if not file_path.exists(): continue
    |                                  ^
139 |
140 |         print(f"[{processed+1}] Fixing {file_rel}...")
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:147:25
    |
145 |             with open(file_path, "r", encoding="utf-8") as f:
146 |                 content = f.read()
147 |         except Exception: continue
    |                         ^
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:161:44
    |
160 |             idx = line_num - 1
161 |             if idx < 0 or idx >= len(lines): continue
    |                                            ^
162 |
163 |             line = lines[idx]
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:166:28
    |
166 |             if line is None: continue
    |                            ^
167 |
168 |             if code == "W293": # blank line contains whitespace
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:193:25
    |
191 |                         existing += 1
192 |                         check_idx -= 1
193 |                     else: break
    |                         ^
194 |                 to_add = needed - existing
    |

E741 Ambiguous variable name: `l`
   --> temp\fix_flake8_issues.py:232:24
    |
230 |                         fixed_count += 1
231 |
232 |         lines = [l for l in lines if l is not None]
    |                        ^
233 |         new_content = "\n".join(lines).rstrip() + "\n"
234 |         if new_content == "\n": new_content = ""
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_flake8_issues.py:234:31
    |
232 |         lines = [l for l in lines if l is not None]
233 |         new_content = "\n".join(lines).rstrip() + "\n"
234 |         if new_content == "\n": new_content = ""
    |                               ^
235 |
236 |         if new_content != content:
    |

E701 Multiple statements on one line (colon)
  --> temp\fix_hardcoded_paths.py:16:35
   |
14 |     # Scan src and tests
15 |     for target_dir in [root_dir / "src", root_dir / "tests"]:
16 |         if not target_dir.exists(): continue
   |                                   ^
17 |         for root, dirs, files in os.walk(target_dir):
18 |             for file in files:
   |

F401 [*] `typing.Dict` imported but unused
 --> temp\fix_mypy_issues.py:5:20
  |
3 | import subprocess
4 | from pathlib import Path
5 | from typing import Dict, List, Set
  |                    ^^^^
6 |
7 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F401 [*] `typing.List` imported but unused
 --> temp\fix_mypy_issues.py:5:26
  |
3 | import subprocess
4 | from pathlib import Path
5 | from typing import Dict, List, Set
  |                          ^^^^
6 |
7 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F401 [*] `typing.Set` imported but unused
 --> temp\fix_mypy_issues.py:5:32
  |
3 | import subprocess
4 | from pathlib import Path
5 | from typing import Dict, List, Set
  |                                ^^^
6 |
7 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F541 [*] f-string without any placeholders
   --> temp\fix_mypy_issues.py:146:81
    |
145 |     # Robust check for existence
146 |     if re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) or re.search(rf"\bimport typing\b", content):
    |                                                                                 ^^^^^^^^^^^^^^^^^^^^^
147 |
148 |         return content
    |
help: Remove extraneous `f` prefix

F401 [*] `typing.Dict` imported but unused
 --> temp\fix_mypy_issues_v2.py:6:20
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                    ^^^^
7 |
8 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F401 [*] `typing.List` imported but unused
 --> temp\fix_mypy_issues_v2.py:6:26
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                          ^^^^
7 |
8 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F401 [*] `typing.Set` imported but unused
 --> temp\fix_mypy_issues_v2.py:6:32
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                                ^^^
7 |
8 | MYPY_LOG = r"docs\work\mypy.txt"
  |
help: Remove unused import

F541 [*] f-string without any placeholders
  --> temp\fix_mypy_issues_v2.py:83:81
   |
81 |         name = match.group(1)
82 |
83 |     if re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) or re.search(rf"\bimport typing\b", content):
   |                                                                                 ^^^^^^^^^^^^^^^^^^^^^
   |
help: Remove extraneous `f` prefix

E701 Multiple statements on one line (colon)
   --> temp\fix_mypy_issues_v2.py:186:34
    |
184 |     for file_rel in files:
185 |         file_path = WS_ROOT / file_rel
186 |         if not file_path.exists(): continue
    |                                  ^
187 |
188 |         print(f"Processing {file_rel}...")
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_mypy_issues_v2.py:211:33
    |
209 |             line = issue['line']
210 |             lines = new_content.splitlines()
211 |             if line > len(lines): continue
    |                                 ^
212 |             line_idx = line - 1
213 |             l_content = lines[line_idx]
    |

F401 [*] `typing.Dict` imported but unused
 --> temp\fix_mypy_issues_v3.py:6:20
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                    ^^^^
7 |
8 | MYPY_LOG = r"docs\work\mypy_final.txt"
  |
help: Remove unused import: `typing.Dict`

F541 [*] f-string without any placeholders
  --> temp\fix_mypy_issues_v3.py:81:94
   |
79 |     final_needed = set()
80 |     for name in needed:
81 |         if not re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) and not re.search(rf"\bimport typing\b", content):
   |                                                                                              ^^^^^^^^^^^^^^^^^^^^^
82 |             final_needed.add(name)
83 |     return final_needed
   |
help: Remove extraneous `f` prefix

E701 Multiple statements on one line (colon)
   --> temp\fix_mypy_issues_v3.py:109:34
    |
108 |         file_path = WS_ROOT / file_rel
109 |         if not file_path.exists(): continue
    |                                  ^
110 |
111 |         print(f"Processing {file_rel}...")
    |

E701 Multiple statements on one line (colon)
   --> temp\fix_mypy_issues_v3.py:134:37
    |
133 |             line_num = issue['line']
134 |             if line_num > len(lines): continue
    |                                     ^
135 |             idx = line_num - 1
136 |             line = lines[idx]
    |

F401 [*] `typing.Dict` imported but unused
 --> temp\fix_mypy_issues_v4.py:6:20
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                    ^^^^
7 |
8 | MYPY_LOG = r"mypy_after_v3.txt"
  |
help: Remove unused import

F401 [*] `typing.Set` imported but unused
 --> temp\fix_mypy_issues_v4.py:6:32
  |
4 | import subprocess
5 | from pathlib import Path
6 | from typing import Dict, List, Set
  |                                ^^^
7 |
8 | MYPY_LOG = r"mypy_after_v3.txt"
  |
help: Remove unused import

F541 [*] f-string without any placeholders
  --> temp\fix_mypy_issues_v4.py:80:94
   |
78 |     final_typing = set()
79 |     for name in typing_needed:
80 |         if not re.search(rf"\bfrom typing import\b.*?\b{name}\b", content) and not re.search(rf"\bimport typing\b", content):
   |                                                                                              ^^^^^^^^^^^^^^^^^^^^^
81 |             final_typing.add(name)
   |
help: Remove extraneous `f` prefix

E701 Multiple statements on one line (colon)
   --> temp\fix_mypy_issues_v4.py:127:37
    |
125 |             msg = issue['message']
126 |             line_num = issue['line']
127 |             if line_num > len(lines): continue
    |                                     ^
    |

E701 Multiple statements on one line (colon)
  --> temp\fix_pytest_all.py:9:27
   |
 7 | def fix_infrastructure_conftest():
 8 |     target = Path("tests/unit/infrastructure/conftest.py")
 9 |     if not target.exists(): return
   |                           ^
10 |
11 |     content = target.read_text("utf-8")
   |

E701 Multiple statements on one line (colon)
  --> temp\fix_pytest_all.py:75:27
   |
73 | def fix_core_conftest():
74 |     target = Path("tests/unit/core/conftest.py")
75 |     if not target.exists(): return
   |                           ^
   |

E402 Module level import not at top of file
  --> temp\repair_autodoc.py:10:1
   |
 8 | sys.path.append(str(src_path.parent))
 9 |
10 | from src.observability.reports.ReportGenerator import ReportGenerator
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_agent_logic_integration.py:13:73
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_agent_logic_integration.py:13:96
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_backend_integration.py:14:73
   |
12 | # Try to import test utilities
13 | try:
14 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
15 | except ImportError:
16 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_backend_integration.py:14:96
   |
12 | # Try to import test utilities
13 | try:
14 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
15 | except ImportError:
16 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\integration\test_backend_integration.py:20:32
   |
19 |     class agent_sys_path:
20 |         def __enter__(self) -> Self:
   |                                ^^^^
21 |
22 |             return self
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_coder_logic_integration.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_coder_logic_integration.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\integration\test_coder_logic_integration.py:18:32
   |
17 |     class agent_sys_path:
18 |         def __enter__(self) -> Self:
   |                                ^^^^
19 |
20 |             return self
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_context_integration.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\integration\test_context_integration.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\integration\test_context_integration.py:18:32
   |
17 |     class agent_sys_path:
18 |         def __enter__(self) -> Self:
   |                                ^^^^
19 |
20 |             return self
   |

F821 Undefined name `logging`
  --> tests\integration\test_gui_integration.py:33:13
   |
31 |             cls._tk_available = True
32 |         except Exception as e:
33 |             logging.warning(f"Skipping GUI tests: Tkinter not available: {e}")
   |             ^^^^^^^
34 |             cls._tk_available = False
   |

E701 Multiple statements on one line (colon)
  --> tests\integration\test_webhooks_integration.py:34:16
   |
32 |     def fake_post(url: str, json: Dict[str, Any], timeout: int) -> MagicMock:
33 |         calls.append({'url': url, 'payload': json})
34 |         class R: pass
   |                ^
35 |         r = R()
36 |         r.status_code = 200
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\performance\test_agent_PERFORMANCE.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\performance\test_agent_PERFORMANCE.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F841 Local variable `core` is assigned to but never used
  --> tests\performance\test_auction_benchmark.py:10:5
   |
 9 | def benchmark_auction():
10 |     core = AuctionCore()
   |     ^^^^
11 |
12 |     # Setup data
   |
help: Remove assignment to unused variable `core`

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\performance\test_base_agent_PERFORMANCE.py:11:73
   |
 9 | # Try to import test utilities
10 | try:
11 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
12 | except ImportError:
13 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\performance\test_base_agent_PERFORMANCE.py:11:96
   |
 9 | # Try to import test utilities
10 | try:
11 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
12 | except ImportError:
13 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\performance\test_coder_PERFORMANCE.py:10:73
   |
 8 | # Try to import test utilities
 9 | try:
10 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
11 | except ImportError:
12 |     # Fallback
   |
help: Remove unused import: `tests.utils.agent_test_utils.load_module_from_path`

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phase123_decentralization.py:74:38
   |
72 |     def test_distributed_logging(self) -> None:
73 |         log_file = os.path.join(self.test_dir, "logging_agent.py")
74 |         with open(log_file, "w") as f: f.write("#")
   |                                      ^
75 |         agent = LoggingAgent(log_file)
76 |         # Test configuration
   |

E741 Ambiguous variable name: `l`
  --> tests\phases\test_phase123_decentralization.py:97:65
   |
96 |         logs = logging_agent.get_aggregated_logs()
97 |         self.assertTrue(any(l["message"] == "Alert message" for l in logs))
   |                                                                 ^
98 |
99 |     def test_did_sovereign_identity(self) -> None:
   |

E701 Multiple statements on one line (colon)
   --> tests\phases\test_phase123_decentralization.py:101:37
    |
 99 |     def test_did_sovereign_identity(self) -> None:
100 |         id_file = os.path.join(self.test_dir, "identity_agent.py")
101 |         with open(id_file, "w") as f: f.write("#")
    |                                     ^
102 |         agent = AgentIdentityAgent(id_file)
    |

F841 Local variable `pruned` is assigned to but never used
  --> tests\phases\test_phase123_final_realization.py:82:9
   |
82 |         pruned = pruner.prune_underutilized(threshold=0.0)
   |         ^^^^^^
83 |
84 |         if hasattr(self.fleet.memory, "deleted"):
   |
help: Remove assignment to unused variable `pruned`

F841 Local variable `training_data` is assigned to but never used
  --> tests\phases\test_phase19.py:50:5
   |
49 |     # generate_training_data(self, topic: str, count: int = 5)
50 |     training_data = fleet.synthetic_data.generate_training_data(topic, count=3)
   |     ^^^^^^^^^^^^^
   |
help: Remove assignment to unused variable `training_data`

F841 Local variable `agreement` is assigned to but never used
  --> tests\phases\test_phase22.py:40:5
   |
38 |     # Assuming finalizing agreement is the next step as per original context.
39 |
40 |     agreement = fleet.sovereignty_orchestrator.finalize_federated_agreement(proposal_id, ["sig1", "sig2"])
   |     ^^^^^^^^^
41 |     print("\n[2/2] Testing Recursive World Modeling (Interaction Simulation)...")
   |
help: Remove assignment to unused variable `agreement`

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phase45.py:21:36
   |
19 |         # Add entities (assuming sync or async, handling both)
20 |         res = self.fleet.graph_relational.add_entity("ByzantineJudge", "SpecializedAgent", {"logic": "AI-Voting"})
21 |         if asyncio.iscoroutine(res): await res
   |                                    ^
22 |
23 |         res = self.fleet.graph_relational.add_entity("FleetManager", "Coordinator")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phase45.py:24:36
   |
23 |         res = self.fleet.graph_relational.add_entity("FleetManager", "Coordinator")
24 |         if asyncio.iscoroutine(res): await res
   |                                    ^
25 |
26 |         res = self.fleet.graph_relational.add_relation("FleetManager", "manages", "ByzantineJudge")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phase45.py:51:36
   |
49 |         print("\nTesting MemoRAG Sharding...")
50 |         res = self.fleet.memorag.memorise_to_shard("Refactoring the consensus module", "cons_v2")
51 |         if asyncio.iscoroutine(res): await res
   |                                    ^
52 |
53 |         shards = self.fleet.memorag.list_shards()
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phase51.py:21:36
   |
19 |         # Resource limits
20 |         res = self.fleet.tenant_isolation.set_resource_limits(tenant_a, 10000, 5)
21 |         if asyncio.iscoroutine(res): await res
   |                                    ^
22 |         self.assertIn(tenant_a, self.fleet.tenant_isolation.resource_limits)
   |

F841 Local variable `res2` is assigned to but never used
  --> tests\phases\test_phase76.py:36:9
   |
34 |         # Distill
35 |         res1 = self.fleet.swarm_distillation.distill_agent_knowledge("CoderAgent", coder_kb)
36 |         res2 = self.fleet.swarm_distillation.distill_agent_knowledge("TesterAgent", tester_kb)
   |         ^^^^
   |
help: Remove assignment to unused variable `res2`

F841 Local variable `bid2` is assigned to but never used
  --> tests\phases\test_phase77.py:36:9
   |
34 |         # Place bids
35 |         bid1 = self.fleet.fleet_economy.place_bid("AgentA", "task_refactor", 20.0, priority=2)
36 |         bid2 = self.fleet.fleet_economy.place_bid("AgentB", "task_test", 10.0, priority=1)
   |         ^^^^
37 |
38 |         print(f"Bid 1: {bid1}")
   |
help: Remove assignment to unused variable `bid2`

E402 Module level import not at top of file
  --> tests\phases\test_phase78.py:10:1
   |
 8 |     sys.path.append(str(root))
 9 |
10 | from src.infrastructure.fleet.FleetManager import FleetManager
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> tests\phases\test_phase79.py:10:1
   |
 8 |     sys.path.append(str(root))
 9 |
10 | from src.infrastructure.fleet.FleetManager import FleetManager
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> tests\phases\test_phase80.py:10:1
   |
 8 |     sys.path.append(str(root))
 9 |
10 | from src.infrastructure.fleet.FleetManager import FleetManager
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

F841 Local variable `report` is assigned to but never used
  --> tests\phases\test_phase96.py:27:13
   |
25 |             report = await res
26 |         else:
27 |             report = res
   |             ^^^^^^
28 |
29 |         # Get workflow ID from the report or internal state
   |
help: Remove assignment to unused variable `report`

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:27:36
   |
25 |         ]
26 |         res = self.fleet.resource_predictor.ingest_metrics(metrics)
27 |         if asyncio.iscoroutine(res): await res
   |                                    ^
28 |
29 |         forecast = self.fleet.resource_predictor.forecast_usage()
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:30:41
   |
29 |         forecast = self.fleet.resource_predictor.forecast_usage()
30 |         if asyncio.iscoroutine(forecast): forecast = await forecast
   |                                         ^
31 |         print(f"Forecast: {forecast}")
32 |         self.assertGreater(forecast["forecasted_tokens"], 2000)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:35:40
   |
34 |         scaling = self.fleet.resource_predictor.evaluate_scaling_needs(2)
35 |         if asyncio.iscoroutine(scaling): scaling = await scaling
   |                                        ^
36 |         print(f"Scaling Recommendation: {scaling}")
37 |         self.assertTrue(scaling["trigger_scaling"])
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:42:39
   |
40 | …     print("\nTesting Phase 54: Generative UI Architecture...")
41 | …     layout = self.fleet.ui_architect.design_dashboard_layout("Code Refactor", ["AgentA", "AgentB", "AgentC", "AgentD", "AgentE", "Ag…
42 | …     if asyncio.iscoroutine(layout): layout = await layout
   |                                     ^
43 | …     print(f"Layout Panels: {len(layout['panels'])}")
44 | …     # Should have 'Agent Heatmap' because list > 5
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:59:41
   |
58 |         manifest = self.fleet.ui_architect.generate_ui_manifest("Let's run some SQL queries and plot the results.")
59 |         if asyncio.iscoroutine(manifest): manifest = await manifest
   |                                         ^
60 |         print(f"UI Manifest Plugins: {manifest['requested_plugins']}")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases53_55.py:76:36
   |
74 |         # This will also trigger the inter-fleet bridge broadcast
75 |         res = self.fleet.consensus_orchestrator.verify_state_block("Refactor UI", "Change button color to blue")
76 |         if asyncio.iscoroutine(res): await res
   |                                    ^
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:19:36
   |
17 |         # Configure AWS
18 |         res = self.fleet.cloud_provider.configure_provider("aws", {"api_key": "mock_key"})
19 |         if asyncio.iscoroutine(res): await res
   |                                    ^
20 |         print("Provider Configured")
21 |         self.assertIn("aws", self.fleet.cloud_provider.credentials)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:25:41
   |
23 |         # Generate Terraform
24 |         template = self.fleet.cloud_provider.generate_terraform_template("aws", 3, "us-west-2")
25 |         if asyncio.iscoroutine(template): template = await template
   |                                         ^
26 |         print(f"Terraform Template:\n{template}")
27 |         self.assertIn('region = "us-west-2"', template)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:32:39
   |
30 |         # Optimal region
31 |         region = self.fleet.cloud_provider.select_optimal_region({"us-east-1": 150, "eu-west-1": 80, "ap-southeast-1": 250})
32 |         if asyncio.iscoroutine(region): region = await region
   |                                       ^
33 |         print(f"Optimal Region: {region}")
34 |         self.assertEqual(region, "eu-west-1")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:42:41
   |
40 |         # Scan
41 |         scan_res = self.fleet.compliance_agent.scan_shard(sensitive_doc)
42 |         if asyncio.iscoroutine(scan_res): scan_res = await scan_res
   |                                         ^
43 |         print(f"Scan Result: {scan_res}")
44 |         self.assertTrue(scan_res["pii_detected"])
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:49:39
   |
47 |         # Mask
48 |         masked = self.fleet.compliance_agent.mask_pii(sensitive_doc)
49 |         if asyncio.iscoroutine(masked): masked = await masked
   |                                       ^
50 |         print(f"Masked Data: {masked}")
51 |         self.assertIn("[MASKED_EMAIL]", masked)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:57:40
   |
55 |         # Audit ZK Fusion
56 |         is_safe = self.fleet.compliance_agent.audit_zk_fusion([masked, "Clean data"])
57 |         if asyncio.iscoroutine(is_safe): is_safe = await is_safe
   |                                        ^
58 |         print(f"ZK Fusion Audit: {is_safe}")
59 |         self.assertTrue(is_safe)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:66:46
   |
64 |         # Audio
65 |         transcription = self.fleet.audio_reasoning.transcribe_audio("engine_hum.mp3")
66 |         if asyncio.iscoroutine(transcription): transcription = await transcription
   |                                              ^
67 |
68 |         analysis = self.fleet.audio_reasoning.analyze_audio_intent(transcription)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:69:41
   |
68 |         analysis = self.fleet.audio_reasoning.analyze_audio_intent(transcription)
69 |         if asyncio.iscoroutine(analysis): analysis = await analysis
   |                                         ^
70 |         print(f"Audio Analysis: {analysis}")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases56_58.py:84:44
   |
83 |         correlation = self.fleet.audio_reasoning.correlate_with_telemetry(analysis, {"vibration_level": 0.9})
84 |         if asyncio.iscoroutine(correlation): correlation = await correlation
   |                                            ^
   |

E701 Multiple statements on one line (colon)
   --> tests\phases\test_phases56_58.py:104:42
    |
104 |         if asyncio.iscoroutine(video_res): video_res = await video_res
    |                                          ^
105 |         print(f"Video Grounding: {video_res}")
106 |         self.assertEqual(len(video_res["detected_sequence"]), 3)
    |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:20:40
   |
18 |         content = "This project uses the GPL v3 license."
19 |         lic_res = self.fleet.legal_audit.scan_licensing(content)
20 |         if asyncio.iscoroutine(lic_res): lic_res = await lic_res
   |                                        ^
21 |         print(f"Licensing Result: {lic_res}")
22 |         self.assertEqual(lic_res["risk_level"], "high")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:32:42
   |
30 |         """
31 |         audit_res = self.fleet.legal_audit.verify_smart_contract(contract)
32 |         if asyncio.iscoroutine(audit_res): audit_res = await audit_res
   |                                          ^
33 |         print(f"Audit Result: {audit_res}")
34 |         self.assertEqual(audit_res["status"], "fail")
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:39:39
   |
37 |         # Liability
38 |         report = self.fleet.legal_audit.generate_liability_report("I guarantee this code is 100% safe.")
39 |         if asyncio.iscoroutine(report): report = await report
   |                                       ^
40 |         print(f"Liability Report: {report}")
41 |         self.assertIn("WARNING", report)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:49:40
   |
47 |         # PQC Keygen
48 |         pub_key = self.fleet.entropy_guard.generate_pqc_keypair(fleet_b)
49 |         if asyncio.iscoroutine(pub_key): pub_key = await pub_key
   |                                        ^
50 |         print(f"PQC Public Key (simulated): {pub_key}")
51 |         self.assertEqual(len(pub_key), 128)  # SHA3-512 hex length
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:56:42
   |
54 |         msg = "Top secret quantum message"
55 |         encrypted = self.fleet.entropy_guard.simulate_quantum_safe_encrypt(msg, fleet_b)
56 |         if asyncio.iscoroutine(encrypted): encrypted = await encrypted
   |                                          ^
57 |         print(f"Encrypted Data: {encrypted.hex()}")
58 |         self.assertNotEqual(msg, encrypted.decode(errors='ignore'))
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:73:36
   |
73 |         if asyncio.iscoroutine(res): await res
   |                                    ^
74 |         self.assertNotEqual(old_pool, self.fleet.entropy_guard.entropy_pool)
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:85:41
   |
83 |         # Sentiment
84 |         analysis = self.fleet.empathy_engine.analyze_user_sentiment("This is wrong, fix it now!")
85 |         if asyncio.iscoroutine(analysis): analysis = await analysis
   |                                         ^
   |

E701 Multiple statements on one line (colon)
  --> tests\phases\test_phases59_61.py:97:42
   |
96 |         mediation = self.fleet.empathy_engine.mediate_conflict("CoderAgent", "I don't like this refactoring.")
97 |         if asyncio.iscoroutine(mediation): mediation = await mediation
   |                                          ^
98 |         print(f"Mediation: {mediation}")
99 |         self.assertIn("understand", mediation)
   |

E402 Module level import not at top of file
  --> tests\specialists\test_phase122_specialists.py:12:1
   |
10 |     sys.path.append(str(root))
11 |
12 | from src.infrastructure.fleet.SecretManager import SecretManager
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
13 | from src.logic.agents.security.ImmuneSystemAgent import ImmuneSystemAgent
14 | from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
   |

E402 Module level import not at top of file
  --> tests\specialists\test_phase122_specialists.py:13:1
   |
12 | from src.infrastructure.fleet.SecretManager import SecretManager
13 | from src.logic.agents.security.ImmuneSystemAgent import ImmuneSystemAgent
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
14 | from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
15 | from src.logic.agents.system.IdentityAgent import IdentityAgent as AgentIdentityAgent
   |

E402 Module level import not at top of file
  --> tests\specialists\test_phase122_specialists.py:14:1
   |
12 | from src.infrastructure.fleet.SecretManager import SecretManager
13 | from src.logic.agents.security.ImmuneSystemAgent import ImmuneSystemAgent
14 | from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15 | from src.logic.agents.system.IdentityAgent import IdentityAgent as AgentIdentityAgent
   |

E402 Module level import not at top of file
  --> tests\specialists\test_phase122_specialists.py:15:1
   |
13 | from src.logic.agents.security.ImmuneSystemAgent import ImmuneSystemAgent
14 | from src.logic.agents.cognitive.VisualizerAgent import VisualizerAgent
15 | from src.logic.agents.system.IdentityAgent import IdentityAgent as AgentIdentityAgent
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

F405 `TestAgentComposer` may be undefined, or defined from star imports
 --> tests\unit\core\__init__.py:5:5
  |
4 | __all__ = [
5 |     "TestAgentComposer",
  |     ^^^^^^^^^^^^^^^^^^^
6 |     "TestAgentCompositionPatterns",
7 |     "TestAgentConfig",
  |

F405 `TestAgentCompositionPatterns` may be undefined, or defined from star imports
 --> tests\unit\core\__init__.py:6:5
  |
4 | __all__ = [
5 |     "TestAgentComposer",
6 |     "TestAgentCompositionPatterns",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
7 |     "TestAgentConfig",
8 |     "TestAgentConfigurationProfiles",
  |

F405 `TestAgentConfig` may be undefined, or defined from star imports
 --> tests\unit\core\__init__.py:7:5
  |
5 |     "TestAgentComposer",
6 |     "TestAgentCompositionPatterns",
7 |     "TestAgentConfig",
  |     ^^^^^^^^^^^^^^^^^
8 |     "TestAgentConfigurationProfiles",
9 |     "TestAgentEventHooks",
  |

F405 `TestAgentConfigurationProfiles` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:8:5
   |
 6 |     "TestAgentCompositionPatterns",
 7 |     "TestAgentConfig",
 8 |     "TestAgentConfigurationProfiles",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 9 |     "TestAgentEventHooks",
10 |     "TestAgentHealthDiagnostics",
   |

F405 `TestAgentEventHooks` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:9:5
   |
 7 |     "TestAgentConfig",
 8 |     "TestAgentConfigurationProfiles",
 9 |     "TestAgentEventHooks",
   |     ^^^^^^^^^^^^^^^^^^^^^
10 |     "TestAgentHealthDiagnostics",
11 |     "TestAgentPluginLoading",
   |

F405 `TestAgentHealthDiagnostics` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:10:5
   |
 8 |     "TestAgentConfigurationProfiles",
 9 |     "TestAgentEventHooks",
10 |     "TestAgentHealthDiagnostics",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |     "TestAgentPluginLoading",
12 |     "TestAgentState",
   |

F405 `TestAgentPluginLoading` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:11:5
   |
 9 |     "TestAgentEventHooks",
10 |     "TestAgentHealthDiagnostics",
11 |     "TestAgentPluginLoading",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
12 |     "TestAgentState",
13 |     "TestAgentStatePersistence",
   |

F405 `TestAgentState` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:12:5
   |
10 |     "TestAgentHealthDiagnostics",
11 |     "TestAgentPluginLoading",
12 |     "TestAgentState",
   |     ^^^^^^^^^^^^^^^^
13 |     "TestAgentStatePersistence",
14 |     "TestAuthenticationManager",
   |

F405 `TestAgentStatePersistence` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:13:5
   |
11 |     "TestAgentPluginLoading",
12 |     "TestAgentState",
13 |     "TestAgentStatePersistence",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
14 |     "TestAuthenticationManager",
15 |     "TestCacheManagement",
   |

F405 `TestAuthenticationManager` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:14:5
   |
12 |     "TestAgentState",
13 |     "TestAgentStatePersistence",
14 |     "TestAuthenticationManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
15 |     "TestCacheManagement",
16 |     "TestContentBasedResponseCaching",
   |

F405 `TestCacheManagement` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:15:5
   |
13 |     "TestAgentStatePersistence",
14 |     "TestAuthenticationManager",
15 |     "TestCacheManagement",
   |     ^^^^^^^^^^^^^^^^^^^^^
16 |     "TestContentBasedResponseCaching",
17 |     "TestContextWindow",
   |

F405 `TestContentBasedResponseCaching` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:16:5
   |
14 |     "TestAuthenticationManager",
15 |     "TestCacheManagement",
16 |     "TestContentBasedResponseCaching",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
17 |     "TestContextWindow",
18 |     "TestContextWindowManagement",
   |

F405 `TestContextWindow` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:17:5
   |
15 |     "TestCacheManagement",
16 |     "TestContentBasedResponseCaching",
17 |     "TestContextWindow",
   |     ^^^^^^^^^^^^^^^^^^^
18 |     "TestContextWindowManagement",
19 |     "TestConversationHistory",
   |

F405 `TestContextWindowManagement` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:18:5
   |
16 |     "TestContentBasedResponseCaching",
17 |     "TestContextWindow",
18 |     "TestContextWindowManagement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
19 |     "TestConversationHistory",
20 |     "TestConversationHistoryManagement",
   |

F405 `TestConversationHistory` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:19:5
   |
17 |     "TestContextWindow",
18 |     "TestContextWindowManagement",
19 |     "TestConversationHistory",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
20 |     "TestConversationHistoryManagement",
21 |     "TestCustomAuthenticationMethods",
   |

F405 `TestConversationHistoryManagement` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:20:5
   |
18 |     "TestContextWindowManagement",
19 |     "TestConversationHistory",
20 |     "TestConversationHistoryManagement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
21 |     "TestCustomAuthenticationMethods",
22 |     "TestEventHooks",
   |

F405 `TestCustomAuthenticationMethods` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:21:5
   |
19 |     "TestConversationHistory",
20 |     "TestConversationHistoryManagement",
21 |     "TestCustomAuthenticationMethods",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
22 |     "TestEventHooks",
23 |     "TestEventType",
   |

F405 `TestEventHooks` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:22:5
   |
20 |     "TestConversationHistoryManagement",
21 |     "TestCustomAuthenticationMethods",
22 |     "TestEventHooks",
   |     ^^^^^^^^^^^^^^^^
23 |     "TestEventType",
24 |     "TestFilePriorityManager",
   |

F405 `TestEventType` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:23:5
   |
21 |     "TestCustomAuthenticationMethods",
22 |     "TestEventHooks",
23 |     "TestEventType",
   |     ^^^^^^^^^^^^^^^
24 |     "TestFilePriorityManager",
25 |     "TestHealthCheckResult",
   |

F405 `TestFilePriorityManager` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:24:5
   |
22 |     "TestEventHooks",
23 |     "TestEventType",
24 |     "TestFilePriorityManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
25 |     "TestHealthCheckResult",
26 |     "TestHealthChecks",
   |

F405 `TestHealthCheckResult` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:25:5
   |
23 |     "TestEventType",
24 |     "TestFilePriorityManager",
25 |     "TestHealthCheckResult",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
26 |     "TestHealthChecks",
27 |     "TestModelSelection",
   |

F405 `TestHealthChecks` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:26:5
   |
24 |     "TestFilePriorityManager",
25 |     "TestHealthCheckResult",
26 |     "TestHealthChecks",
   |     ^^^^^^^^^^^^^^^^^^
27 |     "TestModelSelection",
28 |     "TestModelSelectionPerAgentType",
   |

F405 `TestModelSelection` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:27:5
   |
25 |     "TestHealthCheckResult",
26 |     "TestHealthChecks",
27 |     "TestModelSelection",
   |     ^^^^^^^^^^^^^^^^^^^^
28 |     "TestModelSelectionPerAgentType",
29 |     "TestMultimodalInputHandling",
   |

F405 `TestModelSelectionPerAgentType` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:28:5
   |
26 |     "TestHealthChecks",
27 |     "TestModelSelection",
28 |     "TestModelSelectionPerAgentType",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
29 |     "TestMultimodalInputHandling",
30 |     "TestMultimodalProcessor",
   |

F405 `TestMultimodalInputHandling` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:29:5
   |
27 |     "TestModelSelection",
28 |     "TestModelSelectionPerAgentType",
29 |     "TestMultimodalInputHandling",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
30 |     "TestMultimodalProcessor",
31 |     "TestPluginSystem",
   |

F405 `TestMultimodalProcessor` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:30:5
   |
28 |     "TestModelSelectionPerAgentType",
29 |     "TestMultimodalInputHandling",
30 |     "TestMultimodalProcessor",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
31 |     "TestPluginSystem",
32 |     "TestPostProcessors",
   |

F405 `TestPluginSystem` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:31:5
   |
29 |     "TestMultimodalInputHandling",
30 |     "TestMultimodalProcessor",
31 |     "TestPluginSystem",
   |     ^^^^^^^^^^^^^^^^^^
32 |     "TestPostProcessors",
33 |     "TestPromptTemplate",
   |

F405 `TestPostProcessors` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:32:5
   |
30 |     "TestMultimodalProcessor",
31 |     "TestPluginSystem",
32 |     "TestPostProcessors",
   |     ^^^^^^^^^^^^^^^^^^^^
33 |     "TestPromptTemplate",
34 |     "TestPromptTemplates",
   |

F405 `TestPromptTemplate` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:33:5
   |
31 |     "TestPluginSystem",
32 |     "TestPostProcessors",
33 |     "TestPromptTemplate",
   |     ^^^^^^^^^^^^^^^^^^^^
34 |     "TestPromptTemplates",
35 |     "TestPromptTemplatingSystem",
   |

F405 `TestPromptTemplates` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:34:5
   |
32 |     "TestPostProcessors",
33 |     "TestPromptTemplate",
34 |     "TestPromptTemplates",
   |     ^^^^^^^^^^^^^^^^^^^^^
35 |     "TestPromptTemplatingSystem",
36 |     "TestPromptVersionManager",
   |

F405 `TestPromptTemplatingSystem` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:35:5
   |
33 |     "TestPromptTemplate",
34 |     "TestPromptTemplates",
35 |     "TestPromptTemplatingSystem",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
36 |     "TestPromptVersionManager",
37 |     "TestPromptVersioningAndABTesting",
   |

F405 `TestPromptVersionManager` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:36:5
   |
34 |     "TestPromptTemplates",
35 |     "TestPromptTemplatingSystem",
36 |     "TestPromptVersionManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
37 |     "TestPromptVersioningAndABTesting",
38 |     "TestRequestBatcher",
   |

F405 `TestPromptVersioningAndABTesting` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:37:5
   |
35 |     "TestPromptTemplatingSystem",
36 |     "TestPromptVersionManager",
37 |     "TestPromptVersioningAndABTesting",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |     "TestRequestBatcher",
39 |     "TestRequestBatchingPerformance",
   |

F405 `TestRequestBatcher` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:38:5
   |
36 |     "TestPromptVersionManager",
37 |     "TestPromptVersioningAndABTesting",
38 |     "TestRequestBatcher",
   |     ^^^^^^^^^^^^^^^^^^^^
39 |     "TestRequestBatchingPerformance",
40 |     "TestResponsePostProcessingHooks",
   |

F405 `TestRequestBatchingPerformance` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:39:5
   |
37 |     "TestPromptVersioningAndABTesting",
38 |     "TestRequestBatcher",
39 |     "TestRequestBatchingPerformance",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
40 |     "TestResponsePostProcessingHooks",
41 |     "TestResponseQuality",
   |

F405 `TestResponsePostProcessingHooks` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:40:5
   |
38 |     "TestRequestBatcher",
39 |     "TestRequestBatchingPerformance",
40 |     "TestResponsePostProcessingHooks",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41 |     "TestResponseQuality",
42 |     "TestResponseQualityScoring",
   |

F405 `TestResponseQuality` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:41:5
   |
39 |     "TestRequestBatchingPerformance",
40 |     "TestResponsePostProcessingHooks",
41 |     "TestResponseQuality",
   |     ^^^^^^^^^^^^^^^^^^^^^
42 |     "TestResponseQualityScoring",
43 |     "TestResponseQualityScoring_v2",
   |

F405 `TestResponseQualityScoring` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:42:5
   |
40 |     "TestResponsePostProcessingHooks",
41 |     "TestResponseQuality",
42 |     "TestResponseQualityScoring",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
43 |     "TestResponseQualityScoring_v2",
44 |     "TestSerializationManager",
   |

F405 `TestResponseQualityScoring_v2` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:43:5
   |
41 |     "TestResponseQuality",
42 |     "TestResponseQualityScoring",
43 |     "TestResponseQualityScoring_v2",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
44 |     "TestSerializationManager",
45 |     "TestSession8Dataclasses",
   |

F405 `TestSerializationManager` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:44:5
   |
42 |     "TestResponseQualityScoring",
43 |     "TestResponseQualityScoring_v2",
44 |     "TestSerializationManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
45 |     "TestSession8Dataclasses",
46 |     "TestSession8Enums",
   |

F405 `TestSession8Dataclasses` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:45:5
   |
43 |     "TestResponseQualityScoring_v2",
44 |     "TestSerializationManager",
45 |     "TestSession8Dataclasses",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
46 |     "TestSession8Enums",
47 |     "TestStatePersistence",
   |

F405 `TestSession8Enums` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:46:5
   |
44 |     "TestSerializationManager",
45 |     "TestSession8Dataclasses",
46 |     "TestSession8Enums",
   |     ^^^^^^^^^^^^^^^^^^^
47 |     "TestStatePersistence",
48 |     "TestTokenBudget",
   |

F405 `TestStatePersistence` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:47:5
   |
45 |     "TestSession8Dataclasses",
46 |     "TestSession8Enums",
47 |     "TestStatePersistence",
   |     ^^^^^^^^^^^^^^^^^^^^^^
48 |     "TestTokenBudget",
49 |     "TestTokenBudgetManagement",
   |

F405 `TestTokenBudget` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:48:5
   |
46 |     "TestSession8Enums",
47 |     "TestStatePersistence",
48 |     "TestTokenBudget",
   |     ^^^^^^^^^^^^^^^^^
49 |     "TestTokenBudgetManagement",
50 | ]
   |

F405 `TestTokenBudgetManagement` may be undefined, or defined from star imports
  --> tests\unit\core\__init__.py:49:5
   |
47 |     "TestStatePersistence",
48 |     "TestTokenBudget",
49 |     "TestTokenBudgetManagement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
50 | ]
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\core\advanced.py:13:73
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\core\advanced.py:13:96
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\core\test_base_agent_LEGACY.py:8:5
   |
 6 | import subprocess
 7 | try:
 8 |     from tests.utils.agent_test_utils import *
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 9 | except ImportError:
10 |     pass
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_base_agent_LEGACY.py:430:10
    |
428 |     """Test import fallback chains for agent_backend module."""
429 |     # Verify that the agent_backend can be imported from scripts / agent
430 |     with agent_dir_on_path():
    |          ^^^^^^^^^^^^^^^^^
431 |         try:
432 |             from src.infrastructure.backend import execution_engine as agent_backend
    |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\core\test_context_CORE_UNIT.py:14:1
   |
13 | # Import test utilities
14 | from tests.utils.agent_test_utils import *
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15 |
16 | # Import from src if needed
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_CORE_UNIT.py:30:14
   |
28 |     def test_alert_marker_detection(self, tmp_path: Path) -> None:
29 |         """Test alert marker detection."""
30 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
31 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_CORE_UNIT.py:31:35
   |
29 |         """Test alert marker detection."""
30 |         with agent_dir_on_path():
31 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
32 |
33 |         content = "> ⚠️ WARNING: This module is deprecated."
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_CORE_UNIT.py:44:14
   |
42 |     def test_breaking_change_detection(self, tmp_path: Path) -> None:
43 |         """Test breaking change detection."""
44 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
45 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_CORE_UNIT.py:45:35
   |
43 |         """Test breaking change detection."""
44 |         with agent_dir_on_path():
45 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
46 |
47 |         content = "BREAKING CHANGE: API signature changed in v2.0"
   |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
 --> tests\unit\core\test_context_LEGACY.py:6:5
  |
4 | from typing import Any
5 | try:
6 |     from tests.utils.agent_test_utils import *
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
7 | except ImportError:
8 |     pass
  |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_LEGACY.py:17:14
   |
15 | ) -> None:
16 |         import asyncio
17 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
18 |             mod = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_LEGACY.py:18:19
   |
16 |         import asyncio
17 |         with agent_dir_on_path():
18 |             mod = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                   ^^^^^^^^^^^^^^^^^
19 |
20 |         async def fake_run_subagent(
   |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\core\test_context_UNIT.py:9:1
   |
 8 | # Import test utilities
 9 | from tests.utils.agent_test_utils import *
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
10 |
11 | # Import from src if needed
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:21:14
   |
19 |     def test_semantic_search_basic(self, tmp_path: Path) -> None:
20 |         """Test basic semantic search."""
21 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
22 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:22:35
   |
20 |         """Test basic semantic search."""
21 |         with agent_dir_on_path():
22 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
23 |
24 |         content = "def calculate_total(items) -> bool: return sum(items)"
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:35:14
   |
33 |     def test_semantic_search_relevance(self, tmp_path: Path) -> None:
34 |         """Test semantic search returns relevant results."""
35 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
36 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:36:35
   |
34 |         """Test semantic search returns relevant results."""
35 |         with agent_dir_on_path():
36 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
37 |
38 |         content = "# User Authentication\nThis module handles user login."
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:59:14
   |
57 |     def test_cross_repo_reference(self, tmp_path: Path) -> None:
58 |         """Test detecting cross-repository references."""
59 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
60 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:60:35
   |
58 |         """Test detecting cross-repository references."""
59 |         with agent_dir_on_path():
60 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
61 |
62 |         content = "Depends on: github.com / org / other-repo"
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:83:14
   |
81 |     def test_diff_content_detection(self, tmp_path: Path) -> None:
82 |         """Test diff content is detected."""
83 |         with agent_dir_on_path():
   |              ^^^^^^^^^^^^^^^^^
84 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |

F405 `load_agent_module` may be undefined, or defined from star imports
  --> tests\unit\core\test_context_UNIT.py:84:35
   |
82 |         """Test diff content is detected."""
83 |         with agent_dir_on_path():
84 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
   |                                   ^^^^^^^^^^^^^^^^^
85 |
86 |         content = """
   |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:113:14
    |
111 |     def test_template_placeholder_detection(self, tmp_path: Path) -> None:
112 |         """Test template placeholder detection."""
113 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
114 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:114:35
    |
112 |         """Test template placeholder detection."""
113 |         with agent_dir_on_path():
114 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
115 |
116 |         content = "# {module_name}\n\nDescription: {description}"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:137:14
    |
135 |     def test_inheritance_detection(self, tmp_path: Path) -> None:
136 |         """Test detecting inheritance in context."""
137 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
138 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:138:35
    |
136 |         """Test detecting inheritance in context."""
137 |         with agent_dir_on_path():
138 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
139 |
140 |         content = "Extends: base_module\nInherits: core.BaseClass"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:161:14
    |
159 |     def test_tag_detection(self, tmp_path: Path) -> None:
160 |         """Test tag detection in context."""
161 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
162 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:162:35
    |
160 |         """Test tag detection in context."""
161 |         with agent_dir_on_path():
162 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
163 |
164 |         content = "Tags: [security], [authentication], [api]"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:175:14
    |
173 |     def test_category_detection(self, tmp_path: Path) -> None:
174 |         """Test category detection."""
175 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
176 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:176:35
    |
174 |         """Test category detection."""
175 |         with agent_dir_on_path():
176 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
177 |
178 |         content = "Category: Core Infrastructure"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:199:14
    |
197 |     def test_natural_language_query(self, tmp_path: Path) -> None:
198 |         """Test natural language content is searchable."""
199 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
200 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:200:35
    |
198 |         """Test natural language content is searchable."""
199 |         with agent_dir_on_path():
200 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
201 |
202 |         content = "This module handles the user login process and session management."
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:223:14
    |
221 |     def test_version_header_detection(self, tmp_path: Path) -> None:
222 |         """Test version header detection."""
223 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
224 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:224:35
    |
222 |         """Test version header detection."""
223 |         with agent_dir_on_path():
224 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
225 |
226 |         content = "# Context v2.0.0\n\nUpdated description."
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:247:14
    |
245 |     def test_large_context_readable(self, tmp_path: Path) -> None:
246 |         """Test large context can be read."""
247 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
248 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:248:35
    |
246 |         """Test large context can be read."""
247 |         with agent_dir_on_path():
248 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
249 |
250 |         content: str = "\n".join([f"Line {i}: Description text" for i in range(100)])
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:272:14
    |
270 |     def test_markdown_format_preserved(self, tmp_path: Path) -> None:
271 |         """Test markdown format is preserved for export."""
272 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
273 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:273:35
    |
271 |         """Test markdown format is preserved for export."""
272 |         with agent_dir_on_path():
273 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
274 |
275 |         content = "# Title\n\n## Section\n\n- Item 1\n- Item 2"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:297:14
    |
295 |     def test_valid_context_format(self, tmp_path: Path) -> None:
296 |         """Test valid context format is accepted."""
297 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
298 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:298:35
    |
296 |         """Test valid context format is accepted."""
297 |         with agent_dir_on_path():
298 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
299 |
300 |         content = "# Module: test_module\n\n## Purpose\n\nTest purpose."
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:321:14
    |
319 |     def test_annotation_detection(self, tmp_path: Path) -> None:
320 |         """Test annotation detection."""
321 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
322 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:322:35
    |
320 |         """Test annotation detection."""
321 |         with agent_dir_on_path():
322 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
323 |
324 |         content = "<!-- @author: John Doe -->\n# Module"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:345:14
    |
343 |     def test_related_content_detection(self, tmp_path: Path) -> None:
344 |         """Test related content detection."""
345 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
346 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:346:35
    |
344 |         """Test related content detection."""
345 |         with agent_dir_on_path():
346 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
347 |
348 |         content = "Related: auth_module, user_module, session_module"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:369:14
    |
367 |     def test_code_example_detection(self, tmp_path: Path) -> None:
368 |         """Test code example detection in context."""
369 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
370 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:370:35
    |
368 |         """Test code example detection in context."""
369 |         with agent_dir_on_path():
370 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
371 |
372 |         content = """
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:400:14
    |
398 |     def test_refactoring_note_detection(self, tmp_path: Path) -> None:
399 |         """Test refactoring note detection."""
400 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
401 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:401:35
    |
399 |         """Test refactoring note detection."""
400 |         with agent_dir_on_path():
401 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
402 |
403 |         content = "TODO: Refactor this module to use async / await"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:424:14
    |
422 |     def test_conflict_marker_detection(self, tmp_path: Path) -> None:
423 |         """Test conflict marker detection."""
424 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
425 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:425:35
    |
423 |         """Test conflict marker detection."""
424 |         with agent_dir_on_path():
425 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
426 |
427 |         content = """
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:454:14
    |
452 |     def test_read_access(self, tmp_path: Path) -> None:
453 |         """Test read access to context."""
454 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
455 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:455:35
    |
453 |         """Test read access to context."""
454 |         with agent_dir_on_path():
455 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
456 |
457 |         content = "# Private Module\n\nInternal use only."
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:478:14
    |
476 |     def test_archived_marker_detection(self, tmp_path: Path) -> None:
477 |         """Test archived marker detection."""
478 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
479 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:479:35
    |
477 |         """Test archived marker detection."""
478 |         with agent_dir_on_path():
479 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
480 |
481 |         content = "<!-- ARCHIVED: 2024-12-01 -->\n# Old Module"
    |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:502:14
    |
500 |     def test_keywords_extracted(self, tmp_path: Path) -> None:
501 |         """Test keywords can be extracted from context."""
502 |         with agent_dir_on_path():
    |              ^^^^^^^^^^^^^^^^^
503 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\core\test_context_UNIT.py:503:13
    |
501 |         """Test keywords can be extracted from context."""
502 |         with agent_dir_on_path():
503 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |             ^^^
504 |
505 |         content = "Keywords: authentication, security, oauth2, jwt"
    |
help: Remove assignment to unused variable `mod`

F405 `load_agent_module` may be undefined, or defined from star imports
   --> tests\unit\core\test_context_UNIT.py:503:35
    |
501 |         """Test keywords can be extracted from context."""
502 |         with agent_dir_on_path():
503 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
    |                                   ^^^^^^^^^^^^^^^^^
504 |
505 |         content = "Keywords: authentication, security, oauth2, jwt"
    |

F841 Local variable `content` is assigned to but never used
   --> tests\unit\core\test_context_UNIT.py:505:9
    |
503 |             mod: sys.ModuleType = load_agent_module("logic/agents/cognitive/ContextAgent.py")
504 |
505 |         content = "Keywords: authentication, security, oauth2, jwt"
    |         ^^^^^^^
    |
help: Remove assignment to unused variable `content`

F405 `TestABTester` may be undefined, or defined from star imports
 --> tests\unit\infrastructure\__init__.py:5:5
  |
4 | __all__ = [
5 |     "TestABTester",
  |     ^^^^^^^^^^^^^^
6 |     "TestAuditLogger",
7 |     "TestSystemAnalytics",
  |

F405 `TestAuditLogger` may be undefined, or defined from star imports
 --> tests\unit\infrastructure\__init__.py:6:5
  |
4 | __all__ = [
5 |     "TestABTester",
6 |     "TestAuditLogger",
  |     ^^^^^^^^^^^^^^^^^
7 |     "TestSystemAnalytics",
8 |     "TestSystemConfigDataclass",
  |

F405 `TestSystemAnalytics` may be undefined, or defined from star imports
 --> tests\unit\infrastructure\__init__.py:7:5
  |
5 |     "TestABTester",
6 |     "TestAuditLogger",
7 |     "TestSystemAnalytics",
  |     ^^^^^^^^^^^^^^^^^^^^^
8 |     "TestSystemConfigDataclass",
9 |     "TestSystemHealthMonitor",
  |

F405 `TestSystemConfigDataclass` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:8:5
   |
 6 |     "TestAuditLogger",
 7 |     "TestSystemAnalytics",
 8 |     "TestSystemConfigDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
 9 |     "TestSystemHealthMonitor",
10 |     "TestSystemHealthStatusDataclass",
   |

F405 `TestSystemHealthMonitor` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:9:5
   |
 7 |     "TestSystemAnalytics",
 8 |     "TestSystemConfigDataclass",
 9 |     "TestSystemHealthMonitor",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
10 |     "TestSystemHealthStatusDataclass",
11 |     "TestSystemResponseDataclass",
   |

F405 `TestSystemHealthStatusDataclass` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:10:5
   |
 8 |     "TestSystemConfigDataclass",
 9 |     "TestSystemHealthMonitor",
10 |     "TestSystemHealthStatusDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |     "TestSystemResponseDataclass",
12 |     "TestBackendStateEnum",
   |

F405 `TestSystemResponseDataclass` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:11:5
   |
 9 |     "TestSystemHealthMonitor",
10 |     "TestSystemHealthStatusDataclass",
11 |     "TestSystemResponseDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
12 |     "TestBackendStateEnum",
13 |     "TestBackendTypeEnum",
   |

F405 `TestBackendStateEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:12:5
   |
10 |     "TestSystemHealthStatusDataclass",
11 |     "TestSystemResponseDataclass",
12 |     "TestBackendStateEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^
13 |     "TestBackendTypeEnum",
14 |     "TestCapabilityDiscovery",
   |

F405 `TestBackendTypeEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:13:5
   |
11 |     "TestSystemResponseDataclass",
12 |     "TestBackendStateEnum",
13 |     "TestBackendTypeEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^
14 |     "TestCapabilityDiscovery",
15 |     "TestCircuitStateEnum",
   |

F405 `TestCapabilityDiscovery` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:14:5
   |
12 |     "TestBackendStateEnum",
13 |     "TestBackendTypeEnum",
14 |     "TestCapabilityDiscovery",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
15 |     "TestCircuitStateEnum",
16 |     "TestConfigHotReloader",
   |

F405 `TestCircuitStateEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:15:5
   |
13 |     "TestBackendTypeEnum",
14 |     "TestCapabilityDiscovery",
15 |     "TestCircuitStateEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^
16 |     "TestConfigHotReloader",
17 |     "TestConnectionPool",
   |

F405 `TestConfigHotReloader` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:16:5
   |
14 |     "TestCapabilityDiscovery",
15 |     "TestCircuitStateEnum",
16 |     "TestConfigHotReloader",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
17 |     "TestConnectionPool",
18 |     "TestCustomModelEndpoints",
   |

F405 `TestConnectionPool` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:17:5
   |
15 |     "TestCircuitStateEnum",
16 |     "TestConfigHotReloader",
17 |     "TestConnectionPool",
   |     ^^^^^^^^^^^^^^^^^^^^
18 |     "TestCustomModelEndpoints",
19 |     "TestExtractCodeTransformer",
   |

F405 `TestCustomModelEndpoints` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:18:5
   |
16 |     "TestConfigHotReloader",
17 |     "TestConnectionPool",
18 |     "TestCustomModelEndpoints",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
19 |     "TestExtractCodeTransformer",
20 |     "TestExtractJsonTransformer",
   |

F405 `TestExtractCodeTransformer` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:19:5
   |
17 |     "TestConnectionPool",
18 |     "TestCustomModelEndpoints",
19 |     "TestExtractCodeTransformer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
20 |     "TestExtractJsonTransformer",
21 |     "TestGitHubModelsIntegration",
   |

F405 `TestExtractJsonTransformer` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:20:5
   |
18 |     "TestCustomModelEndpoints",
19 |     "TestExtractCodeTransformer",
20 |     "TestExtractJsonTransformer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
21 |     "TestGitHubModelsIntegration",
22 |     "TestLoadBalanceStrategyEnum",
   |

F405 `TestGitHubModelsIntegration` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:21:5
   |
19 |     "TestExtractCodeTransformer",
20 |     "TestExtractJsonTransformer",
21 |     "TestGitHubModelsIntegration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
22 |     "TestLoadBalanceStrategyEnum",
23 |     "TestLoadBalancer",
   |

F405 `TestLoadBalanceStrategyEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:22:5
   |
20 |     "TestExtractJsonTransformer",
21 |     "TestGitHubModelsIntegration",
22 |     "TestLoadBalanceStrategyEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
23 |     "TestLoadBalancer",
24 |     "TestPhase6Integration",
   |

F405 `TestLoadBalancer` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:23:5
   |
21 |     "TestGitHubModelsIntegration",
22 |     "TestLoadBalanceStrategyEnum",
23 |     "TestLoadBalancer",
   |     ^^^^^^^^^^^^^^^^^^
24 |     "TestPhase6Integration",
25 |     "TestQueuedRequestDataclass",
   |

F405 `TestPhase6Integration` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:24:5
   |
22 |     "TestLoadBalanceStrategyEnum",
23 |     "TestLoadBalancer",
24 |     "TestPhase6Integration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
25 |     "TestQueuedRequestDataclass",
26 |     "TestRequestBatcher",
   |

F405 `TestQueuedRequestDataclass` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:25:5
   |
23 |     "TestLoadBalancer",
24 |     "TestPhase6Integration",
25 |     "TestQueuedRequestDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
26 |     "TestRequestBatcher",
27 |     "TestRequestCompressor",
   |

F405 `TestRequestBatcher` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:26:5
   |
24 |     "TestPhase6Integration",
25 |     "TestQueuedRequestDataclass",
26 |     "TestRequestBatcher",
   |     ^^^^^^^^^^^^^^^^^^^^
27 |     "TestRequestCompressor",
28 |     "TestRequestContextDataclass",
   |

F405 `TestRequestCompressor` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:27:5
   |
25 |     "TestQueuedRequestDataclass",
26 |     "TestRequestBatcher",
27 |     "TestRequestCompressor",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
28 |     "TestRequestContextDataclass",
29 |     "TestRequestDeduplicator",
   |

F405 `TestRequestContextDataclass` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:28:5
   |
26 |     "TestRequestBatcher",
27 |     "TestRequestCompressor",
28 |     "TestRequestContextDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
29 |     "TestRequestDeduplicator",
30 |     "TestRequestPriorityEnum",
   |

F405 `TestRequestDeduplicator` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:29:5
   |
27 |     "TestRequestCompressor",
28 |     "TestRequestContextDataclass",
29 |     "TestRequestDeduplicator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
30 |     "TestRequestPriorityEnum",
31 |     "TestRequestQueue",
   |

F405 `TestRequestPriorityEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:30:5
   |
28 |     "TestRequestContextDataclass",
29 |     "TestRequestDeduplicator",
30 |     "TestRequestPriorityEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
31 |     "TestRequestQueue",
32 |     "TestRequestRecorder",
   |

F405 `TestRequestQueue` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:31:5
   |
29 |     "TestRequestDeduplicator",
30 |     "TestRequestPriorityEnum",
31 |     "TestRequestQueue",
   |     ^^^^^^^^^^^^^^^^^^
32 |     "TestRequestRecorder",
33 |     "TestRequestSigner",
   |

F405 `TestRequestRecorder` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:32:5
   |
30 |     "TestRequestPriorityEnum",
31 |     "TestRequestQueue",
32 |     "TestRequestRecorder",
   |     ^^^^^^^^^^^^^^^^^^^^^
33 |     "TestRequestSigner",
34 |     "TestRequestThrottler",
   |

F405 `TestRequestSigner` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:33:5
   |
31 |     "TestRequestQueue",
32 |     "TestRequestRecorder",
33 |     "TestRequestSigner",
   |     ^^^^^^^^^^^^^^^^^^^
34 |     "TestRequestThrottler",
35 |     "TestRequestTracer",
   |

F405 `TestRequestThrottler` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:34:5
   |
32 |     "TestRequestRecorder",
33 |     "TestRequestSigner",
34 |     "TestRequestThrottler",
   |     ^^^^^^^^^^^^^^^^^^^^^^
35 |     "TestRequestTracer",
36 |     "TestResponseTransformEnum",
   |

F405 `TestRequestTracer` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:35:5
   |
33 |     "TestRequestSigner",
34 |     "TestRequestThrottler",
35 |     "TestRequestTracer",
   |     ^^^^^^^^^^^^^^^^^^^
36 |     "TestResponseTransformEnum",
37 |     "TestStripWhitespaceTransformer",
   |

F405 `TestResponseTransformEnum` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:36:5
   |
34 |     "TestRequestThrottler",
35 |     "TestRequestTracer",
36 |     "TestResponseTransformEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
37 |     "TestStripWhitespaceTransformer",
38 |     "TestTTLCache",
   |

F405 `TestStripWhitespaceTransformer` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:37:5
   |
35 |     "TestRequestTracer",
36 |     "TestResponseTransformEnum",
37 |     "TestStripWhitespaceTransformer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |     "TestTTLCache",
39 |     "TestUsageQuotaManager",
   |

F405 `TestTTLCache` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:38:5
   |
36 |     "TestResponseTransformEnum",
37 |     "TestStripWhitespaceTransformer",
38 |     "TestTTLCache",
   |     ^^^^^^^^^^^^^^
39 |     "TestUsageQuotaManager",
40 |     "TestVersionNegotiator",
   |

F405 `TestUsageQuotaManager` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:39:5
   |
37 |     "TestStripWhitespaceTransformer",
38 |     "TestTTLCache",
39 |     "TestUsageQuotaManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
40 |     "TestVersionNegotiator",
41 | ]
   |

F405 `TestVersionNegotiator` may be undefined, or defined from star imports
  --> tests\unit\infrastructure\__init__.py:40:5
   |
38 |     "TestTTLCache",
39 |     "TestUsageQuotaManager",
40 |     "TestVersionNegotiator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
41 | ]
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\infrastructure\test_backend_CORE_UNIT.py:15:73
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\infrastructure\test_backend_CORE_UNIT.py:15:96
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
 --> tests\unit\infrastructure\test_backend_LEGACY.py:5:5
  |
3 | from typing import Any
4 | try:
5 |     from tests.utils.agent_test_utils import *
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
6 | except ImportError:
7 |     pass
  |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\infrastructure\test_backend_UNIT.py:11:73
   |
 9 | # Try to import test utilities
10 | try:
11 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
12 | except ImportError:
13 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\infrastructure\test_backend_UNIT.py:11:96
   |
 9 | # Try to import test utilities
10 | try:
11 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
12 | except ImportError:
13 |     # Fallback
   |
help: Remove unused import

F841 Local variable `src_dir` is assigned to but never used
  --> tests\unit\infrastructure\test_models_propagation.py:11:5
   |
 9 | def load_agent_module() -> Any:
10 |     repo_root: Path = Path(__file__).resolve().parents[2]
11 |     src_dir: Path = repo_root / 'src'
   |     ^^^^^^^
12 |     if str(repo_root) not in sys.path:
13 |         sys.path.insert(0, str(repo_root))
   |
help: Remove assignment to unused variable `src_dir`

F405 `TestAIRetryAndErrorRecovery` may be undefined, or defined from star imports
 --> tests\unit\logic\__init__.py:5:5
  |
4 | __all__ = [
5 |     "TestAIRetryAndErrorRecovery",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
6 |     "TestAPICompatibility",
7 |     "TestARIAAttributeDataclass",
  |

F405 `TestAPICompatibility` may be undefined, or defined from star imports
 --> tests\unit\logic\__init__.py:6:5
  |
4 | __all__ = [
5 |     "TestAIRetryAndErrorRecovery",
6 |     "TestAPICompatibility",
  |     ^^^^^^^^^^^^^^^^^^^^^^
7 |     "TestARIAAttributeDataclass",
8 |     "TestAccessibilityAnalyzer",
  |

F405 `TestARIAAttributeDataclass` may be undefined, or defined from star imports
 --> tests\unit\logic\__init__.py:7:5
  |
5 |     "TestAIRetryAndErrorRecovery",
6 |     "TestAPICompatibility",
7 |     "TestARIAAttributeDataclass",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
8 |     "TestAccessibilityAnalyzer",
9 |     "TestAccessibilityIssueDataclass",
  |

F405 `TestAccessibilityAnalyzer` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:8:5
   |
 6 |     "TestAPICompatibility",
 7 |     "TestARIAAttributeDataclass",
 8 |     "TestAccessibilityAnalyzer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
 9 |     "TestAccessibilityIssueDataclass",
10 |     "TestAccessibilityIssueTypeEnum",
   |

F405 `TestAccessibilityIssueDataclass` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:9:5
   |
 7 |     "TestARIAAttributeDataclass",
 8 |     "TestAccessibilityAnalyzer",
 9 |     "TestAccessibilityIssueDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
10 |     "TestAccessibilityIssueTypeEnum",
11 |     "TestAccessibilityReportDataclass",
   |

F405 `TestAccessibilityIssueTypeEnum` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:10:5
   |
 8 |     "TestAccessibilityAnalyzer",
 9 |     "TestAccessibilityIssueDataclass",
10 |     "TestAccessibilityIssueTypeEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |     "TestAccessibilityReportDataclass",
12 |     "TestAccessibilitySeverityEnum",
   |

F405 `TestAccessibilityReportDataclass` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:11:5
   |
 9 |     "TestAccessibilityIssueDataclass",
10 |     "TestAccessibilityIssueTypeEnum",
11 |     "TestAccessibilityReportDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
12 |     "TestAccessibilitySeverityEnum",
13 |     "TestAdvancedCodeFormatting",
   |

F405 `TestAccessibilitySeverityEnum` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:12:5
   |
10 |     "TestAccessibilityIssueTypeEnum",
11 |     "TestAccessibilityReportDataclass",
12 |     "TestAccessibilitySeverityEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
13 |     "TestAdvancedCodeFormatting",
14 |     "TestAdvancedSecurityValidation",
   |

F405 `TestAdvancedCodeFormatting` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:13:5
   |
11 |     "TestAccessibilityReportDataclass",
12 |     "TestAccessibilitySeverityEnum",
13 |     "TestAdvancedCodeFormatting",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
14 |     "TestAdvancedSecurityValidation",
15 |     "TestBackupCreation",
   |

F405 `TestAdvancedSecurityValidation` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:14:5
   |
12 |     "TestAccessibilitySeverityEnum",
13 |     "TestAdvancedCodeFormatting",
14 |     "TestAdvancedSecurityValidation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
15 |     "TestBackupCreation",
16 |     "TestCodeComplexity",
   |

F405 `TestBackupCreation` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:15:5
   |
13 |     "TestAdvancedCodeFormatting",
14 |     "TestAdvancedSecurityValidation",
15 |     "TestBackupCreation",
   |     ^^^^^^^^^^^^^^^^^^^^
16 |     "TestCodeComplexity",
17 |     "TestCodeConsistency",
   |

F405 `TestCodeComplexity` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:16:5
   |
14 |     "TestAdvancedSecurityValidation",
15 |     "TestBackupCreation",
16 |     "TestCodeComplexity",
   |     ^^^^^^^^^^^^^^^^^^^^
17 |     "TestCodeConsistency",
18 |     "TestCodeDocumentationGeneration",
   |

F405 `TestCodeConsistency` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:17:5
   |
15 |     "TestBackupCreation",
16 |     "TestCodeComplexity",
17 |     "TestCodeConsistency",
   |     ^^^^^^^^^^^^^^^^^^^^^
18 |     "TestCodeDocumentationGeneration",
19 |     "TestCodeFormatting",
   |

F405 `TestCodeDocumentationGeneration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:18:5
   |
16 |     "TestCodeComplexity",
17 |     "TestCodeConsistency",
18 |     "TestCodeDocumentationGeneration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
19 |     "TestCodeFormatting",
20 |     "TestCodeMetrics",
   |

F405 `TestCodeFormatting` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:19:5
   |
17 |     "TestCodeConsistency",
18 |     "TestCodeDocumentationGeneration",
19 |     "TestCodeFormatting",
   |     ^^^^^^^^^^^^^^^^^^^^
20 |     "TestCodeMetrics",
21 |     "TestCodeOptimizationPatterns",
   |

F405 `TestCodeMetrics` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:20:5
   |
18 |     "TestCodeDocumentationGeneration",
19 |     "TestCodeFormatting",
20 |     "TestCodeMetrics",
   |     ^^^^^^^^^^^^^^^^^
21 |     "TestCodeOptimizationPatterns",
22 |     "TestCodeQualityValidation",
   |

F405 `TestCodeOptimizationPatterns` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:21:5
   |
19 |     "TestCodeFormatting",
20 |     "TestCodeMetrics",
21 |     "TestCodeOptimizationPatterns",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
22 |     "TestCodeQualityValidation",
23 |     "TestCodeRefactoring",
   |

F405 `TestCodeQualityValidation` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:22:5
   |
20 |     "TestCodeMetrics",
21 |     "TestCodeOptimizationPatterns",
22 |     "TestCodeQualityValidation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
23 |     "TestCodeRefactoring",
24 |     "TestCodeSplitting",
   |

F405 `TestCodeRefactoring` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:23:5
   |
21 |     "TestCodeOptimizationPatterns",
22 |     "TestCodeQualityValidation",
23 |     "TestCodeRefactoring",
   |     ^^^^^^^^^^^^^^^^^^^^^
24 |     "TestCodeSplitting",
25 |     "TestCodeTemplates",
   |

F405 `TestCodeSplitting` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:24:5
   |
22 |     "TestCodeQualityValidation",
23 |     "TestCodeRefactoring",
24 |     "TestCodeSplitting",
   |     ^^^^^^^^^^^^^^^^^^^
25 |     "TestCodeTemplates",
26 |     "TestColorContrastResultDataclass",
   |

F405 `TestCodeTemplates` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:25:5
   |
23 |     "TestCodeRefactoring",
24 |     "TestCodeSplitting",
25 |     "TestCodeTemplates",
   |     ^^^^^^^^^^^^^^^^^^^
26 |     "TestColorContrastResultDataclass",
27 |     "TestComplexityAnalysis",
   |

F405 `TestColorContrastResultDataclass` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:26:5
   |
24 |     "TestCodeSplitting",
25 |     "TestCodeTemplates",
26 |     "TestColorContrastResultDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
27 |     "TestComplexityAnalysis",
28 |     "TestConcurrency",
   |

F405 `TestComplexityAnalysis` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:27:5
   |
25 |     "TestCodeTemplates",
26 |     "TestColorContrastResultDataclass",
27 |     "TestComplexityAnalysis",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
28 |     "TestConcurrency",
29 |     "TestCoverageGapDetection",
   |

F405 `TestConcurrency` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:28:5
   |
26 |     "TestColorContrastResultDataclass",
27 |     "TestComplexityAnalysis",
28 |     "TestConcurrency",
   |     ^^^^^^^^^^^^^^^^^
29 |     "TestCoverageGapDetection",
30 |     "TestDeadCodeDetection",
   |

F405 `TestCoverageGapDetection` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:29:5
   |
27 |     "TestComplexityAnalysis",
28 |     "TestConcurrency",
29 |     "TestCoverageGapDetection",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
30 |     "TestDeadCodeDetection",
31 |     "TestDependencyInjectionPatterns",
   |

F405 `TestDeadCodeDetection` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:30:5
   |
28 |     "TestConcurrency",
29 |     "TestCoverageGapDetection",
30 |     "TestDeadCodeDetection",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
31 |     "TestDependencyInjectionPatterns",
32 |     "TestDiffApplication",
   |

F405 `TestDependencyInjectionPatterns` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:31:5
   |
29 |     "TestCoverageGapDetection",
30 |     "TestDeadCodeDetection",
31 |     "TestDependencyInjectionPatterns",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
32 |     "TestDiffApplication",
33 |     "TestDocstringGeneration",
   |

F405 `TestDiffApplication` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:32:5
   |
30 |     "TestDeadCodeDetection",
31 |     "TestDependencyInjectionPatterns",
32 |     "TestDiffApplication",
   |     ^^^^^^^^^^^^^^^^^^^^^
33 |     "TestDocstringGeneration",
34 |     "TestErrorRecovery",
   |

F405 `TestDocstringGeneration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:33:5
   |
31 |     "TestDependencyInjectionPatterns",
32 |     "TestDiffApplication",
33 |     "TestDocstringGeneration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
34 |     "TestErrorRecovery",
35 |     "TestFlake8Integration",
   |

F405 `TestErrorRecovery` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:34:5
   |
32 |     "TestDiffApplication",
33 |     "TestDocstringGeneration",
34 |     "TestErrorRecovery",
   |     ^^^^^^^^^^^^^^^^^^^
35 |     "TestFlake8Integration",
36 |     "TestImportOrganization",
   |

F405 `TestFlake8Integration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:35:5
   |
33 |     "TestDocstringGeneration",
34 |     "TestErrorRecovery",
35 |     "TestFlake8Integration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
36 |     "TestImportOrganization",
37 |     "TestIncrementalImprovement",
   |

F405 `TestImportOrganization` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:36:5
   |
34 |     "TestErrorRecovery",
35 |     "TestFlake8Integration",
36 |     "TestImportOrganization",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
37 |     "TestIncrementalImprovement",
38 |     "TestIntegration",
   |

F405 `TestIncrementalImprovement` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:37:5
   |
35 |     "TestFlake8Integration",
36 |     "TestImportOrganization",
37 |     "TestIncrementalImprovement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |     "TestIntegration",
39 |     "TestLargeFileHandling",
   |

F405 `TestIntegration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:38:5
   |
36 |     "TestImportOrganization",
37 |     "TestIncrementalImprovement",
38 |     "TestIntegration",
   |     ^^^^^^^^^^^^^^^^^
39 |     "TestLargeFileHandling",
40 |     "TestMergeConflictResolution",
   |

F405 `TestLargeFileHandling` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:39:5
   |
37 |     "TestIncrementalImprovement",
38 |     "TestIntegration",
39 |     "TestLargeFileHandling",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
40 |     "TestMergeConflictResolution",
41 |     "TestMigrationAutomation",
   |

F405 `TestMergeConflictResolution` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:40:5
   |
38 |     "TestIntegration",
39 |     "TestLargeFileHandling",
40 |     "TestMergeConflictResolution",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
41 |     "TestMigrationAutomation",
42 |     "TestMultiLanguageCodeGeneration",
   |

F405 `TestMigrationAutomation` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:41:5
   |
39 |     "TestLargeFileHandling",
40 |     "TestMergeConflictResolution",
41 |     "TestMigrationAutomation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
42 |     "TestMultiLanguageCodeGeneration",
43 |     "TestPerformanceProfiling",
   |

F405 `TestMultiLanguageCodeGeneration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:42:5
   |
40 |     "TestMergeConflictResolution",
41 |     "TestMigrationAutomation",
42 |     "TestMultiLanguageCodeGeneration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
43 |     "TestPerformanceProfiling",
44 |     "TestQualityGates",
   |

F405 `TestPerformanceProfiling` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:43:5
   |
41 |     "TestMigrationAutomation",
42 |     "TestMultiLanguageCodeGeneration",
43 |     "TestPerformanceProfiling",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
44 |     "TestQualityGates",
45 |     "TestRollback",
   |

F405 `TestQualityGates` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:44:5
   |
42 |     "TestMultiLanguageCodeGeneration",
43 |     "TestPerformanceProfiling",
44 |     "TestQualityGates",
   |     ^^^^^^^^^^^^^^^^^^
45 |     "TestRollback",
46 |     "TestSecurityScanning",
   |

F405 `TestRollback` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:45:5
   |
43 |     "TestPerformanceProfiling",
44 |     "TestQualityGates",
45 |     "TestRollback",
   |     ^^^^^^^^^^^^^^
46 |     "TestSecurityScanning",
47 |     "TestSecurityScanningIntegration",
   |

F405 `TestSecurityScanning` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:46:5
   |
44 |     "TestQualityGates",
45 |     "TestRollback",
46 |     "TestSecurityScanning",
   |     ^^^^^^^^^^^^^^^^^^^^^^
47 |     "TestSecurityScanningIntegration",
48 |     "TestStyleUnification",
   |

F405 `TestSecurityScanningIntegration` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:47:5
   |
45 |     "TestRollback",
46 |     "TestSecurityScanning",
47 |     "TestSecurityScanningIntegration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
48 |     "TestStyleUnification",
49 |     "TestSyntaxValidation",
   |

F405 `TestStyleUnification` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:48:5
   |
46 |     "TestSecurityScanning",
47 |     "TestSecurityScanningIntegration",
48 |     "TestStyleUnification",
   |     ^^^^^^^^^^^^^^^^^^^^^^
49 |     "TestSyntaxValidation",
50 |     "TestTypeAnnotationInference",
   |

F405 `TestSyntaxValidation` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:49:5
   |
47 |     "TestSecurityScanningIntegration",
48 |     "TestStyleUnification",
49 |     "TestSyntaxValidation",
   |     ^^^^^^^^^^^^^^^^^^^^^^
50 |     "TestTypeAnnotationInference",
51 |     "TestWCAGLevelEnum",
   |

F405 `TestTypeAnnotationInference` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:50:5
   |
48 |     "TestStyleUnification",
49 |     "TestSyntaxValidation",
50 |     "TestTypeAnnotationInference",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
51 |     "TestWCAGLevelEnum",
52 | ]
   |

F405 `TestWCAGLevelEnum` may be undefined, or defined from star imports
  --> tests\unit\logic\__init__.py:51:5
   |
49 |     "TestSyntaxValidation",
50 |     "TestTypeAnnotationInference",
51 |     "TestWCAGLevelEnum",
   |     ^^^^^^^^^^^^^^^^^^^
52 | ]
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\advanced.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\advanced.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\logic\advanced.py:18:32
   |
17 |     class agent_sys_path:
18 |         def __enter__(self) -> Self:
   |                                ^^^^
19 |
20 |             return self
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:37:27
   |
35 |             mod.LockType = LockType
36 |             mod.RateLimitStrategy = RateLimitStrategy
37 |         except ImportError: pass
   |                           ^
38 |
39 |         # Utils
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:43:27
   |
41 |             from src.core.base.utils.AgentPriorityQueue import AgentPriorityQueue
42 |             mod.AgentPriorityQueue = AgentPriorityQueue
43 |         except ImportError: pass
   |                           ^
44 |
45 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:48:27
   |
46 |             from src.core.base.utils.ValidationRuleManager import ValidationRuleManager
47 |             mod.ValidationRuleManager = ValidationRuleManager
48 |         except ImportError: pass
   |                           ^
49 |
50 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:53:27
   |
51 |             from src.core.base.utils.TelemetryCollector import TelemetryCollector
52 |             mod.TelemetryCollector = TelemetryCollector
53 |         except ImportError: pass
   |                           ^
54 |
55 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:58:27
   |
56 |             from src.core.base.utils.ConditionalExecutor import ConditionalExecutor
57 |             mod.ConditionalExecutor = ConditionalExecutor
58 |         except ImportError: pass
   |                           ^
59 |
60 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:63:27
   |
61 |             from src.core.base.utils.TemplateManager import TemplateManager
62 |             mod.TemplateManager = TemplateManager
63 |         except ImportError: pass
   |                           ^
64 |
65 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:68:27
   |
66 |             from src.core.base.utils.ResultCache import ResultCache
67 |             mod.ResultCache = ResultCache
68 |         except ImportError: pass
   |                           ^
69 |
70 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:73:27
   |
71 |             from src.core.base.utils.ExecutionScheduler import ExecutionScheduler
72 |             mod.ExecutionScheduler = ExecutionScheduler
73 |         except ImportError: pass
   |                           ^
74 |
75 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:78:27
   |
76 |             from src.core.base.utils.FileLockManager import FileLockManager
77 |             mod.FileLockManager = FileLockManager
78 |         except ImportError: pass
   |                           ^
79 |
80 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:83:27
   |
81 |             from src.core.base.utils.RateLimiter import RateLimiter
82 |             mod.RateLimiter = RateLimiter
83 |         except ImportError: pass
   |                           ^
84 |
85 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:88:27
   |
86 |             from src.core.base.utils.DiffGenerator import DiffGenerator
87 |             mod.DiffGenerator = DiffGenerator
88 |         except ImportError: pass
   |                           ^
89 |
90 |         try:
   |

E701 Multiple statements on one line (colon)
  --> tests\unit\logic\conftest.py:93:27
   |
91 |             from src.core.base.utils.FileLock import FileLock
92 |             mod.FileLock = FileLock
93 |         except ImportError: pass
   |                           ^
94 |
95 |         # Core Base
   |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:103:27
    |
101 |                 AgentPluginBase.shutdown = lambda self: None
102 |             mod.AgentPluginBase = AgentPluginBase
103 |         except ImportError: pass
    |                           ^
104 |
105 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:108:27
    |
106 |             from src.core.base.DependencyGraph import DependencyGraph
107 |             mod.DependencyGraph = DependencyGraph
108 |         except ImportError: pass
    |                           ^
109 |
110 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:113:27
    |
111 |             from src.core.base.ConfigLoader import ConfigLoader
112 |             mod.ConfigLoader = ConfigLoader
113 |         except ImportError: pass
    |                           ^
114 |
115 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:118:27
    |
116 |             from src.core.base.GracefulShutdown import GracefulShutdown
117 |             mod.GracefulShutdown = GracefulShutdown
118 |         except ImportError: pass
    |                           ^
119 |
120 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:123:27
    |
121 |             from src.core.base.IncrementalProcessor import IncrementalProcessor
122 |             mod.IncrementalProcessor = IncrementalProcessor
123 |         except ImportError: pass
    |                           ^
124 |
125 |         # Managers
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:130:27
    |
128 |             mod.ProfileManager = ProfileManager
129 |             mod.HealthChecker = HealthChecker
130 |         except ImportError: pass
    |                           ^
131 |
132 |         # Logic
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:136:27
    |
134 |             from src.logic.agents.development.GitBranchProcessor import GitBranchProcessor
135 |             mod.GitBranchProcessor = GitBranchProcessor
136 |         except ImportError: pass
    |                           ^
137 |
138 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:141:27
    |
139 |             from src.logic.orchestration.AgentChain import AgentChain
140 |             mod.AgentChain = AgentChain
141 |         except ImportError: pass
    |                           ^
142 |
143 |         # Models
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:149:27
    |
147 |             mod.RateLimitConfig = RateLimitConfig
148 |             mod.ShutdownState = ShutdownState
149 |         except ImportError: pass
    |                           ^
150 |
151 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:155:27
    |
153 |             mod.AgentPluginConfig = AgentPluginConfig
154 |             mod.AgentHealthCheck = AgentHealthCheck
155 |         except ImportError: pass
    |                           ^
156 |
157 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:200:27
    |
198 |             mod.ValidationRule = TestValidationRule
199 |
200 |         except ImportError: pass
    |                           ^
201 |
202 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:247:27
    |
246 |             mod.CircuitBreaker = TestCircuitBreaker
247 |         except ImportError: pass
    |                           ^
248 |
249 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:252:27
    |
250 |             from src.core.base.utils.ConditionalExecutor import ConditionalExecutor
251 |             mod.ConditionalExecutor = ConditionalExecutor
252 |         except ImportError: pass
    |                           ^
253 |
254 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:257:27
    |
255 |             from src.core.base.DependencyGraph import DependencyGraph
256 |             mod.DependencyGraph = DependencyGraph
257 |         except ImportError: pass
    |                           ^
258 |
259 |         try:
    |

E701 Multiple statements on one line (colon)
   --> tests\unit\logic\conftest.py:262:27
    |
260 |             from src.core.base.utils.ValidationRuleManager import ValidationRuleManager
261 |             mod.ValidationRuleManager = ValidationRuleManager
262 |         except ImportError: pass
    |                           ^
    |

E741 Ambiguous variable name: `l`
   --> tests\unit\logic\conftest.py:462:56
    |
460 |                     if ignore_file.exists():
461 |                         lines = ignore_file.read_text().splitlines()
462 |                         patterns.extend([l.strip() for l in lines if l.strip()])
    |                                                        ^
463 |                     # Check parent just in case (though test seems to test load_cascading_codeignore_loads_subdirectory_patterns)
464 |                     if path and path != self.repo_root:
    |

E741 Ambiguous variable name: `l`
   --> tests\unit\logic\conftest.py:468:60
    |
466 |                         if root_ignore.exists():
467 |                             lines = root_ignore.read_text().splitlines()
468 |                             patterns.extend([l.strip() for l in lines if l.strip()])
    |                                                            ^
469 |                     return patterns
    |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\edge_cases.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\edge_cases.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_ADVANCED_UNIT.py:15:73
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_ADVANCED_UNIT.py:15:96
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_CORE_UNIT.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_CORE_UNIT.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\logic\test_agent_LEGACY.py:9:5
   |
 8 | try:
 9 |     from tests.utils.agent_test_utils import *
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
10 | except ImportError:
11 |     pass
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_UNIT.py:15:73
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_agent_UNIT.py:15:96
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\logic\test_coder_CORE_UNIT.py:22:1
   |
20 | import sys
21 | import tempfile
22 | from tests.utils.agent_test_utils import *  # Added for modular test support
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
23 |
24 | # Try to import test utilities
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_coder_CORE_UNIT.py:26:73
   |
24 | # Try to import test utilities
25 | try:
26 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
27 | except ImportError:
28 |     # Fallback
   |
help: Remove unused import: `tests.utils.agent_test_utils.load_module_from_path`

F841 Local variable `mod` is assigned to but never used
  --> tests\unit\logic\test_coder_CORE_UNIT.py:77:13
   |
75 |         """Test enum has expected values."""
76 |         with agent_dir_on_path():
77 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
   |             ^^^
78 |         assert AccessibilityIssueType.MISSING_ALT_TEXT.value == "missing_alt_text"
79 |         assert AccessibilityIssueType.LOW_COLOR_CONTRAST.value == "low_color_contrast"
   |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
  --> tests\unit\logic\test_coder_CORE_UNIT.py:86:13
   |
84 |         """Test all enum members exist."""
85 |         with agent_dir_on_path():
86 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
   |             ^^^
87 |         members: List[Any] = list(AccessibilityIssueType)
88 |         assert len(members) == 10
   |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
  --> tests\unit\logic\test_coder_CORE_UNIT.py:97:13
   |
95 |         """Test enum has expected values."""
96 |         with agent_dir_on_path():
97 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
   |             ^^^
98 |         assert AccessibilitySeverity.CRITICAL.value == 4
99 |         assert AccessibilitySeverity.SERIOUS.value == 3
   |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:106:13
    |
104 |         """Test severity values are ordered correctly."""
105 |         with agent_dir_on_path():
106 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
107 |         assert AccessibilitySeverity.MINOR.value < AccessibilitySeverity.MODERATE.value
108 |         assert AccessibilitySeverity.MODERATE.value < AccessibilitySeverity.SERIOUS.value
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:118:13
    |
116 |         """Test enum has expected values."""
117 |         with agent_dir_on_path():
118 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
119 |         assert WCAGLevel.A.value == "A"
120 |         assert WCAGLevel.AA.value == "AA"
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:126:13
    |
124 |         """Test all WCAG levels exist."""
125 |         with agent_dir_on_path():
126 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
127 |         assert len(list(WCAGLevel)) == 3
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:136:13
    |
134 |         """Test creating AccessibilityIssue."""
135 |         with agent_dir_on_path():
136 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
137 |         issue = AccessibilityIssue(
138 |             issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:154:13
    |
152 |         """Test AccessibilityIssue defaults."""
153 |         with agent_dir_on_path():
154 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
155 |         issue = AccessibilityIssue(
156 |             issue_type=AccessibilityIssueType.ARIA_MISSING,
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:174:13
    |
172 |         """Test creating ColorContrastResult."""
173 |         with agent_dir_on_path():
174 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
175 |         result = ColorContrastResult(
176 |             foreground="#000000",
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:193:13
    |
191 |         """Test creating AccessibilityReport."""
192 |         with agent_dir_on_path():
193 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
194 |         report = AccessibilityReport(
195 |             file_path="test.html",
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:209:13
    |
207 |         """Test AccessibilityReport defaults."""
208 |         with agent_dir_on_path():
209 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
210 |         report = AccessibilityReport(file_path="test.html")
211 |         assert report.issues == []
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:222:13
    |
220 |         """Test creating ARIAAttribute."""
221 |         with agent_dir_on_path():
222 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
223 |         attr = ARIAAttribute(
224 |             name="aria-label",
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:239:13
    |
237 |         """Test AccessibilityAnalyzer initialization."""
238 |         with agent_dir_on_path():
239 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
240 |         analyzer = AccessibilityAgent(WCAGLevel.AA)
241 |         assert analyzer.target_level == WCAGLevel.AA
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:247:13
    |
245 |         """Test detecting missing alt text in HTML."""
246 |         with agent_dir_on_path():
247 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
248 |         analyzer = AccessibilityAgent()
249 |         html_content = '<html><body><img src="test.jpg"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:258:13
    |
256 |         """Test HTML with proper alt text has no alt issues."""
257 |         with agent_dir_on_path():
258 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
259 |         analyzer = AccessibilityAgent()
260 |         html_content = '<html><body><img src="test.jpg" alt="Test image"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:269:13
    |
267 |         """Test detecting missing form labels in HTML."""
268 |         with agent_dir_on_path():
269 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
270 |         analyzer = AccessibilityAgent()
271 |         html_content = '<html><body><input type="text" id="name"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:280:13
    |
278 |         """Test detecting heading hierarchy issues."""
279 |         with agent_dir_on_path():
280 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
281 |         analyzer = AccessibilityAgent()
282 |         # Page starts with h2 instead of h1
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:292:13
    |
290 |         """Test detecting click handlers without keyboard support."""
291 |         with agent_dir_on_path():
292 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
293 |         analyzer = AccessibilityAgent()
294 |         js_content = '<button onClick={handleClick}>Click me</button>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:303:13
    |
301 |         """Test detecting interactive divs without proper roles."""
302 |         with agent_dir_on_path():
303 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
304 |         analyzer = AccessibilityAgent()
305 |         js_content = '<div onClick={handleClick}>Clickable</div>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:314:13
    |
312 |         """Test color contrast check with high contrast."""
313 |         with agent_dir_on_path():
314 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
315 |         analyzer = AccessibilityAgent()
316 |         result = analyzer.check_color_contrast("#000000", "#FFFFFF")
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:324:13
    |
322 |         """Test color contrast check with low contrast."""
323 |         with agent_dir_on_path():
324 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
325 |         analyzer = AccessibilityAgent()
326 |         result = analyzer.check_color_contrast("#777777", "#999999")
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:332:13
    |
330 |         """Test color contrast check with large text requirements."""
331 |         with agent_dir_on_path():
332 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
333 |         analyzer = AccessibilityAgent()
334 |         result = analyzer.check_color_contrast("#555555", "#FFFFFF", is_large_text=True)
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:341:13
    |
339 |         """Test filtering issues by severity."""
340 |         with agent_dir_on_path():
341 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
342 |         analyzer = AccessibilityAgent()
343 |         html_content = '<html><body><img src="test.jpg"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:354:13
    |
352 |         """Test filtering issues by WCAG level."""
353 |         with agent_dir_on_path():
354 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
355 |         analyzer = AccessibilityAgent()
356 |         html_content = '<html><body><img src="test.jpg"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:364:13
    |
362 |         """Test enabling and disabling rules."""
363 |         with agent_dir_on_path():
364 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
365 |         analyzer = AccessibilityAgent()
366 |         analyzer.disable_rule("1.1.1")
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:374:13
    |
372 |         """Test compliance score is calculated correctly."""
373 |         with agent_dir_on_path():
374 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
375 |         analyzer = AccessibilityAgent()
376 |         # Clean HTML should have high score
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:393:13
    |
391 |         """Test analyzing nonexistent file returns empty report."""
392 |         with agent_dir_on_path():
393 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
394 |         analyzer = AccessibilityAgent()
395 |         report = analyzer.analyze_file(str(tmp_path / "nonexistent.html"))
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:402:13
    |
400 |         """Test analyzing HTML file."""
401 |         with agent_dir_on_path():
402 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
403 |         html_file: Path = tmp_path / "test.html"
404 |         html_file.write_text('<html><body><img src="x.jpg"></body></html>')
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:412:13
    |
410 |         """Test analyzing Python UI code."""
411 |         with agent_dir_on_path():
412 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
413 |         analyzer = AccessibilityAgent()
414 |         python_content = '''
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:425:13
    |
423 |         """Test that recommendations are generated."""
424 |         with agent_dir_on_path():
425 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
426 |         analyzer = AccessibilityAgent()
427 |         html_content = '<html><body><img src="test.jpg"></body></html>'
    |
help: Remove assignment to unused variable `mod`

F841 Local variable `mod` is assigned to but never used
   --> tests\unit\logic\test_coder_CORE_UNIT.py:489:13
    |
487 |         """Test generating Python code."""
488 |         with agent_dir_on_path():
489 |             mod: sys.ModuleType = load_agent_module("src/logic/agents/development/CoderAgent.py")
    |             ^^^
490 |
491 |         target: Path = tmp_path / "test.py"
    |
help: Remove assignment to unused variable `mod`

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
  --> tests\unit\logic\test_coder_UNIT.py:8:1
   |
 6 | from pathlib import Path
 7 | import sys
 8 | from tests.utils.agent_test_utils import *  # Added for modular test support
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 9 |
10 | # Try to import test utilities
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\logic\test_coder_UNIT.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import: `tests.utils.agent_test_utils.load_module_from_path`

F405 `mod` may be undefined, or defined from star imports
  --> tests\unit\logic\test_coder_UNIT.py:32:17
   |
30 |             sys.path.remove(str(AGENT_DIR))
31 |
32 |         agent = mod.CoderAgent(str(target))
   |                 ^^^
33 |         lang = agent.detect_language()
   |

F405 `target` may be undefined, or defined from star imports
  --> tests\unit\logic\test_coder_UNIT.py:32:36
   |
30 |             sys.path.remove(str(AGENT_DIR))
31 |
32 |         agent = mod.CoderAgent(str(target))
   |                                    ^^^^^^
33 |         lang = agent.detect_language()
   |

F405 `mod` may be undefined, or defined from star imports
  --> tests\unit\logic\test_coder_UNIT.py:35:24
   |
33 |         lang = agent.detect_language()
34 |
35 |         assert lang == mod.CodeLanguage.PYTHON
   |                        ^^^
36 |
37 |     def test_generate_javascript_code(self, tmp_path: Path) -> None:
   |

F405 `TestABComparisonEngine` may be undefined, or defined from star imports
 --> tests\unit\observability\__init__.py:5:5
  |
4 | __all__ = [
5 |     "TestABComparisonEngine",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^
6 |     "TestAggregation",
7 |     "TestAggregationAdvanced",
  |

F405 `TestAggregation` may be undefined, or defined from star imports
 --> tests\unit\observability\__init__.py:6:5
  |
4 | __all__ = [
5 |     "TestABComparisonEngine",
6 |     "TestAggregation",
  |     ^^^^^^^^^^^^^^^^^
7 |     "TestAggregationAdvanced",
8 |     "TestAlertSeverity",
  |

F405 `TestAggregationAdvanced` may be undefined, or defined from star imports
 --> tests\unit\observability\__init__.py:7:5
  |
5 |     "TestABComparisonEngine",
6 |     "TestAggregation",
7 |     "TestAggregationAdvanced",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^
8 |     "TestAlertSeverity",
9 |     "TestAlerting",
  |

F405 `TestAlertSeverity` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:8:5
   |
 6 |     "TestAggregation",
 7 |     "TestAggregationAdvanced",
 8 |     "TestAlertSeverity",
   |     ^^^^^^^^^^^^^^^^^^^
 9 |     "TestAlerting",
10 |     "TestAnnotationManager",
   |

F405 `TestAlerting` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:9:5
   |
 7 |     "TestAggregationAdvanced",
 8 |     "TestAlertSeverity",
 9 |     "TestAlerting",
   |     ^^^^^^^^^^^^^^
10 |     "TestAnnotationManager",
11 |     "TestAnomalyDetection",
   |

F405 `TestAnnotationManager` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:10:5
   |
 8 |     "TestAlertSeverity",
 9 |     "TestAlerting",
10 |     "TestAnnotationManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
11 |     "TestAnomalyDetection",
12 |     "TestBenchmarking",
   |

F405 `TestAnomalyDetection` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:11:5
   |
 9 |     "TestAlerting",
10 |     "TestAnnotationManager",
11 |     "TestAnomalyDetection",
   |     ^^^^^^^^^^^^^^^^^^^^^^
12 |     "TestBenchmarking",
13 |     "TestBenchmarkingAdvanced",
   |

F405 `TestBenchmarking` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:12:5
   |
10 |     "TestAnnotationManager",
11 |     "TestAnomalyDetection",
12 |     "TestBenchmarking",
   |     ^^^^^^^^^^^^^^^^^^
13 |     "TestBenchmarkingAdvanced",
14 |     "TestCSVExport",
   |

F405 `TestBenchmarkingAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:13:5
   |
11 |     "TestAnomalyDetection",
12 |     "TestBenchmarking",
13 |     "TestBenchmarkingAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
14 |     "TestCSVExport",
15 |     "TestCaching",
   |

F405 `TestCSVExport` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:14:5
   |
12 |     "TestBenchmarking",
13 |     "TestBenchmarkingAdvanced",
14 |     "TestCSVExport",
   |     ^^^^^^^^^^^^^^^
15 |     "TestCaching",
16 |     "TestCachingAdvanced",
   |

F405 `TestCaching` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:15:5
   |
13 |     "TestBenchmarkingAdvanced",
14 |     "TestCSVExport",
15 |     "TestCaching",
   |     ^^^^^^^^^^^^^
16 |     "TestCachingAdvanced",
17 |     "TestCloudExporter",
   |

F405 `TestCachingAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:16:5
   |
14 |     "TestCSVExport",
15 |     "TestCaching",
16 |     "TestCachingAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^
17 |     "TestCloudExporter",
18 |     "TestComparison",
   |

F405 `TestCloudExporter` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:17:5
   |
15 |     "TestCaching",
16 |     "TestCachingAdvanced",
17 |     "TestCloudExporter",
   |     ^^^^^^^^^^^^^^^^^^^
18 |     "TestComparison",
19 |     "TestComparisonReports",
   |

F405 `TestComparison` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:18:5
   |
16 |     "TestCachingAdvanced",
17 |     "TestCloudExporter",
18 |     "TestComparison",
   |     ^^^^^^^^^^^^^^^^
19 |     "TestComparisonReports",
20 |     "TestCompression",
   |

F405 `TestComparisonReports` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:19:5
   |
17 |     "TestCloudExporter",
18 |     "TestComparison",
19 |     "TestComparisonReports",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
20 |     "TestCompression",
21 |     "TestCorrelationAnalyzer",
   |

F405 `TestCompression` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:20:5
   |
18 |     "TestComparison",
19 |     "TestComparisonReports",
20 |     "TestCompression",
   |     ^^^^^^^^^^^^^^^^^
21 |     "TestCorrelationAnalyzer",
22 |     "TestCoverageMetrics",
   |

F405 `TestCorrelationAnalyzer` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:21:5
   |
19 |     "TestComparisonReports",
20 |     "TestCompression",
21 |     "TestCorrelationAnalyzer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
22 |     "TestCoverageMetrics",
23 |     "TestCustomMetrics",
   |

F405 `TestCoverageMetrics` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:22:5
   |
20 |     "TestCompression",
21 |     "TestCorrelationAnalyzer",
22 |     "TestCoverageMetrics",
   |     ^^^^^^^^^^^^^^^^^^^^^
23 |     "TestCustomMetrics",
24 |     "TestDerivedMetricCalculator",
   |

F405 `TestCustomMetrics` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:23:5
   |
21 |     "TestCorrelationAnalyzer",
22 |     "TestCoverageMetrics",
23 |     "TestCustomMetrics",
   |     ^^^^^^^^^^^^^^^^^^^
24 |     "TestDerivedMetricCalculator",
25 |     "TestDocstrings",
   |

F405 `TestDerivedMetricCalculator` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:24:5
   |
22 |     "TestCoverageMetrics",
23 |     "TestCustomMetrics",
24 |     "TestDerivedMetricCalculator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
25 |     "TestDocstrings",
26 |     "TestEdgeCases",
   |

F405 `TestDocstrings` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:25:5
   |
23 |     "TestCustomMetrics",
24 |     "TestDerivedMetricCalculator",
25 |     "TestDocstrings",
   |     ^^^^^^^^^^^^^^^^
26 |     "TestEdgeCases",
27 |     "TestExportFormats",
   |

F405 `TestEdgeCases` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:26:5
   |
24 |     "TestDerivedMetricCalculator",
25 |     "TestDocstrings",
26 |     "TestEdgeCases",
   |     ^^^^^^^^^^^^^^^
27 |     "TestExportFormats",
28 |     "TestExportFormatsAdvanced",
   |

F405 `TestExportFormats` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:27:5
   |
25 |     "TestDocstrings",
26 |     "TestEdgeCases",
27 |     "TestExportFormats",
   |     ^^^^^^^^^^^^^^^^^^^
28 |     "TestExportFormatsAdvanced",
29 |     "TestFiltering",
   |

F405 `TestExportFormatsAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:28:5
   |
26 |     "TestEdgeCases",
27 |     "TestExportFormats",
28 |     "TestExportFormatsAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
29 |     "TestFiltering",
30 |     "TestForecasting",
   |

F405 `TestFiltering` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:29:5
   |
27 |     "TestExportFormats",
28 |     "TestExportFormatsAdvanced",
29 |     "TestFiltering",
   |     ^^^^^^^^^^^^^^^
30 |     "TestForecasting",
31 |     "TestIntegration",
   |

F405 `TestForecasting` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:30:5
   |
28 |     "TestExportFormatsAdvanced",
29 |     "TestFiltering",
30 |     "TestForecasting",
   |     ^^^^^^^^^^^^^^^^^
31 |     "TestIntegration",
32 |     "TestIntegrationAdvanced",
   |

F405 `TestIntegration` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:31:5
   |
29 |     "TestFiltering",
30 |     "TestForecasting",
31 |     "TestIntegration",
   |     ^^^^^^^^^^^^^^^^^
32 |     "TestIntegrationAdvanced",
33 |     "TestMetricFiltering",
   |

F405 `TestIntegrationAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:32:5
   |
30 |     "TestForecasting",
31 |     "TestIntegration",
32 |     "TestIntegrationAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
33 |     "TestMetricFiltering",
34 |     "TestMetricNamespaceManager",
   |

F405 `TestMetricFiltering` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:33:5
   |
31 |     "TestIntegration",
32 |     "TestIntegrationAdvanced",
33 |     "TestMetricFiltering",
   |     ^^^^^^^^^^^^^^^^^^^^^
34 |     "TestMetricNamespaceManager",
35 |     "TestMetricType",
   |

F405 `TestMetricNamespaceManager` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:34:5
   |
32 |     "TestIntegrationAdvanced",
33 |     "TestMetricFiltering",
34 |     "TestMetricNamespaceManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
35 |     "TestMetricType",
36 |     "TestPathLibUsage",
   |

F405 `TestMetricType` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:35:5
   |
33 |     "TestMetricFiltering",
34 |     "TestMetricNamespaceManager",
35 |     "TestMetricType",
   |     ^^^^^^^^^^^^^^^^
36 |     "TestPathLibUsage",
37 |     "TestPerformanceMetrics",
   |

F405 `TestPathLibUsage` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:36:5
   |
34 |     "TestMetricNamespaceManager",
35 |     "TestMetricType",
36 |     "TestPathLibUsage",
   |     ^^^^^^^^^^^^^^^^^^
37 |     "TestPerformanceMetrics",
38 |     "TestRealTimeStatsStreaming",
   |

F405 `TestPerformanceMetrics` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:37:5
   |
35 |     "TestMetricType",
36 |     "TestPathLibUsage",
37 |     "TestPerformanceMetrics",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
38 |     "TestRealTimeStatsStreaming",
39 |     "TestReporting",
   |

F405 `TestRealTimeStatsStreaming` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:38:5
   |
36 |     "TestPathLibUsage",
37 |     "TestPerformanceMetrics",
38 |     "TestRealTimeStatsStreaming",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
39 |     "TestReporting",
40 |     "TestReportingWithInsights",
   |

F405 `TestReporting` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:39:5
   |
37 |     "TestPerformanceMetrics",
38 |     "TestRealTimeStatsStreaming",
39 |     "TestReporting",
   |     ^^^^^^^^^^^^^^^
40 |     "TestReportingWithInsights",
41 |     "TestRetentionPolicies",
   |

F405 `TestReportingWithInsights` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:40:5
   |
38 |     "TestRealTimeStatsStreaming",
39 |     "TestReporting",
40 |     "TestReportingWithInsights",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
41 |     "TestRetentionPolicies",
42 |     "TestSession7Dataclasses",
   |

F405 `TestRetentionPolicies` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:41:5
   |
39 |     "TestReporting",
40 |     "TestReportingWithInsights",
41 |     "TestRetentionPolicies",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
42 |     "TestSession7Dataclasses",
43 |     "TestSession7Enums",
   |

F405 `TestSession7Dataclasses` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:42:5
   |
40 |     "TestReportingWithInsights",
41 |     "TestRetentionPolicies",
42 |     "TestSession7Dataclasses",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
43 |     "TestSession7Enums",
44 |     "TestSnapshots",
   |

F405 `TestSession7Enums` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:43:5
   |
41 |     "TestRetentionPolicies",
42 |     "TestSession7Dataclasses",
43 |     "TestSession7Enums",
   |     ^^^^^^^^^^^^^^^^^^^
44 |     "TestSnapshots",
45 |     "TestStatisticalSummaries",
   |

F405 `TestSnapshots` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:44:5
   |
42 |     "TestSession7Dataclasses",
43 |     "TestSession7Enums",
44 |     "TestSnapshots",
   |     ^^^^^^^^^^^^^^^
45 |     "TestStatisticalSummaries",
46 |     "TestStatisticalSummariesAdvanced",
   |

F405 `TestStatisticalSummaries` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:45:5
   |
43 |     "TestSession7Enums",
44 |     "TestSnapshots",
45 |     "TestStatisticalSummaries",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
46 |     "TestStatisticalSummariesAdvanced",
47 |     "TestStatsABComparison",
   |

F405 `TestStatisticalSummariesAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:46:5
   |
44 |     "TestSnapshots",
45 |     "TestStatisticalSummaries",
46 |     "TestStatisticalSummariesAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
47 |     "TestStatsABComparison",
48 |     "TestStatsAPIServer",
   |

F405 `TestStatsABComparison` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:47:5
   |
45 |     "TestStatisticalSummaries",
46 |     "TestStatisticalSummariesAdvanced",
47 |     "TestStatsABComparison",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
48 |     "TestStatsAPIServer",
49 |     "TestStatsAccessControl",
   |

F405 `TestStatsAPIServer` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:48:5
   |
46 |     "TestStatisticalSummariesAdvanced",
47 |     "TestStatsABComparison",
48 |     "TestStatsAPIServer",
   |     ^^^^^^^^^^^^^^^^^^^^
49 |     "TestStatsAccessControl",
50 |     "TestStatsAgent",
   |

F405 `TestStatsAccessControl` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:49:5
   |
47 |     "TestStatsABComparison",
48 |     "TestStatsAPIServer",
49 |     "TestStatsAccessControl",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
50 |     "TestStatsAgent",
51 |     "TestStatsAnnotationPersistence",
   |

F405 `TestStatsAgent` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:50:5
   |
48 |     "TestStatsAPIServer",
49 |     "TestStatsAccessControl",
50 |     "TestStatsAgent",
   |     ^^^^^^^^^^^^^^^^
51 |     "TestStatsAnnotationPersistence",
52 |     "TestStatsBackupAndRestore",
   |

F405 `TestStatsAnnotationPersistence` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:51:5
   |
49 |     "TestStatsAccessControl",
50 |     "TestStatsAgent",
51 |     "TestStatsAnnotationPersistence",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
52 |     "TestStatsBackupAndRestore",
53 |     "TestStatsChangeNotificationSystem",
   |

F405 `TestStatsBackupAndRestore` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:52:5
   |
50 |     "TestStatsAgent",
51 |     "TestStatsAnnotationPersistence",
52 |     "TestStatsBackupAndRestore",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
53 |     "TestStatsChangeNotificationSystem",
54 |     "TestStatsCompressionAlgorithms",
   |

F405 `TestStatsChangeNotificationSystem` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:53:5
   |
51 |     "TestStatsAnnotationPersistence",
52 |     "TestStatsBackupAndRestore",
53 |     "TestStatsChangeNotificationSystem",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
54 |     "TestStatsCompressionAlgorithms",
55 |     "TestStatsExportToMonitoringPlatforms",
   |

F405 `TestStatsCompressionAlgorithms` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:54:5
   |
52 |     "TestStatsBackupAndRestore",
53 |     "TestStatsChangeNotificationSystem",
54 |     "TestStatsCompressionAlgorithms",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
55 |     "TestStatsExportToMonitoringPlatforms",
56 |     "TestStatsFederation",
   |

F405 `TestStatsExportToMonitoringPlatforms` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:55:5
   |
53 |     "TestStatsChangeNotificationSystem",
54 |     "TestStatsCompressionAlgorithms",
55 |     "TestStatsExportToMonitoringPlatforms",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
56 |     "TestStatsFederation",
57 |     "TestStatsFederationAcrossSources",
   |

F405 `TestStatsFederation` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:56:5
   |
54 |     "TestStatsCompressionAlgorithms",
55 |     "TestStatsExportToMonitoringPlatforms",
56 |     "TestStatsFederation",
   |     ^^^^^^^^^^^^^^^^^^^^^
57 |     "TestStatsFederationAcrossSources",
58 |     "TestStatsForecastingAccuracy",
   |

F405 `TestStatsFederationAcrossSources` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:57:5
   |
55 |     "TestStatsExportToMonitoringPlatforms",
56 |     "TestStatsFederation",
57 |     "TestStatsFederationAcrossSources",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
58 |     "TestStatsForecastingAccuracy",
59 |     "TestStatsMetricFormulaCalculation",
   |

F405 `TestStatsForecastingAccuracy` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:58:5
   |
56 |     "TestStatsFederation",
57 |     "TestStatsFederationAcrossSources",
58 |     "TestStatsForecastingAccuracy",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
59 |     "TestStatsMetricFormulaCalculation",
60 |     "TestStatsNamespaceIsolation",
   |

F405 `TestStatsMetricFormulaCalculation` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:59:5
   |
57 |     "TestStatsFederationAcrossSources",
58 |     "TestStatsForecastingAccuracy",
59 |     "TestStatsMetricFormulaCalculation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
60 |     "TestStatsNamespaceIsolation",
61 |     "TestStatsQueryPerformance",
   |

F405 `TestStatsNamespaceIsolation` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:60:5
   |
58 |     "TestStatsForecastingAccuracy",
59 |     "TestStatsMetricFormulaCalculation",
60 |     "TestStatsNamespaceIsolation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
61 |     "TestStatsQueryPerformance",
62 |     "TestStatsRetentionPolicyEnforcement",
   |

F405 `TestStatsQueryPerformance` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:61:5
   |
59 |     "TestStatsMetricFormulaCalculation",
60 |     "TestStatsNamespaceIsolation",
61 |     "TestStatsQueryPerformance",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
62 |     "TestStatsRetentionPolicyEnforcement",
63 |     "TestStatsRollup",
   |

F405 `TestStatsRetentionPolicyEnforcement` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:62:5
   |
60 |     "TestStatsNamespaceIsolation",
61 |     "TestStatsQueryPerformance",
62 |     "TestStatsRetentionPolicyEnforcement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
63 |     "TestStatsRollup",
64 |     "TestStatsRollupCalculations",
   |

F405 `TestStatsRollup` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:63:5
   |
61 |     "TestStatsQueryPerformance",
62 |     "TestStatsRetentionPolicyEnforcement",
63 |     "TestStatsRollup",
   |     ^^^^^^^^^^^^^^^^^
64 |     "TestStatsRollupCalculations",
65 |     "TestStatsSnapshotCreationAndRestore",
   |

F405 `TestStatsRollupCalculations` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:64:5
   |
62 |     "TestStatsRetentionPolicyEnforcement",
63 |     "TestStatsRollup",
64 |     "TestStatsRollupCalculations",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
65 |     "TestStatsSnapshotCreationAndRestore",
66 |     "TestStatsStreamer",
   |

F405 `TestStatsSnapshotCreationAndRestore` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:65:5
   |
63 |     "TestStatsRollup",
64 |     "TestStatsRollupCalculations",
65 |     "TestStatsSnapshotCreationAndRestore",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
66 |     "TestStatsStreamer",
67 |     "TestStatsSubscriptionAndNotification",
   |

F405 `TestStatsStreamer` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:66:5
   |
64 |     "TestStatsRollupCalculations",
65 |     "TestStatsSnapshotCreationAndRestore",
66 |     "TestStatsStreamer",
   |     ^^^^^^^^^^^^^^^^^^^
67 |     "TestStatsSubscriptionAndNotification",
68 |     "TestStatsThresholdAlerting",
   |

F405 `TestStatsSubscriptionAndNotification` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:67:5
   |
65 |     "TestStatsSnapshotCreationAndRestore",
66 |     "TestStatsStreamer",
67 |     "TestStatsSubscriptionAndNotification",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
68 |     "TestStatsThresholdAlerting",
69 |     "TestSubscriptionManager",
   |

F405 `TestStatsThresholdAlerting` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:68:5
   |
66 |     "TestStatsStreamer",
67 |     "TestStatsSubscriptionAndNotification",
68 |     "TestStatsThresholdAlerting",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
69 |     "TestSubscriptionManager",
70 |     "TestThresholdsAndAlerting",
   |

F405 `TestSubscriptionManager` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:69:5
   |
67 |     "TestStatsSubscriptionAndNotification",
68 |     "TestStatsThresholdAlerting",
69 |     "TestSubscriptionManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
70 |     "TestThresholdsAndAlerting",
71 |     "TestTimeSeries",
   |

F405 `TestThresholdsAndAlerting` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:70:5
   |
68 |     "TestStatsThresholdAlerting",
69 |     "TestSubscriptionManager",
70 |     "TestThresholdsAndAlerting",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
71 |     "TestTimeSeries",
72 |     "TestTimeSeriesStorage",
   |

F405 `TestTimeSeries` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:71:5
   |
69 |     "TestSubscriptionManager",
70 |     "TestThresholdsAndAlerting",
71 |     "TestTimeSeries",
   |     ^^^^^^^^^^^^^^^^
72 |     "TestTimeSeriesStorage",
73 |     "TestTrendAnalysis",
   |

F405 `TestTimeSeriesStorage` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:72:5
   |
70 |     "TestThresholdsAndAlerting",
71 |     "TestTimeSeries",
72 |     "TestTimeSeriesStorage",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
73 |     "TestTrendAnalysis",
74 |     "TestTrendAnalysisAdvanced",
   |

F405 `TestTrendAnalysis` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:73:5
   |
71 |     "TestTimeSeries",
72 |     "TestTimeSeriesStorage",
73 |     "TestTrendAnalysis",
   |     ^^^^^^^^^^^^^^^^^^^
74 |     "TestTrendAnalysisAdvanced",
75 |     "TestValidation",
   |

F405 `TestTrendAnalysisAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:74:5
   |
72 |     "TestTimeSeriesStorage",
73 |     "TestTrendAnalysis",
74 |     "TestTrendAnalysisAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
75 |     "TestValidation",
76 |     "TestVisualization",
   |

F405 `TestValidation` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:75:5
   |
73 |     "TestTrendAnalysis",
74 |     "TestTrendAnalysisAdvanced",
75 |     "TestValidation",
   |     ^^^^^^^^^^^^^^^^
76 |     "TestVisualization",
77 |     "TestVisualizationAdvanced",
   |

F405 `TestVisualization` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:76:5
   |
74 |     "TestTrendAnalysisAdvanced",
75 |     "TestValidation",
76 |     "TestVisualization",
   |     ^^^^^^^^^^^^^^^^^^^
77 |     "TestVisualizationAdvanced",
78 |     "TestVisualizationGeneration",
   |

F405 `TestVisualizationAdvanced` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:77:5
   |
75 |     "TestValidation",
76 |     "TestVisualization",
77 |     "TestVisualizationAdvanced",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
78 |     "TestVisualizationGeneration",
79 | ]
   |

F405 `TestVisualizationGeneration` may be undefined, or defined from star imports
  --> tests\unit\observability\__init__.py:78:5
   |
76 |     "TestVisualization",
77 |     "TestVisualizationAdvanced",
78 |     "TestVisualizationGeneration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
79 | ]
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\advanced.py:17:73
   |
15 | # Try to import test utilities
16 | try:
17 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
18 | except ImportError:
19 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\advanced.py:17:96
   |
15 | # Try to import test utilities
16 | try:
17 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
18 | except ImportError:
19 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\advanced.py:23:32
   |
22 |     class agent_sys_path:
23 |         def __enter__(self) -> Self:
   |                                ^^^^
24 |
25 |             return self
   |

F841 Local variable `AGENT_DIR` is assigned to but never used
  --> tests\unit\observability\conftest.py:35:9
   |
33 |     except ImportError:
34 |         # Fallback to loading it manually if path setup is tricky
35 |         AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |         ^^^^^^^^^
36 |
37 |         import observability.reports as reports
   |
help: Remove assignment to unused variable `AGENT_DIR`

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\edge_cases.py:14:73
   |
12 | # Try to import test utilities
13 | try:
14 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
15 | except ImportError:
16 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\edge_cases.py:14:96
   |
12 | # Try to import test utilities
13 | try:
14 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
15 | except ImportError:
16 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\edge_cases.py:20:32
   |
19 |     class agent_sys_path:
20 |         def __enter__(self) -> Self:
   |                                ^^^^
21 |
22 |             return self
   |

F401 `tests.utils.agent_test_utils.agent_sys_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_CORE.py:10:57
   |
 8 | # Import test utilities
 9 | try:
10 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                         ^^^^^^^^^^^^^^
11 | except ImportError:
12 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_CORE.py:10:73
   |
 8 | # Import test utilities
 9 | try:
10 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
11 | except ImportError:
12 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_CORE.py:10:96
   |
 8 | # Import test utilities
 9 | try:
10 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
11 | except ImportError:
12 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_INTEGRATION.py:16:73
   |
14 | # Try to import test utilities
15 | try:
16 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
17 | except ImportError:
18 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_INTEGRATION.py:16:96
   |
14 | # Try to import test utilities
15 | try:
16 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
17 | except ImportError:
18 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\test_reports_INTEGRATION.py:22:32
   |
21 |     class agent_sys_path:
22 |         def __enter__(self) -> Self:
   |                                ^^^^
23 |
24 |             return self
   |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
 --> tests\unit\observability\test_reports_LEGACY.py:3:5
  |
1 | from typing import Any
2 | try:
3 |     from tests.utils.agent_test_utils import *
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4 | except ImportError:
5 |     pass
  |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_PERFORMANCE.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_PERFORMANCE.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\test_reports_PERFORMANCE.py:18:32
   |
17 |     class agent_sys_path:
18 |         def __enter__(self) -> Self:
   |                                ^^^^
19 |
20 |             return self
   |

F401 `tests.utils.agent_test_utils.agent_sys_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_SHELL.py:12:57
   |
10 | # Import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                         ^^^^^^^^^^^^^^
13 | except ImportError:
14 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_SHELL.py:12:73
   |
10 | # Import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_SHELL.py:12:96
   |
10 | # Import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_reports_UNIT.py:13:57
   |
11 | # Import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, load_module_from_path
   |                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
   |
help: Remove unused import: `tests.utils.agent_test_utils.load_module_from_path`

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_stats_INTEGRATION.py:13:73
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_stats_INTEGRATION.py:13:96
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\test_stats_INTEGRATION.py:19:32
   |
18 |     class agent_sys_path:
19 |         def __enter__(self) -> Self:
   |                                ^^^^
20 |
21 |             return self
   |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
 --> tests\unit\observability\test_stats_LEGACY.py:4:5
  |
2 | from pathlib import Path
3 | try:
4 |     from tests.utils.agent_test_utils import *
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
5 | except ImportError:
6 |     pass
  |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\observability\test_stats_LEGACY.py:12:10
   |
11 | def test_stats_agent_counts_files(tmp_path: Path) -> None:
12 |     with agent_dir_on_path():
   |          ^^^^^^^^^^^^^^^^^
13 |         from src.observability.stats.agents import StatsAgent
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_stats_PERFORMANCE.py:13:73
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\observability\test_stats_PERFORMANCE.py:13:96
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\observability\test_stats_PERFORMANCE.py:19:32
   |
18 |     class agent_sys_path:
19 |         def __enter__(self) -> Self:
   |                                ^^^^
20 |
21 |             return self
   |

F841 Local variable `category` is assigned to but never used
   --> tests\unit\test_error_mapping_core.py:185:13
    |
183 |         """Test that error codes follow category numbering (10xx, 20xx, etc)."""
184 |         for code in ErrorMappingCore.ERROR_CODES.values():
185 |             category = int(code[3])  # Extract middle digit
    |             ^^^^^^^^
186 |             code_num = int(code[3:])
187 |             # Verify it's in format PA-XYYY where X is category
    |
help: Remove assignment to unused variable `category`

F841 Local variable `p95` is assigned to but never used
   --> tests\unit\test_metrics_core.py:136:9
    |
134 |         core = StatsRollupCore()
135 |         p50 = core.rollup_p50(values)
136 |         p95 = core.rollup_p95(values)
    |         ^^^
137 |         p99 = core.rollup_p99(values)
    |
help: Remove assignment to unused variable `p95`

F841 Local variable `p99` is assigned to but never used
   --> tests\unit\test_metrics_core.py:137:9
    |
135 |         p50 = core.rollup_p50(values)
136 |         p95 = core.rollup_p95(values)
137 |         p99 = core.rollup_p99(values)
    |         ^^^
138 |
139 |         assert core.rollup_min(values) <= p50 <= core.rollup_max(values)
    |
help: Remove assignment to unused variable `p99`

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  --> tests\unit\test_privacy_core.py:37:16
   |
35 |         # Just ensure it doesn't crash and returns same structure type
36 |         result = PrivacyCore.scan_log_entry(data)
37 |         assert type(result) == type(data)
   |                ^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

F841 Local variable `base` is assigned to but never used
  --> tests\unit\test_rust_core_parity.py:26:9
   |
24 |     def test_memory_logic(self):
25 |         # Python Logic
26 |         base = 0.5
   |         ^^^^
27 |         success = 0.5 + 0.2
28 |         failure = 0.5 - 0.3
   |
help: Remove assignment to unused variable `base`

F405 `TestAgentAssertions` may be undefined, or defined from star imports
 --> tests\unit\test_utils\__init__.py:5:5
  |
4 | __all__ = [
5 |     "TestAgentAssertions",
  |     ^^^^^^^^^^^^^^^^^^^^^
6 |     "TestAssertionHelperFunctions",
7 |     "TestAssertionHelpers",
  |

F405 `TestAssertionHelperFunctions` may be undefined, or defined from star imports
 --> tests\unit\test_utils\__init__.py:6:5
  |
4 | __all__ = [
5 |     "TestAgentAssertions",
6 |     "TestAssertionHelperFunctions",
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
7 |     "TestAssertionHelpers",
8 |     "TestBaselineManager",
  |

F405 `TestAssertionHelpers` may be undefined, or defined from star imports
 --> tests\unit\test_utils\__init__.py:7:5
  |
5 |     "TestAgentAssertions",
6 |     "TestAssertionHelperFunctions",
7 |     "TestAssertionHelpers",
  |     ^^^^^^^^^^^^^^^^^^^^^^
8 |     "TestBaselineManager",
9 |     "TestComparison",
  |

F405 `TestBaselineManager` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:8:5
   |
 6 |     "TestAssertionHelperFunctions",
 7 |     "TestAssertionHelpers",
 8 |     "TestBaselineManager",
   |     ^^^^^^^^^^^^^^^^^^^^^
 9 |     "TestComparison",
10 |     "TestContextManagers",
   |

F405 `TestComparison` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:9:5
   |
 7 |     "TestAssertionHelpers",
 8 |     "TestBaselineManager",
 9 |     "TestComparison",
   |     ^^^^^^^^^^^^^^^^
10 |     "TestContextManagers",
11 |     "TestCrossPlatformHelper",
   |

F405 `TestContextManagers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:10:5
   |
 8 |     "TestBaselineManager",
 9 |     "TestComparison",
10 |     "TestContextManagers",
   |     ^^^^^^^^^^^^^^^^^^^^^
11 |     "TestCrossPlatformHelper",
12 |     "TestDataGenerators",
   |

F405 `TestCrossPlatformHelper` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:11:5
   |
 9 |     "TestComparison",
10 |     "TestContextManagers",
11 |     "TestCrossPlatformHelper",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
12 |     "TestDataGenerators",
13 |     "TestDependencyContainer",
   |

F405 `TestDataGenerators` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:12:5
   |
10 |     "TestContextManagers",
11 |     "TestCrossPlatformHelper",
12 |     "TestDataGenerators",
   |     ^^^^^^^^^^^^^^^^^^^^
13 |     "TestDependencyContainer",
14 |     "TestExceptionHandling",
   |

F405 `TestDependencyContainer` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:13:5
   |
11 |     "TestCrossPlatformHelper",
12 |     "TestDataGenerators",
13 |     "TestDependencyContainer",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
14 |     "TestExceptionHandling",
15 |     "TestFileSystemIsolator",
   |

F405 `TestExceptionHandling` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:14:5
   |
12 |     "TestDataGenerators",
13 |     "TestDependencyContainer",
14 |     "TestExceptionHandling",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
15 |     "TestFileSystemIsolator",
16 |     "TestFixtureFactoryPatterns",
   |

F405 `TestFileSystemIsolator` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:15:5
   |
13 |     "TestDependencyContainer",
14 |     "TestExceptionHandling",
15 |     "TestFileSystemIsolator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
16 |     "TestFixtureFactoryPatterns",
17 |     "TestFixtureGenerator",
   |

F405 `TestFixtureFactoryPatterns` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:16:5
   |
14 |     "TestExceptionHandling",
15 |     "TestFileSystemIsolator",
16 |     "TestFixtureFactoryPatterns",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
17 |     "TestFixtureGenerator",
18 |     "TestFixtureHelpers",
   |

F405 `TestFixtureGenerator` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:17:5
   |
15 |     "TestFileSystemIsolator",
16 |     "TestFixtureFactoryPatterns",
17 |     "TestFixtureGenerator",
   |     ^^^^^^^^^^^^^^^^^^^^^^
18 |     "TestFixtureHelpers",
19 |     "TestFlakinessDetector",
   |

F405 `TestFixtureHelpers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:18:5
   |
16 |     "TestFixtureFactoryPatterns",
17 |     "TestFixtureGenerator",
18 |     "TestFixtureHelpers",
   |     ^^^^^^^^^^^^^^^^^^^^
19 |     "TestFlakinessDetector",
20 |     "TestIntegration",
   |

F405 `TestFlakinessDetector` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:19:5
   |
17 |     "TestFixtureGenerator",
18 |     "TestFixtureHelpers",
19 |     "TestFlakinessDetector",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
20 |     "TestIntegration",
21 |     "TestIsolationLevelEnum",
   |

F405 `TestIntegration` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:20:5
   |
18 |     "TestFixtureHelpers",
19 |     "TestFlakinessDetector",
20 |     "TestIntegration",
   |     ^^^^^^^^^^^^^^^^^
21 |     "TestIsolationLevelEnum",
22 |     "TestMockAIBackend",
   |

F405 `TestIsolationLevelEnum` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:21:5
   |
19 |     "TestFlakinessDetector",
20 |     "TestIntegration",
21 |     "TestIsolationLevelEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
22 |     "TestMockAIBackend",
23 |     "TestMockSystemResponseGeneration",
   |

F405 `TestMockAIBackend` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:22:5
   |
20 |     "TestIntegration",
21 |     "TestIsolationLevelEnum",
22 |     "TestMockAIBackend",
   |     ^^^^^^^^^^^^^^^^^^^
23 |     "TestMockSystemResponseGeneration",
24 |     "TestMockResponseDataclass",
   |

F405 `TestMockSystemResponseGeneration` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:23:5
   |
21 |     "TestIsolationLevelEnum",
22 |     "TestMockAIBackend",
23 |     "TestMockSystemResponseGeneration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
24 |     "TestMockResponseDataclass",
25 |     "TestMockResponseTypeEnum",
   |

F405 `TestMockResponseDataclass` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:24:5
   |
22 |     "TestMockAIBackend",
23 |     "TestMockSystemResponseGeneration",
24 |     "TestMockResponseDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
25 |     "TestMockResponseTypeEnum",
26 |     "TestMockingUtilities",
   |

F405 `TestMockResponseTypeEnum` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:25:5
   |
23 |     "TestMockSystemResponseGeneration",
24 |     "TestMockResponseDataclass",
25 |     "TestMockResponseTypeEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
26 |     "TestMockingUtilities",
27 |     "TestParallelTestExecutionHelpers",
   |

F405 `TestMockingUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:26:5
   |
24 |     "TestMockResponseDataclass",
25 |     "TestMockResponseTypeEnum",
26 |     "TestMockingUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^
27 |     "TestParallelTestExecutionHelpers",
28 |     "TestParallelTestRunner",
   |

F405 `TestParallelTestExecutionHelpers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:27:5
   |
25 |     "TestMockResponseTypeEnum",
26 |     "TestMockingUtilities",
27 |     "TestParallelTestExecutionHelpers",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
28 |     "TestParallelTestRunner",
29 |     "TestParameterizedTestGenerator",
   |

F405 `TestParallelTestRunner` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:28:5
   |
26 |     "TestMockingUtilities",
27 |     "TestParallelTestExecutionHelpers",
28 |     "TestParallelTestRunner",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
29 |     "TestParameterizedTestGenerator",
30 |     "TestParametrization",
   |

F405 `TestParameterizedTestGenerator` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:29:5
   |
27 |     "TestParallelTestExecutionHelpers",
28 |     "TestParallelTestRunner",
29 |     "TestParameterizedTestGenerator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
30 |     "TestParametrization",
31 |     "TestPerformanceMetricDataclass",
   |

F405 `TestParametrization` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:30:5
   |
28 |     "TestParallelTestRunner",
29 |     "TestParameterizedTestGenerator",
30 |     "TestParametrization",
   |     ^^^^^^^^^^^^^^^^^^^^^
31 |     "TestPerformanceMetricDataclass",
32 |     "TestPerformanceTracker",
   |

F405 `TestPerformanceMetricDataclass` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:31:5
   |
29 |     "TestParameterizedTestGenerator",
30 |     "TestParametrization",
31 |     "TestPerformanceMetricDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
32 |     "TestPerformanceTracker",
33 |     "TestPhase6Integration",
   |

F405 `TestPerformanceTracker` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:32:5
   |
30 |     "TestParametrization",
31 |     "TestPerformanceMetricDataclass",
32 |     "TestPerformanceTracker",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
33 |     "TestPhase6Integration",
34 |     "TestReporting",
   |

F405 `TestPhase6Integration` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:33:5
   |
31 |     "TestPerformanceMetricDataclass",
32 |     "TestPerformanceTracker",
33 |     "TestPhase6Integration",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
34 |     "TestReporting",
35 |     "TestSnapshotComparisonUtilities",
   |

F405 `TestReporting` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:34:5
   |
32 |     "TestPerformanceTracker",
33 |     "TestPhase6Integration",
34 |     "TestReporting",
   |     ^^^^^^^^^^^^^^^
35 |     "TestSnapshotComparisonUtilities",
36 |     "TestSnapshotManager",
   |

F405 `TestSnapshotComparisonUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:35:5
   |
33 |     "TestPhase6Integration",
34 |     "TestReporting",
35 |     "TestSnapshotComparisonUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
36 |     "TestSnapshotManager",
37 |     "TestTestCleanupHooks",
   |

F405 `TestSnapshotManager` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:36:5
   |
34 |     "TestReporting",
35 |     "TestSnapshotComparisonUtilities",
36 |     "TestSnapshotManager",
   |     ^^^^^^^^^^^^^^^^^^^^^
37 |     "TestTestCleanupHooks",
38 |     "TestTestConfigurationLoadingUtilities",
   |

F405 `TestTestCleanupHooks` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:37:5
   |
35 |     "TestSnapshotComparisonUtilities",
36 |     "TestSnapshotManager",
37 |     "TestTestCleanupHooks",
   |     ^^^^^^^^^^^^^^^^^^^^^^
38 |     "TestTestConfigurationLoadingUtilities",
39 |     "TestTestCoverageMeasurementHelpers",
   |

F405 `TestTestConfigurationLoadingUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:38:5
   |
36 |     "TestSnapshotManager",
37 |     "TestTestCleanupHooks",
38 |     "TestTestConfigurationLoadingUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
39 |     "TestTestCoverageMeasurementHelpers",
40 |     "TestTestDataCleaner",
   |

F405 `TestTestCoverageMeasurementHelpers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:39:5
   |
37 |     "TestTestCleanupHooks",
38 |     "TestTestConfigurationLoadingUtilities",
39 |     "TestTestCoverageMeasurementHelpers",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
40 |     "TestTestDataCleaner",
41 |     "TestTestDataGenerator",
   |

F405 `TestTestDataCleaner` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:40:5
   |
38 |     "TestTestConfigurationLoadingUtilities",
39 |     "TestTestCoverageMeasurementHelpers",
40 |     "TestTestDataCleaner",
   |     ^^^^^^^^^^^^^^^^^^^^^
41 |     "TestTestDataGenerator",
42 |     "TestTestDataSeedingUtilities",
   |

F405 `TestTestDataGenerator` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:41:5
   |
39 |     "TestTestCoverageMeasurementHelpers",
40 |     "TestTestDataCleaner",
41 |     "TestTestDataGenerator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^
42 |     "TestTestDataSeedingUtilities",
43 |     "TestTestDataTypeEnum",
   |

F405 `TestTestDataSeedingUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:42:5
   |
40 |     "TestTestDataCleaner",
41 |     "TestTestDataGenerator",
42 |     "TestTestDataSeedingUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
43 |     "TestTestDataTypeEnum",
44 |     "TestTestDependencyManagement",
   |

F405 `TestTestDataTypeEnum` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:43:5
   |
41 |     "TestTestDataGenerator",
42 |     "TestTestDataSeedingUtilities",
43 |     "TestTestDataTypeEnum",
   |     ^^^^^^^^^^^^^^^^^^^^^^
44 |     "TestTestDependencyManagement",
45 |     "TestTestEnvironmentDetection",
   |

F405 `TestTestDependencyManagement` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:44:5
   |
42 |     "TestTestDataSeedingUtilities",
43 |     "TestTestDataTypeEnum",
44 |     "TestTestDependencyManagement",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
45 |     "TestTestEnvironmentDetection",
46 |     "TestTestFixtureDataclass",
   |

F405 `TestTestEnvironmentDetection` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:45:5
   |
43 |     "TestTestDataTypeEnum",
44 |     "TestTestDependencyManagement",
45 |     "TestTestEnvironmentDetection",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
46 |     "TestTestFixtureDataclass",
47 |     "TestTestIsolationMechanisms",
   |

F405 `TestTestFixtureDataclass` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:46:5
   |
44 |     "TestTestDependencyManagement",
45 |     "TestTestEnvironmentDetection",
46 |     "TestTestFixtureDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
47 |     "TestTestIsolationMechanisms",
48 |     "TestTestLogCaptureUtilities",
   |

F405 `TestTestIsolationMechanisms` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:47:5
   |
45 |     "TestTestEnvironmentDetection",
46 |     "TestTestFixtureDataclass",
47 |     "TestTestIsolationMechanisms",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
48 |     "TestTestLogCaptureUtilities",
49 |     "TestTestLogger",
   |

F405 `TestTestLogCaptureUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:48:5
   |
46 |     "TestTestFixtureDataclass",
47 |     "TestTestIsolationMechanisms",
48 |     "TestTestLogCaptureUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
49 |     "TestTestLogger",
50 |     "TestTestOutputFormattingUtilities",
   |

F405 `TestTestLogger` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:49:5
   |
47 |     "TestTestIsolationMechanisms",
48 |     "TestTestLogCaptureUtilities",
49 |     "TestTestLogger",
   |     ^^^^^^^^^^^^^^^^
50 |     "TestTestOutputFormattingUtilities",
51 |     "TestTestProfileManager",
   |

F405 `TestTestOutputFormattingUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:50:5
   |
48 |     "TestTestLogCaptureUtilities",
49 |     "TestTestLogger",
50 |     "TestTestOutputFormattingUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
51 |     "TestTestProfileManager",
52 |     "TestTestRecorder",
   |

F405 `TestTestProfileManager` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:51:5
   |
49 |     "TestTestLogger",
50 |     "TestTestOutputFormattingUtilities",
51 |     "TestTestProfileManager",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
52 |     "TestTestRecorder",
53 |     "TestTestReportGenerationHelpers",
   |

F405 `TestTestRecorder` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:52:5
   |
50 |     "TestTestOutputFormattingUtilities",
51 |     "TestTestProfileManager",
52 |     "TestTestRecorder",
   |     ^^^^^^^^^^^^^^^^^^
53 |     "TestTestReportGenerationHelpers",
54 |     "TestTestResourceAllocation",
   |

F405 `TestTestReportGenerationHelpers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:53:5
   |
51 |     "TestTestProfileManager",
52 |     "TestTestRecorder",
53 |     "TestTestReportGenerationHelpers",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
54 |     "TestTestResourceAllocation",
55 |     "TestTestResultAggregationHelpers",
   |

F405 `TestTestResourceAllocation` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:54:5
   |
52 |     "TestTestRecorder",
53 |     "TestTestReportGenerationHelpers",
54 |     "TestTestResourceAllocation",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
55 |     "TestTestResultAggregationHelpers",
56 |     "TestTestResultAggregator",
   |

F405 `TestTestResultAggregationHelpers` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:55:5
   |
53 |     "TestTestReportGenerationHelpers",
54 |     "TestTestResourceAllocation",
55 |     "TestTestResultAggregationHelpers",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
56 |     "TestTestResultAggregator",
57 |     "TestTestResultDataclass",
   |

F405 `TestTestResultAggregator` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:56:5
   |
54 |     "TestTestResourceAllocation",
55 |     "TestTestResultAggregationHelpers",
56 |     "TestTestResultAggregator",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^
57 |     "TestTestResultDataclass",
58 |     "TestTestRetryUtilities",
   |

F405 `TestTestResultDataclass` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:57:5
   |
55 |     "TestTestResultAggregationHelpers",
56 |     "TestTestResultAggregator",
57 |     "TestTestResultDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^
58 |     "TestTestRetryUtilities",
59 |     "TestTestSnapshotDataclass",
   |

F405 `TestTestRetryUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:58:5
   |
56 |     "TestTestResultAggregator",
57 |     "TestTestResultDataclass",
58 |     "TestTestRetryUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^
59 |     "TestTestSnapshotDataclass",
60 |     "TestTestStatusEnum",
   |

F405 `TestTestSnapshotDataclass` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:59:5
   |
57 |     "TestTestResultDataclass",
58 |     "TestTestRetryUtilities",
59 |     "TestTestSnapshotDataclass",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
60 |     "TestTestStatusEnum",
61 |     "TestTestTimingAndBenchmarkingUtilities",
   |

F405 `TestTestStatusEnum` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:60:5
   |
58 |     "TestTestRetryUtilities",
59 |     "TestTestSnapshotDataclass",
60 |     "TestTestStatusEnum",
   |     ^^^^^^^^^^^^^^^^^^^^
61 |     "TestTestTimingAndBenchmarkingUtilities",
62 | ]
   |

F405 `TestTestTimingAndBenchmarkingUtilities` may be undefined, or defined from star imports
  --> tests\unit\test_utils\__init__.py:61:5
   |
59 |     "TestTestSnapshotDataclass",
60 |     "TestTestStatusEnum",
61 |     "TestTestTimingAndBenchmarkingUtilities",
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
62 | ]
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_COMPREHENSIVE_UNIT.py:17:73
   |
15 | # Try to import test utilities
16 | try:
17 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
18 | except ImportError:
19 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_COMPREHENSIVE_UNIT.py:17:96
   |
15 | # Try to import test utilities
16 | try:
17 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
18 | except ImportError:
19 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_CORE_UNIT.py:15:73
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_CORE_UNIT.py:15:96
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_INTEGRATION.py:15:73
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_INTEGRATION.py:15:96
   |
13 | # Try to import test utilities
14 | try:
15 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
16 | except ImportError:
17 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\test_utils\test_test_utils_INTEGRATION.py:21:32
   |
20 |     class agent_sys_path:
21 |         def __enter__(self) -> Self:
   |                                ^^^^
22 |
23 |             return self
   |

F403 `from tests.utils.agent_test_utils import *` used; unable to detect undefined names
 --> tests\unit\test_utils\test_test_utils_LEGACY.py:3:5
  |
1 | import sys
2 | try:
3 |     from tests.utils.agent_test_utils import *
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4 | except ImportError:
5 |     pass
  |

F405 `agent_dir_on_path` may be undefined, or defined from star imports
  --> tests\unit\test_utils\test_test_utils_LEGACY.py:13:10
   |
11 |     """Test that agent_dir_on_path adds AGENT_DIR to sys.path."""
12 |     original_path = list(sys.path)
13 |     with agent_dir_on_path():
   |          ^^^^^^^^^^^^^^^^^
14 |         assert str(AGENT_DIR) in sys.path
   |

F405 `AGENT_DIR` may be undefined, or defined from star imports
  --> tests\unit\test_utils\test_test_utils_LEGACY.py:14:20
   |
12 |     original_path = list(sys.path)
13 |     with agent_dir_on_path():
14 |         assert str(AGENT_DIR) in sys.path
   |                    ^^^^^^^^^
15 |
16 |     # Should be restored
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_PERFORMANCE.py:12:73
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_PERFORMANCE.py:12:96
   |
10 | # Try to import test utilities
11 | try:
12 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
13 | except ImportError:
14 |     # Fallback
   |
help: Remove unused import

F821 Undefined name `Self`
  --> tests\unit\test_utils\test_test_utils_PERFORMANCE.py:18:32
   |
17 |     class agent_sys_path:
18 |         def __enter__(self) -> Self:
   |                                ^^^^
19 |
20 |             return self
   |

F401 `tests.utils.agent_test_utils.load_module_from_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_UNIT.py:13:73
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                         ^^^^^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F401 `tests.utils.agent_test_utils.agent_dir_on_path` imported but unused; consider using `importlib.util.find_spec` to test for availability
  --> tests\unit\test_utils\test_test_utils_UNIT.py:13:96
   |
11 | # Try to import test utilities
12 | try:
13 |     from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
   |                                                                                                ^^^^^^^^^^^^^^^^^
14 | except ImportError:
15 |     # Fallback
   |
help: Remove unused import

F841 Local variable `MockAIBackend` is assigned to but never used
   --> tests\unit\test_utils\test_test_utils_UNIT.py:486:9
    |
484 |     def test_mock_response_with_custom_content(self, utils_module: Any) -> None:
485 |         """Test mock response with custom content."""
486 |         MockAIBackend = utils_module.MockAIBackend
    |         ^^^^^^^^^^^^^
487 |         MockResponse = utils_module.MockResponse
    |
help: Remove assignment to unused variable `MockAIBackend`

F841 Local variable `MockResponse` is assigned to but never used
   --> tests\unit\test_utils\test_test_utils_UNIT.py:487:9
    |
485 |         """Test mock response with custom content."""
486 |         MockAIBackend = utils_module.MockAIBackend
487 |         MockResponse = utils_module.MockResponse
    |         ^^^^^^^^^^^^
    |
help: Remove assignment to unused variable `MockResponse`

F841 Local variable `original_content` is assigned to but never used
  --> tests\utils\legacy_support.py:86:17
   |
84 |             original_content = ""
85 |             if file_path.exists():
86 |                 original_content = file_path.read_text()
   |                 ^^^^^^^^^^^^^^^^
87 |             return None
   |
help: Remove assignment to unused variable `original_content`

E741 Ambiguous variable name: `l`
   --> tests\utils\legacy_support.py:179:48
    |
177 |             if ignore_file.exists():
178 |                 lines = ignore_file.read_text().splitlines()
179 |                 patterns.extend([l.strip() for l in lines if l.strip()])
    |                                                ^
180 |             # Check parent just in case (though test seems to test load_cascading_codeignore_loads_subdirectory_patterns)
181 |             if path and path != self.repo_root:
    |

E741 Ambiguous variable name: `l`
   --> tests\utils\legacy_support.py:185:56
    |
183 |                     if root_ignore.exists():
184 |                         lines = root_ignore.read_text().splitlines()
185 |                         patterns.extend([l.strip() for l in lines if l.strip()])
    |                                                        ^
186 |             return patterns
    |

Found 746 errors.
[*] 33 fixable with the `--fix` option (69 hidden fixes can be enabled with the `--unsafe-fixes` option).

```

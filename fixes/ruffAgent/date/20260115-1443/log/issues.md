## Issues found by ruffAgent at 20260115-1443

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
41 |      
... [TRUNCATED] ...
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

Found 745 errors.
[*] 32 fixable with the `--fix` option (69 hidden fixes can be enabled with the `--unsafe-fixes` option).

```

# PyAgent Code Refactoring Analysis
# Generated: January 19, 2026
# Goal: Identify large files for splitting and lazy loading opportunities

================================================================================
## LARGE FILE ANALYSIS (>500 lines)
================================================================================

### Critical Priority (>900 lines)

| File | Lines | Status/Recommendation |
|------|-------|-----------------------|
| ToolParserFramework.py | 1057 | **REFACTORED & SPLIT** (src/tools/parser/) |
| SlashCommands.py | 960 | **REFACTORED & SPLIT** (src/interface/commands/) |
| StructuredOutputGrammar.py | 1039 | Split: Grammar, Generator, Validator |
| ReasoningEngine.py | 904 | Split: Strategies, Executor, Combiner |
| ResponsesAPI.py | 874 | Split: Request, Response, Streaming |
| PagedAttentionEngine.py | 868 | Split: Cache, Scheduler, Executor |
| KVCacheCoordinator.py | 861 | Split: Coordinator, Groups, Metrics |
| GrammarEngine.py | 858 | Split: Parser, Generator, Compiler |
| TokenizerRegistry.py | 832 | Split: Registry, Tokenizer, Vocab |
| DistributedCoordinator.py | 830 | Split: Coordinator, Worker, Protocol |

### High Priority (700-900 lines)

| File | Lines | Recommendation |
|------|-------|----------------|
| ConversationContext.py | 828 | Split: Context, History, Memory |
| KVOffloadManager.py | 828 | Split: Manager, Policy, Transfer |
| MediaIOEngine.py | 823 | Split: Audio, Video, Image |
| RotaryEmbeddingEngine.py | 818 | Split: Embeddings, Scaling, Cache |
| GuidedDecoder.py | 817 | Split: Decoder, Constraints, Sampler |
| MultiModalProcessor.py | 808 | Split: Processor, Modalities, Fusion |
| SamplingEngine.py | 808 | Split: Samplers, Penalties, Strategies |
| QuantizationEngine.py | 806 | Split: Quantizer, Calibration, Dequant |
| PlatformInterface.py | 805 | Split: Interface, Adapters, Config |
| FusedMoELayer.py | 799 | Split: Router, Experts, Gating |

### Medium Priority (500-700 lines)

| File | Lines | Recommendation |
|------|-------|----------------|
| StructuredOutputManager.py | 794 | Consider splitting |
| SpeculativeEngine.py | 788 | Consider splitting |
| MCPToolServer.py | 779 | Consider splitting |
| LogprobsProcessor.py | 772 | Consider splitting |
| SpeculativeDecoder.py | 757 | Consider splitting |
| EagleProposer.py | ~710 | Split: Config, Tree, Proposer |
| SpecDecodeMetadataV2.py | ~610 | Split: Metadata, Verification |
| ARCOffloadManager.py | ~580 | Split: Cache, Policy, Transfer |

================================================================================
## LAZY LOADING STRATEGY
================================================================================

### Pattern 1: Module-Level __getattr__

```python
# src/infrastructure/__init__.py
def __getattr__(name: str):
    """Lazy import for expensive modules."""
    if name == "EagleProposer":
        from .speculative_v2.EagleProposer import EagleProposer
        return EagleProposer
    if name == "ARCOffloadManager":
        from .kv_transfer.ARCOffloadManager import ARCOffloadManager
        return ARCOffloadManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

### Pattern 2: Lazy Import Function

```python
# src/infrastructure/lazy.py
from functools import lru_cache
from importlib import import_module

@lru_cache(maxsize=None)
def get_eagle_proposer():
    """Lazy load EagleProposer when first accessed."""
    from .speculative_v2.EagleProposer import EagleProposer
    return EagleProposer

@lru_cache(maxsize=None)
def get_arc_offload_manager():
    """Lazy load ARCOffloadManager when first accessed."""
    from .kv_transfer.ARCOffloadManager import ARCOffloadManager
    return ARCOffloadManager
```

### Pattern 3: Deferred Import Descriptor

```python
# src/core/lazy_loader.py
class LazyLoader:
    """Descriptor for lazy module loading."""
    
    def __init__(self, module_path: str, class_name: str):
        self.module_path = module_path
        self.class_name = class_name
        self._loaded = None
    
    def __get__(self, obj, objtype=None):
        if self._loaded is None:
            module = import_module(self.module_path)
            self._loaded = getattr(module, self.class_name)
        return self._loaded

# Usage:
class InfrastructureModule:
    EagleProposer = LazyLoader(
        "src.infrastructure.engine.speculative.EagleProposer",
        "EagleProposer"
    )
```

================================================================================
## SPLITTING RECOMMENDATIONS
================================================================================

### 1. ToolParserFramework.py (1057 lines)

Split into:
```
tools/
├── parser/
│   ├── __init__.py
│   ├── base.py          # ToolParser abstract class
│   ├── json_parser.py   # JSON tool parser
│   ├── xml_parser.py    # XML tool parser
│   └── custom.py        # Custom format parsers
├── validator/
│   ├── __init__.py
│   ├── schema.py        # Schema validation
│   └── semantic.py      # Semantic validation
└── registry/
    ├── __init__.py
    └── tool_registry.py  # Tool registration
```

### 2. SlashCommands.py (960 lines)

Split into:
```
commands/
├── __init__.py
├── base.py              # CommandBase abstract class
├── registry.py          # CommandRegistry
├── builtin/
│   ├── __init__.py
│   ├── file_commands.py # /file, /read, /write
│   ├── agent_commands.py # /agent, /spawn
│   ├── config_commands.py # /config, /set
│   └── debug_commands.py # /debug, /trace
└── parser.py            # Command parsing logic
```

### 3. ReasoningEngine.py (904 lines)

Split into:
```
reasoning/
├── __init__.py
├── engine.py            # Main engine coordinator
├── strategies/
│   ├── __init__.py
│   ├── chain_of_thought.py
│   ├── tree_of_thought.py
│   ├── self_consistency.py
│   ├── reflection.py
│   └── multi_agent_debate.py
├── executor.py          # Strategy execution
└── combiner.py          # Result combination
```

================================================================================
## REFACTORING SCHEDULE
================================================================================

### Week 1: Infrastructure Setup
- [ ] Create lazy loading utilities
- [ ] Set up module __getattr__ patterns
- [ ] Add import timing metrics

### Week 2: Critical Files (>900 lines)
- [ ] Split ToolParserFramework.py
- [ ] Split StructuredOutputGrammar.py
- [ ] Split SlashCommands.py

### Week 3: High Priority Files (800-900 lines)
- [ ] Split ReasoningEngine.py
- [ ] Split PagedAttentionEngine.py
- [ ] Split KVCacheCoordinator.py

### Week 4: Validation & Testing
- [ ] Measure startup time improvement
- [ ] Verify all imports work correctly
- [ ] Run full test suite
- [ ] Update documentation

================================================================================
## EXPECTED OUTCOMES
================================================================================

### Startup Time Reduction
- Current: ~8-10 seconds (estimated)
- Target: ~3-5 seconds
- Method: Lazy loading + module splitting

### Memory Footprint
- Current: All modules loaded at startup
- Target: Only load what's needed
- Method: Deferred imports

### Code Maintainability
- Current: Large monolithic files
- Target: Single-responsibility modules
- Method: Strategic file splitting

### Test Isolation
- Current: Heavy test setup
- Target: Lightweight unit tests
- Method: Better module boundaries

================================================================================
## METRICS TO TRACK
================================================================================

1. **Startup Time**: `time python -c "import src"`
2. **Memory at Startup**: Peak RSS after import
3. **Lines per File**: Keep under 500
4. **Cyclomatic Complexity**: Keep under 25
5. **Import Depth**: Keep under 5 levels

================================================================================














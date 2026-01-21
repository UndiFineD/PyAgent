from __future__ import annotations
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

class LoRAMethod(Enum):
    """LoRA method variants."""
    LORA = auto()                 # Standard LoRA
    QLORA = auto()                # Quantized LoRA
    DORA = auto()                 # Weight-Decomposed LoRA
    RSLORA = auto()               # Rank-Stabilized LoRA
    ADALORA = auto()              # Adaptive LoRA
    VERA = auto()                 # Vector-based Random LoRA
    LORA_PLUS = auto()            # LoRA+ (different LR for A/B)

class AdapterStatus(Enum):
    """Adapter lifecycle status."""
    LOADING = auto()              # Being loaded
    READY = auto()                # Ready to serve
    ACTIVE = auto()               # Currently in use
    INACTIVE = auto()             # Loaded but not active
    EVICTING = auto()             # Being evicted
    ERROR = auto()                # Load error

class TargetModule(Enum):
    """Common LoRA target modules."""
    Q_PROJ = "q_proj"
    K_PROJ = "k_proj"
    V_PROJ = "v_proj"
    O_PROJ = "o_proj"
    GATE_PROJ = "gate_proj"
    UP_PROJ = "up_proj"
    DOWN_PROJ = "down_proj"
    LM_HEAD = "lm_head"
    EMBED_TOKENS = "embed_tokens"

@dataclass
class LoRAConfig:
    """LoRA adapter configuration."""
    adapter_name: str
    adapter_path: str
    rank: int = 8
    alpha: float = 16.0
    dropout: float = 0.0
    method: LoRAMethod = LoRAMethod.LORA
    target_modules: List[str] = field(default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"])
    modules_to_save: List[str] = field(default_factory=list)
    use_rslora: bool = False
    use_dora: bool = False
    scaling: Optional[float] = None
    bias: str = "none"
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def computed_scaling(self) -> float:
        if self.scaling is not None: return self.scaling
        if self.use_rslora: return self.alpha / (self.rank ** 0.5)
        return self.alpha / self.rank
    
    def __hash__(self) -> int:
        return hash((self.adapter_name, self.adapter_path, self.rank))

@dataclass
class LoRARequest:
    """Request to serve with a LoRA adapter."""
    request_id: str
    adapter_name: str
    adapter_config: Optional[LoRAConfig] = None
    priority: int = 0
    
    def __hash__(self) -> int:
        return hash((self.request_id, self.adapter_name))

@dataclass
class LoRAInfo:
    """Information about a loaded adapter."""
    adapter_name: str
    rank: int
    alpha: float
    method: LoRAMethod
    target_modules: List[str]
    num_parameters: int
    memory_bytes: int
    status: AdapterStatus
    load_time_ms: float = 0.0
    last_used: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "adapter_name": self.adapter_name,
            "rank": self.rank,
            "alpha": self.alpha,
            "method": self.method.name,
            "target_modules": self.target_modules,
            "num_parameters": self.num_parameters,
            "memory_mb": self.memory_bytes / (1024 * 1024),
            "status": self.status.name,
        }

@dataclass
class AdapterSlot:
    """GPU slot for a LoRA adapter."""
    slot_id: int
    adapter_name: Optional[str] = None
    is_active: bool = False
    memory_allocated: int = 0
    assigned_at: float = field(default_factory=time.time)
    
    @property
    def is_free(self) -> bool:
        return self.adapter_name is None

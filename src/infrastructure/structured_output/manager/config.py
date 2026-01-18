from __future__ import annotations
import hashlib
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class GrammarType(Enum):
    """Types of grammar constraints supported."""
    NONE = auto()
    JSON = auto()           # JSON Schema validation
    JSON_OBJECT = auto()    # Any valid JSON object
    REGEX = auto()          # Regular expression
    GRAMMAR = auto()        # EBNF/Lark grammar
    CHOICE = auto()         # Choice from list
    FUNCTION_CALL = auto()  # Function call schema
    STRUCTURAL_TAG = auto() # XML-like structural tags

class CompilationStatus(Enum):
    """Status of grammar compilation."""
    PENDING = auto()
    COMPILING = auto()
    READY = auto()
    FAILED = auto()
    CACHED = auto()

@dataclass(frozen=True)
class GrammarSpec:
    """Specification for a grammar constraint."""
    grammar_type: GrammarType
    spec: str  # JSON schema string, regex pattern, EBNF, or choice list
    strict: bool = True  # Whether to strictly enforce the grammar
    max_tokens: Optional[int] = None  # Maximum tokens to generate
    
    def to_cache_key(self) -> str:
        """Generate cache key for this spec."""
        content = f"{self.grammar_type.name}:{self.spec}:{self.strict}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

@dataclass
class CompilationResult:
    """Result of grammar compilation."""
    status: CompilationStatus
    grammar: Optional["StructuredOutputGrammar"] = None
    error: Optional[str] = None
    compile_time_ms: float = 0.0
    
    @property
    def is_ready(self) -> bool:
        return self.status == CompilationStatus.READY
    
    @property
    def is_failed(self) -> bool:
        return self.status == CompilationStatus.FAILED

@dataclass
class ValidationResult:
    """Result of token validation."""
    is_valid: bool
    accepted_prefix_length: int = 0
    error_message: Optional[str] = None
    suggestion: Optional[str] = None

@dataclass
class BackendStats:
    """Statistics for a structured output backend."""
    grammars_compiled: int = 0
    grammars_cached: int = 0
    compilations_failed: int = 0
    total_compile_time_ms: float = 0.0
    total_tokens_validated: int = 0
    validation_rejections: int = 0

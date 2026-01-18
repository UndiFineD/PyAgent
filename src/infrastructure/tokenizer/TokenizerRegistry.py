# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Tokenizer Registry.
Delegates to modularized sub-packages in src/infrastructure/tokenizer/.
"""

from .models import (
    TokenizerBackend as TokenizerBackend,
    SpecialTokenHandling as SpecialTokenHandling,
    TruncationStrategy as TruncationStrategy,
    PaddingStrategy as PaddingStrategy,
    TokenizerConfig as TokenizerConfig,
    TokenizerInfo as TokenizerInfo,
    TokenizeResult as TokenizeResult,
    BatchTokenizeResult as BatchTokenizeResult,
)
from .protocol import TokenizerProtocol as TokenizerProtocol
from .base import BaseTokenizer as BaseTokenizer
from .huggingface import HuggingFaceTokenizer as HuggingFaceTokenizer
from .tiktoken import TiktokenTokenizer as TiktokenTokenizer
from .mistral import MistralTokenizer as MistralTokenizer
from .registry import TokenizerRegistry as TokenizerRegistry
from .pool import TokenizerPool as TokenizerPool
from .utils import (
    get_tokenizer as get_tokenizer,
    create_tokenizer as create_tokenizer,
    estimate_token_count as estimate_token_count,
    detect_tokenizer_backend as detect_tokenizer_backend,
)

import numpy as np


# =============================================================================
# Enums
# =============================================================================

class TokenizerBackend(Enum):
    """Supported tokenizer backends."""
    HUGGINGFACE = auto()      # transformers AutoTokenizer
    TIKTOKEN = auto()          # OpenAI tiktoken
    MISTRAL = auto()           # Mistral tokenizers
    SENTENCEPIECE = auto()     # Google SentencePiece
    CUSTOM = auto()            # User-defined tokenizer


class SpecialTokenHandling(Enum):
    """How to handle special tokens."""
    INCLUDE = auto()           # Include BOS/EOS/PAD
    EXCLUDE = auto()           # Exclude all special tokens
    BOS_ONLY = auto()          # Include BOS only
    EOS_ONLY = auto()          # Include EOS only
    CUSTOM = auto()            # Custom token set


class TruncationStrategy(Enum):
    """Truncation strategies for long sequences."""
    NONE = auto()              # No truncation (may error)
    LEFT = auto()              # Truncate from left
    RIGHT = auto()             # Truncate from right
    LONGEST_FIRST = auto()     # Truncate longest sequence first


class PaddingStrategy(Enum):
    """Padding strategies for batched inputs."""
    NONE = auto()              # No padding
    MAX_LENGTH = auto()        # Pad to max_length
    LONGEST = auto()           # Pad to longest in batch


# =============================================================================
# Protocols
# =============================================================================

@runtime_checkable
class TokenizerProtocol(Protocol):
    """Protocol for tokenizer implementations."""
    
    @property
    def vocab_size(self) -> int:
        """Size of the vocabulary."""
        ...
    
    @property
    def bos_token_id(self) -> Optional[int]:
        """Beginning of sequence token ID."""
        ...
    
    @property
    def eos_token_id(self) -> Optional[int]:
        """End of sequence token ID."""
        ...
    
    @property
    def pad_token_id(self) -> Optional[int]:
        """Padding token ID."""
        ...
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        """Encode text to token IDs."""
        ...
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        """Decode token IDs to text."""
        ...
    
    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        """Batch encode multiple texts."""
        ...


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class TokenizerConfig:
    """Configuration for tokenizer initialization."""
    model_name: str                                    # Model name or path
    backend: TokenizerBackend = TokenizerBackend.HUGGINGFACE
    revision: Optional[str] = None                     # Model revision
    trust_remote_code: bool = False                    # Allow remote code
    use_fast: bool = True                              # Use fast tokenizer
    max_length: Optional[int] = None                   # Max sequence length
    truncation: TruncationStrategy = TruncationStrategy.RIGHT
    padding: PaddingStrategy = PaddingStrategy.NONE
    special_tokens: SpecialTokenHandling = SpecialTokenHandling.INCLUDE
    add_bos_token: bool = True                         # Add BOS automatically
    add_eos_token: bool = False                        # Add EOS automatically
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        """Hash for caching."""
        return hash((
            self.model_name,
            self.backend,
            self.revision,
            self.trust_remote_code,
            self.use_fast,
            self.max_length,
        ))


@dataclass
class TokenizerInfo:
    """Information about a loaded tokenizer."""
    backend: TokenizerBackend
    vocab_size: int
    bos_token_id: Optional[int]
    eos_token_id: Optional[int]
    pad_token_id: Optional[int]
    max_length: int
    model_name: str
    is_fast: bool = True
    supports_chat_template: bool = False
    chat_template: Optional[str] = None
    special_tokens: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "backend": self.backend.name,
            "vocab_size": self.vocab_size,
            "bos_token_id": self.bos_token_id,
            "eos_token_id": self.eos_token_id,
            "pad_token_id": self.pad_token_id,
            "max_length": self.max_length,
            "model_name": self.model_name,
            "is_fast": self.is_fast,
            "supports_chat_template": self.supports_chat_template,
        }


@dataclass
class TokenizeResult:
    """Result of tokenization."""
    input_ids: List[int]                              # Token IDs
    attention_mask: Optional[List[int]] = None        # Attention mask
    token_type_ids: Optional[List[int]] = None        # Token type IDs
    offsets: Optional[List[Tuple[int, int]]] = None   # Character offsets
    tokens: Optional[List[str]] = None                # String tokens
    num_tokens: int = 0
    truncated: bool = False
    
    def __post_init__(self):
        self.num_tokens = len(self.input_ids)
    
    def to_numpy(self) -> Dict[str, np.ndarray]:
        """Convert to numpy arrays."""
        result = {"input_ids": np.array(self.input_ids, dtype=np.int64)}
        if self.attention_mask:
            result["attention_mask"] = np.array(self.attention_mask, dtype=np.int64)
        if self.token_type_ids:
            result["token_type_ids"] = np.array(self.token_type_ids, dtype=np.int64)
        return result


@dataclass
class BatchTokenizeResult:
    """Result of batch tokenization."""
    input_ids: List[List[int]]
    attention_mask: Optional[List[List[int]]] = None
    token_counts: List[int] = field(default_factory=list)
    max_length: int = 0
    
    def __post_init__(self):
        self.token_counts = [len(ids) for ids in self.input_ids]
        self.max_length = max(self.token_counts) if self.token_counts else 0
    
    def pad_to_max(self, pad_token_id: int = 0) -> 'BatchTokenizeResult':
        """Pad all sequences to max length."""
        padded_ids = []
        padded_mask = []
        
        for ids in self.input_ids:
            pad_len = self.max_length - len(ids)
            padded_ids.append(ids + [pad_token_id] * pad_len)
            padded_mask.append([1] * len(ids) + [0] * pad_len)
        
        return BatchTokenizeResult(
            input_ids=padded_ids,
            attention_mask=padded_mask,
            token_counts=self.token_counts,
            max_length=self.max_length,
        )


# =============================================================================
# Base Tokenizer Class
# =============================================================================

class BaseTokenizer(ABC):
    """Abstract base class for tokenizers."""
    
    def __init__(self, config: TokenizerConfig):
        self.config = config
        self._info: Optional[TokenizerInfo] = None
    
    @property
    @abstractmethod
    def vocab_size(self) -> int:
        """Size of the vocabulary."""
        pass
    
    @property
    @abstractmethod
    def bos_token_id(self) -> Optional[int]:
        """Beginning of sequence token ID."""
        pass
    
    @property
    @abstractmethod
    def eos_token_id(self) -> Optional[int]:
        """End of sequence token ID."""
        pass
    
    @property
    @abstractmethod
    def pad_token_id(self) -> Optional[int]:
        """Padding token ID."""
        pass
    
    @abstractmethod
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        """Encode text to token IDs."""
        pass
    
    @abstractmethod
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        """Decode token IDs to text."""
        pass
    
    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        """Batch encode multiple texts."""
        return [self.encode(text, add_special_tokens) for text in texts]
    
    def batch_decode(
        self,
        token_ids_list: List[Sequence[int]],
        skip_special_tokens: bool = True,
    ) -> List[str]:
        """Batch decode multiple token sequences."""
        return [self.decode(ids, skip_special_tokens) for ids in token_ids_list]
    
    def tokenize(
        self,
        text: str,
        add_special_tokens: bool = True,
        return_offsets: bool = False,
    ) -> TokenizeResult:
        """Full tokenization with metadata."""
        input_ids = self.encode(text, add_special_tokens)
        
        return TokenizeResult(
            input_ids=input_ids,
            attention_mask=[1] * len(input_ids),
            num_tokens=len(input_ids),
        )
    
    def get_info(self) -> TokenizerInfo:
        """Get tokenizer information."""
        if self._info is None:
            self._info = TokenizerInfo(
                backend=self.config.backend,
                vocab_size=self.vocab_size,
                bos_token_id=self.bos_token_id,
                eos_token_id=self.eos_token_id,
                pad_token_id=self.pad_token_id,
                max_length=self.config.max_length or 8192,
                model_name=self.config.model_name,
            )
        return self._info
    
    def estimate_tokens(self, text: str) -> int:
        """Fast token count estimation without full tokenization."""
        # Rough estimate: ~4 chars per token for English
        return max(1, len(text) // 4)


# =============================================================================
# HuggingFace Tokenizer
# =============================================================================

class HuggingFaceTokenizer(BaseTokenizer):
    """HuggingFace transformers tokenizer wrapper."""
    
    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._tokenizer = None
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load the HuggingFace tokenizer."""
        try:
            from transformers import AutoTokenizer
            
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                revision=self.config.revision,
                trust_remote_code=self.config.trust_remote_code,
                use_fast=self.config.use_fast,
            )
            
            # Set padding token if not set
            if self._tokenizer.pad_token is None:
                if self._tokenizer.eos_token is not None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                else:
                    self._tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                    
        except ImportError:
            raise ImportError("transformers package required for HuggingFace tokenizer")
    
    @property
    def vocab_size(self) -> int:
        return self._tokenizer.vocab_size
    
    @property
    def bos_token_id(self) -> Optional[int]:
        return self._tokenizer.bos_token_id
    
    @property
    def eos_token_id(self) -> Optional[int]:
        return self._tokenizer.eos_token_id
    
    @property
    def pad_token_id(self) -> Optional[int]:
        return self._tokenizer.pad_token_id
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._tokenizer.decode(token_ids, skip_special_tokens=skip_special_tokens)
    
    def batch_encode(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        result = self._tokenizer(
            texts,
            add_special_tokens=add_special_tokens,
            padding=False,
            truncation=False,
        )
        return result["input_ids"]
    
    def apply_chat_template(
        self,
        messages: List[Dict[str, str]],
        add_generation_prompt: bool = True,
    ) -> str:
        """Apply chat template to messages."""
        if hasattr(self._tokenizer, 'apply_chat_template'):
            return self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=add_generation_prompt,
            )
        raise ValueError("Tokenizer does not support chat templates")
    
    def get_info(self) -> TokenizerInfo:
        if self._info is None:
            has_chat = hasattr(self._tokenizer, 'chat_template') and self._tokenizer.chat_template is not None
            
            self._info = TokenizerInfo(
                backend=TokenizerBackend.HUGGINGFACE,
                vocab_size=self.vocab_size,
                bos_token_id=self.bos_token_id,
                eos_token_id=self.eos_token_id,
                pad_token_id=self.pad_token_id,
                max_length=self._tokenizer.model_max_length,
                model_name=self.config.model_name,
                is_fast=self._tokenizer.is_fast if hasattr(self._tokenizer, 'is_fast') else False,
                supports_chat_template=has_chat,
                chat_template=self._tokenizer.chat_template if has_chat else None,
            )
        return self._info


# =============================================================================
# Tiktoken Tokenizer
# =============================================================================

class TiktokenTokenizer(BaseTokenizer):
    """OpenAI tiktoken tokenizer wrapper."""
    
    # Model to encoding mapping
    MODEL_ENCODINGS = {
        "gpt-4": "cl100k_base",
        "gpt-4o": "o200k_base",
        "gpt-4-turbo": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "text-embedding-ada-002": "cl100k_base",
        "text-embedding-3-small": "cl100k_base",
        "text-embedding-3-large": "cl100k_base",
    }
    
    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._encoding = None
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load tiktoken encoding."""
        try:
            import tiktoken
            
            # Determine encoding
            model_name = self.config.model_name.lower()
            
            # Check for direct encoding name
            if model_name in ["cl100k_base", "p50k_base", "r50k_base", "o200k_base"]:
                self._encoding = tiktoken.get_encoding(model_name)
            else:
                # Try model-based encoding
                encoding_name = self.MODEL_ENCODINGS.get(model_name)
                if encoding_name:
                    self._encoding = tiktoken.get_encoding(encoding_name)
                else:
                    # Try to get encoding for model
                    try:
                        self._encoding = tiktoken.encoding_for_model(model_name)
                    except KeyError:
                        # Default to cl100k_base
                        self._encoding = tiktoken.get_encoding("cl100k_base")
                        
        except ImportError:
            raise ImportError("tiktoken package required for Tiktoken tokenizer")
    
    @property
    def vocab_size(self) -> int:
        return self._encoding.n_vocab
    
    @property
    def bos_token_id(self) -> Optional[int]:
        # Tiktoken doesn't have explicit BOS
        return None
    
    @property
    def eos_token_id(self) -> Optional[int]:
        # Use special token if available
        try:
            return self._encoding.encode("<|endoftext|>", allowed_special={"<|endoftext|>"})[0]
        except:
            return None
    
    @property
    def pad_token_id(self) -> Optional[int]:
        return None  # Tiktoken doesn't have padding
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        return self._encoding.encode(text)
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._encoding.decode(list(token_ids))
    
    def encode_batch(
        self,
        texts: List[str],
        add_special_tokens: bool = True,
    ) -> List[List[int]]:
        """Parallel batch encoding."""
        return self._encoding.encode_batch(texts)
    
    def estimate_tokens(self, text: str) -> int:
        """Accurate token count for tiktoken."""
        return len(self._encoding.encode(text))


# =============================================================================
# Mistral Tokenizer
# =============================================================================

class MistralTokenizer(BaseTokenizer):
    """Mistral tokenizer wrapper."""
    
    def __init__(self, config: TokenizerConfig):
        super().__init__(config)
        self._tokenizer = None
        self._load_tokenizer()
    
    def _load_tokenizer(self):
        """Load Mistral tokenizer."""
        try:
            from mistral_common.tokens.tokenizers.mistral import MistralTokenizer as MT
            
            self._tokenizer = MT.from_model(self.config.model_name)
        except ImportError:
            # Fall back to HuggingFace
            from transformers import AutoTokenizer
            
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=True,
            )
    
    @property
    def vocab_size(self) -> int:
        if hasattr(self._tokenizer, 'n_words'):
            return self._tokenizer.n_words
        return self._tokenizer.vocab_size
    
    @property
    def bos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'bos_id'):
            return self._tokenizer.bos_id
        return self._tokenizer.bos_token_id
    
    @property
    def eos_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'eos_id'):
            return self._tokenizer.eos_id
        return self._tokenizer.eos_token_id
    
    @property
    def pad_token_id(self) -> Optional[int]:
        if hasattr(self._tokenizer, 'pad_id'):
            return self._tokenizer.pad_id
        return getattr(self._tokenizer, 'pad_token_id', None)
    
    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
    ) -> List[int]:
        if hasattr(self._tokenizer, 'encode'):
            result = self._tokenizer.encode(text)
            if hasattr(result, 'tokens'):
                return result.tokens
            return result
        return self._tokenizer.encode(text, add_special_tokens=add_special_tokens)
    
    def decode(
        self,
        token_ids: Sequence[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return self._tokenizer.decode(list(token_ids))


# =============================================================================
# Tokenizer Registry
# =============================================================================

class TokenizerRegistry:
    """
    Central registry for tokenizer management.
    
    Features:
    - LRU caching of tokenizers
    - Backend auto-detection
    - Thread-safe access
    """
    
    _instance: Optional['TokenizerRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'TokenizerRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, max_cached: int = 16):
        if self._initialized:
            return
        
        self._cache: OrderedDict[int, BaseTokenizer] = OrderedDict()
        self._max_cached = max_cached
        self._cache_lock = threading.RLock()
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
        }
        self._initialized = True
    
    def get_tokenizer(self, config: TokenizerConfig) -> BaseTokenizer:
        """Get or create a tokenizer."""
        key = hash(config)
        
        with self._cache_lock:
            if key in self._cache:
                self._stats["hits"] += 1
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return self._cache[key]
            
            self._stats["misses"] += 1
        
        # Create new tokenizer
        tokenizer = self._create_tokenizer(config)
        
        with self._cache_lock:
            # Evict if necessary
            while len(self._cache) >= self._max_cached:
                self._cache.popitem(last=False)
                self._stats["evictions"] += 1
            
            self._cache[key] = tokenizer
        
        return tokenizer
    
    def _create_tokenizer(self, config: TokenizerConfig) -> BaseTokenizer:
        """Create tokenizer based on backend."""
        if config.backend == TokenizerBackend.HUGGINGFACE:
            return HuggingFaceTokenizer(config)
        elif config.backend == TokenizerBackend.TIKTOKEN:
            return TiktokenTokenizer(config)
        elif config.backend == TokenizerBackend.MISTRAL:
            return MistralTokenizer(config)
        else:
            # Auto-detect backend
            return self._auto_create(config)
    
    def _auto_create(self, config: TokenizerConfig) -> BaseTokenizer:
        """Auto-detect and create appropriate tokenizer."""
        model_name = config.model_name.lower()
        
        # Check for OpenAI models
        if any(name in model_name for name in ["gpt-4", "gpt-3.5", "text-embedding"]):
            config = TokenizerConfig(
                model_name=config.model_name,
                backend=TokenizerBackend.TIKTOKEN,
            )
            return TiktokenTokenizer(config)
        
        # Check for Mistral models
        if "mistral" in model_name:
            config = TokenizerConfig(
                model_name=config.model_name,
                backend=TokenizerBackend.MISTRAL,
            )
            return MistralTokenizer(config)
        
        # Default to HuggingFace
        return HuggingFaceTokenizer(config)
    
    def clear_cache(self):
        """Clear the tokenizer cache."""
        with self._cache_lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._cache_lock:
            return {
                **self._stats,
                "cached": len(self._cache),
                "max_cached": self._max_cached,
            }


# =============================================================================
# Tokenizer Pool
# =============================================================================

class TokenizerPool:
    """
    Thread-safe pool of tokenizers for parallel processing.
    
    Beyond vLLM:
    - Per-thread tokenizer instances
    - Automatic cleanup
    - Memory-efficient pooling
    """
    
    def __init__(
        self,
        config: TokenizerConfig,
        pool_size: int = 4,
    ):
        self.config = config
        self.pool_size = pool_size
        
        self._pool: List[BaseTokenizer] = []
        self._available: List[bool] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        
        self._init_pool()
    
    def _init_pool(self):
        """Initialize the tokenizer pool."""
        registry = TokenizerRegistry()
        
        for _ in range(self.pool_size):
            tokenizer = registry.get_tokenizer(self.config)
            self._pool.append(tokenizer)
            self._available.append(True)
    
    def acquire(self, timeout: Optional[float] = None) -> Optional[BaseTokenizer]:
        """Acquire a tokenizer from the pool."""
        with self._condition:
            start = time.monotonic()
            
            while True:
                for i, available in enumerate(self._available):
                    if available:
                        self._available[i] = False
                        return self._pool[i]
                
                if timeout is not None:
                    remaining = timeout - (time.monotonic() - start)
                    if remaining <= 0:
                        return None
                    self._condition.wait(remaining)
                else:
                    self._condition.wait()
    
    def release(self, tokenizer: BaseTokenizer):
        """Release a tokenizer back to the pool."""
        with self._condition:
            for i, t in enumerate(self._pool):
                if t is tokenizer:
                    self._available[i] = True
                    self._condition.notify()
                    return
    
    def __enter__(self) -> BaseTokenizer:
        tokenizer = self.acquire()
        if tokenizer is None:
            raise RuntimeError("Failed to acquire tokenizer from pool")
        self._current = tokenizer
        return tokenizer
    
    def __exit__(self, *args):
        self.release(self._current)


# =============================================================================
# Utility Functions
# =============================================================================

def get_tokenizer(
    model_name: str,
    backend: Optional[TokenizerBackend] = None,
    **kwargs,
) -> BaseTokenizer:
    """
    Get a tokenizer from the global registry.
    
    Args:
        model_name: Model name or path
        backend: Optional backend override
        **kwargs: Additional config options
    """
    config = TokenizerConfig(
        model_name=model_name,
        backend=backend or TokenizerBackend.HUGGINGFACE,
        **kwargs,
    )
    
    registry = TokenizerRegistry()
    return registry.get_tokenizer(config)


def create_tokenizer(config: TokenizerConfig) -> BaseTokenizer:
    """Create a tokenizer from config."""
    registry = TokenizerRegistry()
    return registry.get_tokenizer(config)


def estimate_token_count(text: str, model_name: Optional[str] = None) -> int:
    """
    Fast token count estimation.
    
    Uses Rust acceleration when available.
    """
    if not text:
        return 0
        
    try:
        import rust_core
        return rust_core.estimate_tokens_rust(text)
    except (ImportError, AttributeError):
        # Fallback to heuristic
        # ~4 chars per token for English, ~2 for code
        has_code = any(c in text for c in "{}[]();=")
        chars_per_token = 2.5 if has_code else 4.0
        return max(1, int(len(text) / chars_per_token))


def detect_tokenizer_backend(model_name: str) -> TokenizerBackend:
    """Auto-detect the appropriate tokenizer backend."""
    model_lower = model_name.lower()
    
    if any(x in model_lower for x in ["gpt-4", "gpt-3.5", "text-embedding", "o1-", "davinci", "curie"]):
        return TokenizerBackend.TIKTOKEN
    
    if "mistral" in model_lower:
        return TokenizerBackend.MISTRAL
    
    return TokenizerBackend.HUGGINGFACE

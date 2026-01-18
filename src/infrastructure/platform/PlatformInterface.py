"""
Platform Abstraction Interface - Phase 42

Unified platform detection and device capability management inspired by vLLM's
platforms module. Provides hardware abstraction for multi-device deployment.

Key Features:
- Platform detection (CUDA, ROCm, TPU, XPU, CPU)
- Device capability enumeration
- Memory management utilities
- Quantization compatibility checks
- Attention backend selection

Performance: Uses Rust-accelerated platform fingerprinting.
"""

from __future__ import annotations

import os
import sys
import platform
import hashlib
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    NamedTuple,
)
from functools import lru_cache

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "PlatformType",
    "CpuArchitecture",
    "QuantizationType",
    "AttentionBackend",
    "DeviceFeature",
    # Data Classes
    "DeviceCapability",
    "MemoryInfo",
    "PlatformConfig",
    "DeviceInfo",
    # Main Classes
    "Platform",
    "CudaPlatform",
    "RocmPlatform",
    "TpuPlatform",
    "XpuPlatform",
    "CpuPlatform",
    "PlatformRegistry",
    # Functions
    "get_current_platform",
    "detect_platform",
    "get_device_count",
    "get_device_capability",
    "get_memory_info",
    "is_quantization_supported",
    "select_attention_backend",
]


# ============================================================================
# Enums
# ============================================================================


class PlatformType(Enum):
    """Supported platform types."""

    CUDA = "cuda"
    ROCM = "rocm"
    TPU = "tpu"
    XPU = "xpu"
    CPU = "cpu"
    OOT = "out_of_tree"  # Out-of-tree custom platforms
    UNKNOWN = "unknown"


class CpuArchitecture(Enum):
    """CPU architecture types."""

    X86_64 = "x86_64"
    ARM64 = "arm64"
    AARCH64 = "aarch64"
    POWERPC = "powerpc"
    S390X = "s390x"
    RISCV = "riscv"
    UNKNOWN = "unknown"


class QuantizationType(Enum):
    """Quantization methods."""

    NONE = "none"
    GPTQ = "gptq"
    AWQ = "awq"
    SQUEEZELLM = "squeezellm"
    FP8 = "fp8"
    FP8_E4M3 = "fp8_e4m3"
    FP8_E5M2 = "fp8_e5m2"
    INT8 = "int8"
    INT4 = "int4"
    NF4 = "nf4"
    GGUF = "gguf"
    BITSANDBYTES = "bitsandbytes"
    EXLLAMA = "exllama"
    EXLLAMA_V2 = "exllama_v2"
    MARLIN = "marlin"


class AttentionBackend(Enum):
    """Attention implementation backends."""

    FLASH_ATTN = "flash_attn"
    FLASH_ATTN_V2 = "flash_attn_v2"
    FLASH_ATTN_V3 = "flash_attn_v3"
    XFORMERS = "xformers"
    TORCH_SDPA = "torch_sdpa"
    FLASHINFER = "flashinfer"
    PAGED_ATTENTION = "paged_attention"
    TRITON = "triton"
    ROCM = "rocm"
    TPU = "tpu"
    CPU = "cpu"
    DEFAULT = "default"


class DeviceFeature(Flag):
    """Device feature flags."""

    NONE = 0
    TENSOR_CORES = auto()
    FP16 = auto()
    BF16 = auto()
    FP8 = auto()
    INT8 = auto()
    INT4 = auto()
    FLASH_ATTENTION = auto()
    PAGED_ATTENTION = auto()
    CUDA_GRAPHS = auto()
    UNIFIED_MEMORY = auto()
    MULTI_GPU = auto()
    PEER_ACCESS = auto()
    NVLINK = auto()
    INFINITY_FABRIC = auto()  # AMD
    ASYNC_COPY = auto()
    SPARSE_OPS = auto()


# ============================================================================
# Data Classes
# ============================================================================


class DeviceCapability(NamedTuple):
    """Device compute capability."""

    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __ge__(self, other: "DeviceCapability") -> bool:
        return (self.major, self.minor) >= (other.major, other.minor)

    def __gt__(self, other: "DeviceCapability") -> bool:
        return (self.major, self.minor) > (other.major, other.minor)

    @property
    def as_int(self) -> int:
        """Return capability as integer (e.g., 80 for 8.0)."""
        return self.major * 10 + self.minor


@dataclass
class MemoryInfo:
    """Device memory information."""

    total_bytes: int
    free_bytes: int
    used_bytes: int
    reserved_bytes: int = 0

    @property
    def total_gb(self) -> float:
        return self.total_bytes / (1024**3)

    @property
    def free_gb(self) -> float:
        return self.free_bytes / (1024**3)

    @property
    def used_gb(self) -> float:
        return self.used_bytes / (1024**3)

    @property
    def utilization(self) -> float:
        """Memory utilization as percentage."""
        if self.total_bytes == 0:
            return 0.0
        return self.used_bytes / self.total_bytes * 100


@dataclass
class DeviceInfo:
    """Complete device information."""

    device_id: int
    name: str
    platform: PlatformType
    capability: DeviceCapability
    memory: MemoryInfo
    features: DeviceFeature
    driver_version: str = ""
    compute_units: int = 0
    clock_rate_mhz: int = 0
    pcie_bandwidth_gbps: float = 0.0

    def supports_feature(self, feature: DeviceFeature) -> bool:
        """Check if device supports a feature."""
        return bool(self.features & feature)

    @property
    def is_datacenter(self) -> bool:
        """Check if device is a datacenter GPU."""
        datacenter_patterns = ["A100", "H100", "H200", "V100", "MI250", "MI300"]
        return any(p in self.name for p in datacenter_patterns)


@dataclass
class PlatformConfig:
    """Platform configuration."""

    platform_type: PlatformType
    device_ids: List[int] = field(default_factory=list)
    memory_fraction: float = 0.9
    enable_cuda_graphs: bool = True
    enable_flash_attention: bool = True
    attention_backend: Optional[AttentionBackend] = None
    quantization_types: Set[QuantizationType] = field(default_factory=set)
    custom_ops_enabled: bool = True
    compile_backend: str = "inductor"


# ============================================================================
# Platform Base Class
# ============================================================================


class Platform(ABC):
    """
    Abstract base class for platform implementations.
    
    Provides unified interface for device detection, capability checking,
    and resource management across different hardware platforms.
    """

    _instances: Dict[PlatformType, "Platform"] = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern for platform instances."""
        platform_type = cls.get_platform_type()
        with cls._lock:
            if platform_type not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[platform_type] = instance
            return cls._instances[platform_type]

    @classmethod
    @abstractmethod
    def get_platform_type(cls) -> PlatformType:
        """Return the platform type."""
        ...

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if this platform is available."""
        ...

    @abstractmethod
    def get_device_count(self) -> int:
        """Get number of available devices."""
        ...

    @abstractmethod
    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        """Get device compute capability."""
        ...

    @abstractmethod
    def get_device_name(self, device_id: int = 0) -> str:
        """Get device name."""
        ...

    @abstractmethod
    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        """Get device memory information."""
        ...

    @abstractmethod
    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        """Get device feature flags."""
        ...

    def get_device_info(self, device_id: int = 0) -> DeviceInfo:
        """Get complete device information."""
        return DeviceInfo(
            device_id=device_id,
            name=self.get_device_name(device_id),
            platform=self.get_platform_type(),
            capability=self.get_device_capability(device_id),
            memory=self.get_memory_info(device_id),
            features=self.get_device_features(device_id),
            driver_version=self.get_driver_version(),
        )

    def get_driver_version(self) -> str:
        """Get platform driver version."""
        return "unknown"

    def supports_quantization(self, quant_type: QuantizationType) -> bool:
        """Check if quantization type is supported."""
        return quant_type in self.get_supported_quantizations()

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        """Get supported quantization types."""
        return {QuantizationType.NONE}

    def get_attention_backends(self) -> List[AttentionBackend]:
        """Get available attention backends in priority order."""
        return [AttentionBackend.DEFAULT]

    def select_attention_backend(
        self,
        preferred: Optional[AttentionBackend] = None,
        features_required: DeviceFeature = DeviceFeature.NONE,
    ) -> AttentionBackend:
        """Select best attention backend."""
        backends = self.get_attention_backends()
        if preferred and preferred in backends:
            return preferred
        return backends[0] if backends else AttentionBackend.DEFAULT

    def empty_cache(self) -> None:
        """Empty device memory cache."""
        pass

    def synchronize(self, device_id: int = 0) -> None:
        """Synchronize device."""
        pass

    def set_device(self, device_id: int) -> None:
        """Set current device."""
        pass

    def get_current_device(self) -> int:
        """Get current device ID."""
        return 0

    @property
    def cpu_architecture(self) -> CpuArchitecture:
        """Get CPU architecture."""
        machine = platform.machine().lower()
        arch_map = {
            "x86_64": CpuArchitecture.X86_64,
            "amd64": CpuArchitecture.X86_64,
            "aarch64": CpuArchitecture.AARCH64,
            "arm64": CpuArchitecture.ARM64,
            "ppc64le": CpuArchitecture.POWERPC,
            "s390x": CpuArchitecture.S390X,
            "riscv64": CpuArchitecture.RISCV,
        }
        return arch_map.get(machine, CpuArchitecture.UNKNOWN)

    def create_fingerprint(self) -> str:
        """Create platform fingerprint for caching."""
        device_count = self.get_device_count()
        devices = []
        for i in range(min(device_count, 8)):  # Limit to 8 devices
            info = self.get_device_info(i)
            devices.append(f"{info.name}:{info.capability}:{info.memory.total_bytes}")

        data = f"{self.get_platform_type().value}:{','.join(devices)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


# ============================================================================
# CUDA Platform
# ============================================================================


class CudaPlatform(Platform):
    """NVIDIA CUDA platform implementation."""

    _torch = None
    _pynvml = None

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.CUDA

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch

            return torch.cuda.is_available()
        except ImportError:
            return False

    def _get_torch(self):
        if self._torch is None:
            import torch

            self._torch = torch
        return self._torch

    def get_device_count(self) -> int:
        torch = self._get_torch()
        return torch.cuda.device_count()

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        torch = self._get_torch()
        cap = torch.cuda.get_device_capability(device_id)
        return DeviceCapability(major=cap[0], minor=cap[1])

    def get_device_name(self, device_id: int = 0) -> str:
        torch = self._get_torch()
        return torch.cuda.get_device_name(device_id)

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        torch = self._get_torch()
        props = torch.cuda.get_device_properties(device_id)
        total = props.total_memory
        reserved = torch.cuda.memory_reserved(device_id)
        allocated = torch.cuda.memory_allocated(device_id)
        free = total - reserved
        return MemoryInfo(
            total_bytes=total,
            free_bytes=free,
            used_bytes=allocated,
            reserved_bytes=reserved,
        )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        cap = self.get_device_capability(device_id)
        features = DeviceFeature.NONE

        # FP16 support (SM 5.3+)
        if cap >= DeviceCapability(5, 3):
            features |= DeviceFeature.FP16

        # Tensor cores (SM 7.0+)
        if cap >= DeviceCapability(7, 0):
            features |= DeviceFeature.TENSOR_CORES
            features |= DeviceFeature.INT8

        # BF16 support (SM 8.0+)
        if cap >= DeviceCapability(8, 0):
            features |= DeviceFeature.BF16
            features |= DeviceFeature.FLASH_ATTENTION
            features |= DeviceFeature.CUDA_GRAPHS
            features |= DeviceFeature.ASYNC_COPY

        # FP8 support (SM 8.9+ / Hopper)
        if cap >= DeviceCapability(8, 9):
            features |= DeviceFeature.FP8
            features |= DeviceFeature.INT4
            features |= DeviceFeature.SPARSE_OPS

        # Multi-GPU check
        if self.get_device_count() > 1:
            features |= DeviceFeature.MULTI_GPU

        return features

    def get_driver_version(self) -> str:
        torch = self._get_torch()
        try:
            return torch.version.cuda or "unknown"
        except Exception:
            return "unknown"

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        cap = self.get_device_capability()
        quants = {QuantizationType.NONE, QuantizationType.INT8}

        if cap >= DeviceCapability(7, 5):
            quants |= {
                QuantizationType.GPTQ,
                QuantizationType.AWQ,
                QuantizationType.INT4,
            }

        if cap >= DeviceCapability(8, 0):
            quants |= {
                QuantizationType.MARLIN,
                QuantizationType.EXLLAMA,
                QuantizationType.EXLLAMA_V2,
                QuantizationType.NF4,
                QuantizationType.BITSANDBYTES,
            }

        if cap >= DeviceCapability(8, 9):
            quants |= {
                QuantizationType.FP8,
                QuantizationType.FP8_E4M3,
                QuantizationType.FP8_E5M2,
            }

        return quants

    def get_attention_backends(self) -> List[AttentionBackend]:
        cap = self.get_device_capability()
        backends = []

        if cap >= DeviceCapability(8, 0):
            backends.append(AttentionBackend.FLASH_ATTN_V2)
            try:
                import flash_attn

                if hasattr(flash_attn, "__version__"):
                    v = flash_attn.__version__
                    if v.startswith("3."):
                        backends.insert(0, AttentionBackend.FLASH_ATTN_V3)
            except ImportError:
                pass

        if cap >= DeviceCapability(9, 0):
            backends.insert(0, AttentionBackend.FLASHINFER)

        backends.extend(
            [
                AttentionBackend.XFORMERS,
                AttentionBackend.TORCH_SDPA,
                AttentionBackend.PAGED_ATTENTION,
                AttentionBackend.DEFAULT,
            ]
        )

        return backends

    def empty_cache(self) -> None:
        torch = self._get_torch()
        torch.cuda.empty_cache()

    def synchronize(self, device_id: int = 0) -> None:
        torch = self._get_torch()
        with torch.cuda.device(device_id):
            torch.cuda.synchronize()

    def set_device(self, device_id: int) -> None:
        torch = self._get_torch()
        torch.cuda.set_device(device_id)

    def get_current_device(self) -> int:
        torch = self._get_torch()
        return torch.cuda.current_device()


# ============================================================================
# ROCm Platform
# ============================================================================


class RocmPlatform(Platform):
    """AMD ROCm platform implementation."""

    _torch = None

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.ROCM

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch

            return torch.cuda.is_available() and hasattr(torch.version, "hip")
        except ImportError:
            return False

    def _get_torch(self):
        if self._torch is None:
            import torch

            self._torch = torch
        return self._torch

    def get_device_count(self) -> int:
        torch = self._get_torch()
        return torch.cuda.device_count()

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        # ROCm uses different capability naming
        torch = self._get_torch()
        props = torch.cuda.get_device_properties(device_id)
        # Map ROCm architecture to capability
        name = props.name.lower()
        if "mi300" in name:
            return DeviceCapability(9, 4)
        elif "mi250" in name:
            return DeviceCapability(9, 0)
        elif "mi100" in name:
            return DeviceCapability(8, 6)
        return DeviceCapability(8, 0)

    def get_device_name(self, device_id: int = 0) -> str:
        torch = self._get_torch()
        return torch.cuda.get_device_name(device_id)

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        torch = self._get_torch()
        props = torch.cuda.get_device_properties(device_id)
        total = props.total_memory
        reserved = torch.cuda.memory_reserved(device_id)
        allocated = torch.cuda.memory_allocated(device_id)
        free = total - reserved
        return MemoryInfo(
            total_bytes=total,
            free_bytes=free,
            used_bytes=allocated,
            reserved_bytes=reserved,
        )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        features = DeviceFeature.FP16 | DeviceFeature.BF16 | DeviceFeature.INT8

        name = self.get_device_name(device_id).lower()
        if "mi250" in name or "mi300" in name:
            features |= (
                DeviceFeature.TENSOR_CORES
                | DeviceFeature.FLASH_ATTENTION
                | DeviceFeature.INFINITY_FABRIC
            )

        if self.get_device_count() > 1:
            features |= DeviceFeature.MULTI_GPU

        return features

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {
            QuantizationType.NONE,
            QuantizationType.INT8,
            QuantizationType.GPTQ,
            QuantizationType.AWQ,
        }

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [
            AttentionBackend.ROCM,
            AttentionBackend.TRITON,
            AttentionBackend.TORCH_SDPA,
            AttentionBackend.DEFAULT,
        ]

    def empty_cache(self) -> None:
        torch = self._get_torch()
        torch.cuda.empty_cache()

    def synchronize(self, device_id: int = 0) -> None:
        torch = self._get_torch()
        torch.cuda.synchronize()


# ============================================================================
# TPU Platform
# ============================================================================


class TpuPlatform(Platform):
    """Google TPU platform implementation."""

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.TPU

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch_xla

            return True
        except ImportError:
            return False

    def get_device_count(self) -> int:
        try:
            import torch_xla.core.xla_model as xm

            return xm.xrt_world_size()
        except Exception:
            return 1

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        # TPU v4/v5 mapped to pseudo-capability
        return DeviceCapability(major=4, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        return f"TPU-v4-{device_id}"

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        # TPU v4 has 32GB HBM per chip
        total = 32 * (1024**3)
        return MemoryInfo(
            total_bytes=total,
            free_bytes=total,
            used_bytes=0,
            reserved_bytes=0,
        )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        return (
            DeviceFeature.BF16
            | DeviceFeature.TENSOR_CORES
            | DeviceFeature.MULTI_GPU
        )

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {QuantizationType.NONE, QuantizationType.INT8}

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.TPU, AttentionBackend.DEFAULT]


# ============================================================================
# XPU Platform (Intel)
# ============================================================================


class XpuPlatform(Platform):
    """Intel XPU (GPU/Accelerator) platform implementation."""

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.XPU

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch
            import intel_extension_for_pytorch

            return hasattr(torch, "xpu") and torch.xpu.is_available()
        except ImportError:
            return False

    def get_device_count(self) -> int:
        try:
            import torch

            return torch.xpu.device_count()
        except Exception:
            return 0

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=1, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        try:
            import torch

            return torch.xpu.get_device_name(device_id)
        except Exception:
            return f"Intel-XPU-{device_id}"

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        try:
            import torch

            props = torch.xpu.get_device_properties(device_id)
            total = props.total_memory
            return MemoryInfo(
                total_bytes=total,
                free_bytes=total,
                used_bytes=0,
                reserved_bytes=0,
            )
        except Exception:
            return MemoryInfo(
                total_bytes=0, free_bytes=0, used_bytes=0, reserved_bytes=0
            )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        return DeviceFeature.FP16 | DeviceFeature.BF16

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {QuantizationType.NONE, QuantizationType.INT8}

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.TORCH_SDPA, AttentionBackend.DEFAULT]


# ============================================================================
# CPU Platform
# ============================================================================


class CpuPlatform(Platform):
    """CPU-only platform implementation."""

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.CPU

    @classmethod
    def is_available(cls) -> bool:
        return True

    def get_device_count(self) -> int:
        return 1

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=0, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        return platform.processor() or "CPU"

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        try:
            import psutil

            vm = psutil.virtual_memory()
            return MemoryInfo(
                total_bytes=vm.total,
                free_bytes=vm.available,
                used_bytes=vm.used,
                reserved_bytes=0,
            )
        except ImportError:
            return MemoryInfo(
                total_bytes=0, free_bytes=0, used_bytes=0, reserved_bytes=0
            )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        features = DeviceFeature.FP16

        # Check for AVX support
        try:
            import cpuinfo

            info = cpuinfo.get_cpu_info()
            flags = info.get("flags", [])
            if "avx512f" in flags:
                features |= DeviceFeature.BF16
        except ImportError:
            pass

        return features

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {
            QuantizationType.NONE,
            QuantizationType.INT8,
            QuantizationType.GGUF,
        }

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.CPU, AttentionBackend.TORCH_SDPA, AttentionBackend.DEFAULT]


# ============================================================================
# Platform Registry
# ============================================================================


class PlatformRegistry:
    """Registry for platform implementations."""

    _platforms: Dict[PlatformType, Type[Platform]] = {}
    _current: Optional[Platform] = None
    _lock = threading.Lock()

    @classmethod
    def register(cls, platform_type: PlatformType, platform_cls: Type[Platform]) -> None:
        """Register a platform implementation."""
        cls._platforms[platform_type] = platform_cls

    @classmethod
    def get_platform(cls, platform_type: PlatformType) -> Optional[Platform]:
        """Get platform instance by type."""
        if platform_type not in cls._platforms:
            return None
        platform_cls = cls._platforms[platform_type]
        if platform_cls.is_available():
            return platform_cls()
        return None

    @classmethod
    def detect_current(cls) -> Platform:
        """Detect and return current platform."""
        with cls._lock:
            if cls._current is not None:
                return cls._current

            # Priority order for platform detection
            priority = [
                PlatformType.CUDA,
                PlatformType.ROCM,
                PlatformType.TPU,
                PlatformType.XPU,
                PlatformType.CPU,
            ]

            for ptype in priority:
                if ptype in cls._platforms:
                    platform_cls = cls._platforms[ptype]
                    if platform_cls.is_available():
                        cls._current = platform_cls()
                        logger.info(f"Detected platform: {ptype.value}")
                        return cls._current

            # Fallback to CPU
            cls._current = CpuPlatform()
            return cls._current

    @classmethod
    def get_current(cls) -> Platform:
        """Get current platform (cached)."""
        if cls._current is None:
            return cls.detect_current()
        return cls._current

    @classmethod
    def reset(cls) -> None:
        """Reset cached platform."""
        with cls._lock:
            cls._current = None


# Register default platforms
PlatformRegistry.register(PlatformType.CUDA, CudaPlatform)
PlatformRegistry.register(PlatformType.ROCM, RocmPlatform)
PlatformRegistry.register(PlatformType.TPU, TpuPlatform)
PlatformRegistry.register(PlatformType.XPU, XpuPlatform)
PlatformRegistry.register(PlatformType.CPU, CpuPlatform)


# ============================================================================
# Convenience Functions
# ============================================================================


def get_current_platform() -> Platform:
    """Get current platform instance."""
    return PlatformRegistry.get_current()


def detect_platform() -> PlatformType:
    """Detect current platform type."""
    return get_current_platform().get_platform_type()


def get_device_count() -> int:
    """Get number of available devices."""
    return get_current_platform().get_device_count()


def get_device_capability(device_id: int = 0) -> DeviceCapability:
    """Get device compute capability."""
    return get_current_platform().get_device_capability(device_id)


def get_memory_info(device_id: int = 0) -> MemoryInfo:
    """Get device memory information."""
    return get_current_platform().get_memory_info(device_id)


def is_quantization_supported(quant_type: QuantizationType) -> bool:
    """Check if quantization type is supported on current platform."""
    return get_current_platform().supports_quantization(quant_type)


def select_attention_backend(
    preferred: Optional[AttentionBackend] = None,
) -> AttentionBackend:
    """Select best attention backend for current platform."""
    return get_current_platform().select_attention_backend(preferred)


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_platform_fingerprint(platform: Platform) -> Optional[str]:
    """Try to use Rust-accelerated platform fingerprinting."""
    try:
        from rust_core import platform_fingerprint_rust

        device_infos = []
        for i in range(min(platform.get_device_count(), 8)):
            info = platform.get_device_info(i)
            device_infos.append(
                {
                    "name": info.name,
                    "capability": str(info.capability),
                    "memory": info.memory.total_bytes,
                }
            )

        return platform_fingerprint_rust(
            platform.get_platform_type().value, device_infos
        )
    except ImportError:
        return None

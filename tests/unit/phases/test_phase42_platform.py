#!/usr/bin/env python3
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

"""
Phase 42: Platform Abstraction Interface Tests
"""

import pytest
from unittest.mock import patch, MagicMock


class TestPlatformEnums:
    """Test platform enums."""

    def test_platform_type_values(self):
        """Test PlatformType enum values."""
        from src.infrastructure.services.platform.platform_interface import PlatformType

        assert PlatformType.CUDA.value == "cuda"
        assert PlatformType.ROCM.value == "rocm"
        assert PlatformType.TPU.value == "tpu"
        assert PlatformType.XPU.value == "xpu"
        assert PlatformType.CPU.value == "cpu"

    def test_cpu_architecture_values(self):
        """Test CpuArchitecture enum."""
        from src.infrastructure.services.platform.platform_interface import CpuArchitecture

        assert CpuArchitecture.X86_64.value == "x86_64"
        assert CpuArchitecture.ARM64.value == "arm64"
        assert CpuArchitecture.AARCH64.value == "aarch64"

    def test_quantization_type_values(self):
        """Test QuantizationType enum."""
        from src.infrastructure.services.platform.platform_interface import QuantizationType

        assert QuantizationType.NONE.value == "none"
        assert QuantizationType.GPTQ.value == "gptq"
        assert QuantizationType.AWQ.value == "awq"
        assert QuantizationType.FP8.value == "fp8"

    def test_attention_backend_values(self):
        """Test AttentionBackend enum."""
        from src.infrastructure.services.platform.platform_interface import AttentionBackend

        assert AttentionBackend.FLASH_ATTN.value == "flash_attn"
        assert AttentionBackend.XFORMERS.value == "xformers"
        assert AttentionBackend.TORCH_SDPA.value == "torch_sdpa"

    def test_device_feature_flags(self):
        """Test DeviceFeature flag composition."""
        from src.infrastructure.services.platform.platform_interface import DeviceFeature

        combined = DeviceFeature.FP16 | DeviceFeature.BF16
        assert bool(combined & DeviceFeature.FP16)
        assert bool(combined & DeviceFeature.BF16)
        assert not bool(combined & DeviceFeature.FP8)


class TestDeviceCapability:
    """Test DeviceCapability named tuple."""

    def test_capability_creation(self):
        """Test creating DeviceCapability."""
        from src.infrastructure.services.platform.platform_interface import DeviceCapability

        cap = DeviceCapability(major=8, minor=6)
        assert cap.major == 8
        assert cap.minor == 6

    def test_capability_string(self):
        """Test string representation."""
        from src.infrastructure.services.platform.platform_interface import DeviceCapability

        cap = DeviceCapability(major=8, minor=0)
        assert str(cap) == "8.0"

    def test_capability_comparison(self):
        """Test capability comparison."""
        from src.infrastructure.services.platform.platform_interface import DeviceCapability

        cap80 = DeviceCapability(8, 0)
        cap86 = DeviceCapability(8, 6)
        cap90 = DeviceCapability(9, 0)

        assert cap86 >= cap80
        assert cap90 > cap86
        assert not cap80 > cap86

    def test_capability_as_int(self):
        """Test as_int property."""
        from src.infrastructure.services.platform.platform_interface import DeviceCapability

        cap = DeviceCapability(8, 6)
        assert cap.as_int == 86


class TestMemoryInfo:
    """Test MemoryInfo dataclass."""

    def test_memory_info_creation(self):
        """Test creating MemoryInfo."""
        from src.infrastructure.services.platform.platform_interface import MemoryInfo

        mem = MemoryInfo(
            total_bytes=16 * (1024**3),
            free_bytes=8 * (1024**3),
            used_bytes=6 * (1024**3),
            reserved_bytes=2 * (1024**3),
        )
        assert mem.total_bytes == 16 * (1024**3)

    def test_memory_gb_properties(self):
        """Test GB conversion properties."""
        from src.infrastructure.services.platform.platform_interface import MemoryInfo

        mem = MemoryInfo(
            total_bytes=16 * (1024**3),
            free_bytes=8 * (1024**3),
            used_bytes=6 * (1024**3),
        )
        assert mem.total_gb == 16.0
        assert mem.free_gb == 8.0
        assert mem.used_gb == 6.0

    def test_utilization(self):
        """Test memory utilization calculation."""
        from src.infrastructure.services.platform.platform_interface import MemoryInfo

        mem = MemoryInfo(
            total_bytes=100,
            free_bytes=40,
            used_bytes=60,
        )
        assert mem.utilization == 60.0


class TestDeviceInfo:
    """Test DeviceInfo dataclass."""

    def test_device_info_creation(self):
        """Test creating DeviceInfo."""
        from src.infrastructure.services.platform.platform_interface import (
            DeviceInfo,
            DeviceCapability,
            MemoryInfo,
            PlatformType,
            DeviceFeature,
        )

        info = DeviceInfo(
            device_id=0,
            name="NVIDIA A100-SXM4-80GB",
            platform=PlatformType.CUDA,
            capability=DeviceCapability(8, 0),
            memory=MemoryInfo(80 * (1024**3), 70 * (1024**3), 10 * (1024**3)),
            features=DeviceFeature.FP16 | DeviceFeature.BF16,
        )
        assert info.name == "NVIDIA A100-SXM4-80GB"
        assert info.is_datacenter

    def test_supports_feature(self):
        """Test feature support check."""
        from src.infrastructure.services.platform.platform_interface import (
            DeviceInfo,
            DeviceCapability,
            MemoryInfo,
            PlatformType,
            DeviceFeature,
        )

        info = DeviceInfo(
            device_id=0,
            name="Test GPU",
            platform=PlatformType.CUDA,
            capability=DeviceCapability(8, 0),
            memory=MemoryInfo(16 * (1024**3), 10 * (1024**3), 6 * (1024**3)),
            features=DeviceFeature.FP16 | DeviceFeature.TENSOR_CORES,
        )
        assert info.supports_feature(DeviceFeature.FP16)
        assert info.supports_feature(DeviceFeature.TENSOR_CORES)
        assert not info.supports_feature(DeviceFeature.FP8)


class TestCpuPlatform:
    """Test CPU platform implementation."""

    def test_cpu_always_available(self):
        """Test CPU platform is always available."""
        from src.infrastructure.services.platform.platform_interface import CpuPlatform

        assert CpuPlatform.is_available() is True

    def test_cpu_device_count(self):
        """Test CPU device count is 1."""
        from src.infrastructure.services.platform.platform_interface import CpuPlatform

        platform = CpuPlatform()
        assert platform.get_device_count() == 1

    def test_cpu_capability(self):
        """Test CPU capability is (0, 0)."""
        from src.infrastructure.services.platform.platform_interface import CpuPlatform

        platform = CpuPlatform()
        cap = platform.get_device_capability()
        assert cap.major == 0
        assert cap.minor == 0

    def test_cpu_platform_type(self):
        """Test CPU platform type."""
        from src.infrastructure.services.platform.platform_interface import (
            CpuPlatform,
            PlatformType,
        )

        assert CpuPlatform.get_platform_type() == PlatformType.CPU

    def test_cpu_quantizations(self):
        """Test CPU supported quantizations."""
        from src.infrastructure.services.platform.platform_interface import (
            CpuPlatform,
            QuantizationType,
        )

        platform = CpuPlatform()
        quants = platform.get_supported_quantizations()
        assert QuantizationType.NONE in quants
        assert QuantizationType.INT8 in quants
        assert QuantizationType.GGUF in quants


class TestPlatformRegistry:
    """Test PlatformRegistry."""

    def test_registry_singleton(self):
        """Test registry is singleton pattern."""
        from src.infrastructure.services.platform.platform_interface import PlatformRegistry

        PlatformRegistry.reset()
        p1 = PlatformRegistry.get_current()
        p2 = PlatformRegistry.get_current()
        assert p1 is p2

    def test_detect_platform(self):
        """Test platform detection returns valid platform."""
        from src.infrastructure.services.platform.platform_interface import (
            PlatformRegistry,
            Platform,
        )

        PlatformRegistry.reset()
        platform = PlatformRegistry.detect_current()
        assert isinstance(platform, Platform)

    def test_get_all_tools(self):
        """Test getting all tools from registry."""
        from src.infrastructure.services.platform.platform_interface import PlatformRegistry

        # Just verify it returns a platform
        PlatformRegistry.reset()
        platform = PlatformRegistry.get_current()
        assert platform is not None


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_get_current_platform(self):
        """Test get_current_platform."""
        from src.infrastructure.services.platform.platform_interface import (
            get_current_platform,
            Platform,
        )

        platform = get_current_platform()
        assert isinstance(platform, Platform)

    def test_detect_platform(self):
        """Test detect_platform returns PlatformType."""
        from src.infrastructure.services.platform.platform_interface import (
            detect_platform,
            PlatformType,
        )

        ptype = detect_platform()
        assert isinstance(ptype, PlatformType)

    def test_get_device_count(self):
        """Test get_device_count returns positive integer."""
        from src.infrastructure.services.platform.platform_interface import get_device_count

        count = get_device_count()
        assert isinstance(count, int)
        assert count >= 1

    def test_is_quantization_supported(self):
        """Test quantization support check."""
        from src.infrastructure.services.platform.platform_interface import (
            is_quantization_supported,
            QuantizationType,
        )

        # NONE should always be supported
        assert is_quantization_supported(QuantizationType.NONE)

    def test_select_attention_backend(self):
        """Test attention backend selection."""
        from src.infrastructure.services.platform.platform_interface import (
            select_attention_backend,
            AttentionBackend,
        )

        backend = select_attention_backend()
        assert isinstance(backend, AttentionBackend)


class TestPlatformConfig:
    """Test PlatformConfig dataclass."""

    def test_platform_config_defaults(self):
        """Test PlatformConfig default values."""
        from src.infrastructure.services.platform.platform_interface import (
            PlatformConfig,
            PlatformType,
        )

        config = PlatformConfig(platform_type=PlatformType.CUDA)
        assert config.memory_fraction == 0.9
        assert config.enable_cuda_graphs is True
        assert config.enable_flash_attention is True


class TestMockCudaPlatform:
    """Test CUDA platform with mocks."""

    @pytest.fixture
    def mock_torch(self):
        """Create mock torch module."""
        mock = MagicMock()
        mock.cuda.is_available.return_value = True
        mock.cuda.device_count.return_value = 2
        mock.cuda.get_device_capability.return_value = (8, 0)
        mock.cuda.get_device_name.return_value = "NVIDIA A100"

        props = MagicMock()
        props.total_memory = 80 * (1024**3)
        mock.cuda.get_device_properties.return_value = props
        mock.cuda.memory_reserved.return_value = 10 * (1024**3)
        mock.cuda.memory_allocated.return_value = 5 * (1024**3)
        mock.version.cuda = "12.1"

        return mock

    def test_cuda_platform_with_mock(self, mock_torch):
        """Test CUDA platform with mocked torch."""
        from src.infrastructure.services.platform.platform_interface import CudaPlatform

        with patch.dict("sys.modules", {"torch": mock_torch}):
            platform = CudaPlatform()
            platform._torch = mock_torch

            assert platform.get_device_count() == 2
            cap = platform.get_device_capability()
            assert cap.major == 8
            assert cap.minor == 0

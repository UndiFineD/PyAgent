from .registry import (
    ModelCapability,
    ModelArchitecture,
    QuantizationType,
    ModelFormat,
    ModelConfig,
    ArchitectureSpec,
    ModelInfo,
    VRAMEstimate,
    ArchitectureDetector,
    VRAMEstimator,
    ModelRegistry,
)

# Helper functions for singleton access
def register_model(spec: ArchitectureSpec) -> None:
    """Register a model architecture."""
    ModelRegistry().register(spec)

def get_model_info(name: str, config: dict = None) -> ModelInfo:
    """Get information for a model."""
    return ModelRegistry().get_model_info(name, config)

def detect_architecture(name: str, config: dict = None) -> ModelArchitecture:
    """Detect architecture from name or config."""
    if config:
        return ArchitectureDetector.detect_from_config(config)
    return ArchitectureDetector.detect_from_name(name)

def estimate_vram(name: str, ctx: int = 4096, quant: QuantizationType = QuantizationType.NONE) -> VRAMEstimate:
    """Estimate VRAM usage for a model."""
    return ModelRegistry().estimate_vram(name, ctx=ctx, quant=quant)

__all__ = [
    "ModelCapability",
    "ModelArchitecture",
    "QuantizationType",
    "ModelFormat",
    "ModelConfig",
    "ArchitectureSpec",
    "ModelInfo",
    "VRAMEstimate",
    "ArchitectureDetector",
    "VRAMEstimator",
    "ModelRegistry",
    "register_model",
    "get_model_info",
    "detect_architecture",
    "estimate_vram"
]


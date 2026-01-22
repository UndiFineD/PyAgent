"""
Manager for response post-processing and multimodal inputs.
(Facade for src.core.base.common.processor_core)
"""
from src.core.base.common.processor_core import (
    ProcessorCore as ResponsePostProcessor,
    ProcessorCore as MultimodalProcessor
)
from src.core.base.common.serialization_core import SerializationCore as SerializationManager


from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
from typing import TYPE_CHECKING
from .config import QuantConfig
from .tensor import QuantizedTensor

if TYPE_CHECKING:
    from numpy.typing import NDArray

class Quantizer(ABC):
    """Base class for quantization algorithms."""
    
    def __init__(self, config: QuantConfig):
        self.config = config
    
    @abstractmethod
    def quantize(
        self,
        weight: NDArray[np.float32],
    ) -> QuantizedTensor:
        pass
    
    @abstractmethod
    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        pass

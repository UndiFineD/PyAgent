# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\seed-vc\dac\__init__.py
__version__ = "1.0.0"

# preserved here for legacy reasons
__model_version__ = "latest"

import audiotools

audiotools.ml.BaseModel.INTERN += ["dac.**"]
audiotools.ml.BaseModel.EXTERN += ["einops"]


from . import model, nn, utils
from .model import DAC, DACFile

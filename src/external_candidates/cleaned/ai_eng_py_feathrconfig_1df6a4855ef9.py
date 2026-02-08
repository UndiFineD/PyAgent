# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\definition.py\feathrconfig_1df6a4855ef9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\definition\feathrconfig.py

from abc import ABC, abstractmethod

class HoconConvertible(ABC):

    """Represent classes that can convert into Feathr HOCON config."""

    @abstractmethod

    def to_feature_config(self) -> str:

        """Convert the feature anchor definition into internal HOCON format. (For internal use ony)"""

        pass


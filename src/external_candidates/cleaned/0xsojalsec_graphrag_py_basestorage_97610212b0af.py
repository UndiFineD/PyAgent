# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\storage.py\basestorage_97610212b0af.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Storage\BaseStorage.py

from dataclasses import dataclass, field

from typing import Any, Optional

from Core.Storage.NameSpace import Namespace


@dataclass
class BaseStorage:
    config: Optional[Any] = field(default=None)

    namespace: Optional[Namespace] = field(default=None)

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\schema.py\chunkschema_1f04e76df401.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Schema\ChunkSchema.py

from dataclasses import asdict, dataclass


@dataclass
class TextChunk:
    def __init__(
        self,
        tokens,
        chunk_id: str,
        content: str,
        doc_id: str,
        index: int,
        title: str = None,
    ):
        self.tokens: int = tokens

        self.chunk_id: str = chunk_id

        self.content: str = content

        self.doc_id: str = doc_id

        self.index: int = index

        self.title: str = title

    @property
    def as_dict(self):
        return asdict(self)

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\chunk.py\chunkfactory_a7b9635d6de2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Chunk\ChunkFactory.py

from collections import defaultdict

from typing import Any

from Core.Common.Utils import mdhash_id

from Core.Schema.ChunkSchema import TextChunk


class ChunkingFactory:
    chunk_methods: dict = defaultdict(Any)

    def register_chunking_method(
        self,
        method_name: str,
        method_func=None,  # can be any classes or functions
    ):
        if self.has_chunk_method(method_name):
            return

        self.chunk_methods[method_name] = method_func

    def has_chunk_method(self, key: str) -> Any:
        return key in self.chunk_methods

    def get_method(self, key) -> Any:
        return self.chunk_methods.get(key)


# Registry instance

CHUNKING_REGISTRY = ChunkingFactory()


def register_chunking_method(method_name):
    """Register a new chunking method

    This is a decorator that can be used to register a new chunking method.

    The method will be stored in the self.methods dictionary.

    Parameters

    ----------

    method_name: str

        The name of the chunking method.

    """

    def decorator(func):
        """Register a new chunking method"""

        CHUNKING_REGISTRY.register_chunking_method(method_name, func)

    return decorator


def create_chunk_method(method_name):
    chunking_method = CHUNKING_REGISTRY.get_method(method_name)

    return chunking_method

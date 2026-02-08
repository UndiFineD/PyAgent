# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\storage.py\basekvstorage_2561388d211f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Storage\BaseKVStorage.py

from dataclasses import dataclass, field

from typing import Generic, Literal, TypedDict, TypeVar, Union

from Core.Storage.BaseStorage import BaseStorage

T = TypeVar("T")


class BaseKVStorage(Generic[T], BaseStorage):
    async def all_keys(self) -> list[str]:
        raise NotImplementedError

    async def get_by_id(self, id: str) -> Union[T, None]:
        raise NotImplementedError

    async def get_by_ids(self, ids: list[str], fields: Union[set[str], None] = None) -> list[Union[T, None]]:
        raise NotImplementedError

    async def filter_keys(self, data: list[str]) -> set[str]:
        """return un-exist keys"""

        raise NotImplementedError

    async def upsert(self, data: dict[str, T]):
        raise NotImplementedError

    async def drop(self):
        raise NotImplementedError

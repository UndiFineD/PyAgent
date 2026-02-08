# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\oxm.py\milvus.py\base_converter_96c029d78984.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\oxm\milvus\base_converter.py

"""

Milvus collection converter base class

Provides basic functionality for converting arbitrary data sources to Milvus collections.

All Milvus collection converters should inherit from this base class to obtain a unified conversion interface.

"""

from abc import ABC, abstractmethod

from typing import Any, Generic, Type, TypeVar, get_args, get_origin

from core.observation.logger import get_logger

from core.oxm.milvus.milvus_collection_base import MilvusCollectionBase

logger = get_logger(__name__)

# Generic type variable - only restricts Milvus collection type

MilvusCollectionType = TypeVar("MilvusCollectionType", bound=MilvusCollectionBase)


class BaseMilvusConverter(ABC, Generic[MilvusCollectionType]):
    """

    Milvus collection converter base class

    Provides basic functionality for converting arbitrary data sources to Milvus collections.

    All Milvus collection converters should inherit from this class.

    Features:

    - Unified conversion interface (class methods)

    - Type-safe Milvus collection generic support

    - Automatically retrieves Milvus collection type from generics

    - Flexible data source support

    """

    @classmethod
    def get_milvus_model(cls) -> Type[MilvusCollectionType]:
        """

        Retrieve the Milvus collection model type from generic information

        Returns:

            Type[MilvusCollectionType]: Milvus collection model class

        """

        # Get the generic base class of the current class

        if hasattr(cls, "__orig_bases__"):
            for base in cls.__orig_bases__:
                if get_origin(base) is BaseMilvusConverter:
                    args = get_args(base)

                    if args:
                        return args[0]

        raise ValueError(f"Unable to retrieve Milvus collection type from generic information of {cls.__name__}")

    @classmethod
    @abstractmethod
    def from_mongo(cls, source_doc: Any) -> MilvusCollectionType:
        """

        Convert from data source to Milvus collection entity

        This is the core conversion method; subclasses must implement specific conversion logic.

        Args:

            source_doc: Source data (can be of any type)

        Returns:

            MilvusCollectionType: Instance of Milvus collection entity

        Raises:

            Exception: Raises an exception when an error occurs during conversion

        """

        raise NotImplementedError("Subclasses must implement the from_mongo method")

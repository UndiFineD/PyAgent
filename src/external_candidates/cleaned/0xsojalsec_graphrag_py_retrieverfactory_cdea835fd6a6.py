# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\retriever.py\retrieverfactory_cdea835fd6a6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Retriever\RetrieverFactory.py

# Registry instance

from collections import defaultdict

from typing import Any


class RetrieverFactory:
    retriever_methods: dict = defaultdict(dict)

    def register_retriever_method(
        self,
        type: str,
        method_name: str,
        method_func=None,  # can be any classes or functions
    ):
        if self.has_retriever_method(type, method_name):
            return

        self.retriever_methods[type][method_name] = method_func

    def has_retriever_method(self, type: str, key: str) -> Any:
        return (type in self.retriever_methods) and (key in self.retriever_methods[type])

    def get_method(self, type, key) -> Any:
        return self.retriever_methods.get(type).get(key)


RETRIEVER_REGISTRY = RetrieverFactory()


def register_retriever_method(type, method_name):
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

        RETRIEVER_REGISTRY.register_retriever_method(type, method_name, func)

    return decorator


def get_retriever_operator(type, method_name):
    retriever_operator = RETRIEVER_REGISTRY.get_method(type, method_name)

    return retriever_operator

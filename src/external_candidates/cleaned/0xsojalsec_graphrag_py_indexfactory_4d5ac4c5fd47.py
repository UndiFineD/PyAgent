# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\index.py\indexfactory_4d5ac4c5fd47.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Index\IndexFactory.py

import os

import faiss

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage

from Core.Common.BaseFactory import ConfigBasedFactory

from Core.Index.ColBertIndex import ColBertIndex

from Core.Index.FaissIndex import FaissIndex

from Core.Index.Schema import (
    BaseIndexConfig,
    ColBertIndexConfig,
    FAISSIndexConfig,
    VectorIndexConfig,
)

from Core.Index.VectorIndex import VectorIndex


class RAGIndexFactory(ConfigBasedFactory):
    def __init__(self):
        creators = {
            VectorIndexConfig: self._create_vector_index,
            ColBertIndexConfig: self._create_colbert,
            FAISSIndexConfig: self._create_faiss,
        }

        super().__init__(creators)

    def get_index(self, config: BaseIndexConfig):
        """Key is IndexType."""

        return super().get_instance(config)

    @classmethod
    def _create_vector_index(cls, config):
        return VectorIndex(config)

    @classmethod
    def _create_colbert(cls, config: ColBertIndexConfig):
        return ColBertIndex(config)

    def _create_faiss(self, config):
        return FaissIndex(config)


get_index = RAGIndexFactory().get_index

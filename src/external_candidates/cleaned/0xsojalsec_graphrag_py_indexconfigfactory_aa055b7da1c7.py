# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graphrag.py\core.py\index.py\indexconfigfactory_aa055b7da1c7.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GraphRAG\Core\Index\IndexConfigFactory.py

"""

Index Config Factory.

"""

from Core.Index import get_rag_embedding

from Core.Index.Schema import ColBertIndexConfig, FAISSIndexConfig, VectorIndexConfig


class IndexConfigFactory:
    def __init__(self):
        self.creators = {
            "vector": self._create_vector_config,
            "colbert": self._create_colbert_config,
            "faiss": self._create_faiss_config,
        }

    def get_config(self, config, persist_path):
        """Key is PersistType."""

        return self.creators[config.vdb_type](config, persist_path)

    @staticmethod
    def _create_vector_config(config, persist_path):
        return VectorIndexConfig(
            persist_path=persist_path,
            embed_model=get_rag_embedding(config.embedding.api_type, config),
        )

    @staticmethod
    def _create_faiss_config(config, persist_path):
        return FAISSIndexConfig(
            persist_path=persist_path,
            embed_model=get_rag_embedding(config.embedding.api_type, config),
        )

    @staticmethod
    def _create_colbert_config(config, persist_path):
        return ColBertIndexConfig(
            persist_path=persist_path,
            index_name="nbits_2",
            model_name=config.colbert_checkpoint_path,
            nbits=2,
        )


get_index_config = IndexConfigFactory().get_config

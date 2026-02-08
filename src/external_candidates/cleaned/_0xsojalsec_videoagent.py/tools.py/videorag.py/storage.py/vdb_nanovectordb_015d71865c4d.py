# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\_storage\vdb_nanovectordb.py
import asyncio
import os
from dataclasses import dataclass

import numpy as np
import torch
from imagebind.models import imagebind_model
from nano_vectordb import NanoVectorDB
from tqdm import tqdm

from .._utils import logger
from .._videoutil import encode_string_query, encode_video_segments
from ..base import BaseVectorStorage


@dataclass
class NanoVectorDBVideoSegmentStorage(BaseVectorStorage):
    embedding_func = None
    segment_retrieval_top_k: float = 2

    def __post_init__(self):
        self._client_file_name = os.path.join(self.global_config["working_dir"], f"vdb_{self.namespace}.json")
        self._max_batch_size = self.global_config["video_embedding_batch_num"]
        self._client = NanoVectorDB(
            self.global_config["video_embedding_dim"],
            storage_file=self._client_file_name,
        )
        self.top_k = self.global_config.get("segment_retrieval_top_k", self.segment_retrieval_top_k)

    async def upsert(self, video_name, segment_index2name, video_output_format):
        import os

        # Determine the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

        # Store the original working directory
        original_dir = os.getcwd()

        # Change to the project root directory
        os.chdir(project_root)

        # Load the model (this will look for .checkpoints relative to the project root)
        embedder = imagebind_model.imagebind_huge(pretrained=True).cuda()

        # Change back to the original directory
        os.chdir(original_dir)
        embedder.eval()

        logger.info(f"Inserting {len(segment_index2name)} segments to {self.namespace}")
        if not len(segment_index2name):
            logger.warning("You insert an empty data to vector DB")
            return []
        list_data, video_paths = [], []
        cache_path = os.path.join(self.global_config["working_dir"], "_cache", video_name)
        index_list = list(segment_index2name.keys())
        for index in index_list:
            list_data.append(
                {
                    "__id__": f"{video_name}_{index}",
                    "__video_name__": video_name,
                    "__index__": index,
                }
            )
            segment_name = segment_index2name[index]
            video_file = os.path.join(cache_path, f"{segment_name}.{video_output_format}")
            video_paths.append(video_file)
        batches = [video_paths[i : i + self._max_batch_size] for i in range(0, len(video_paths), self._max_batch_size)]
        embeddings = []
        for _batch in tqdm(batches, desc=f"Encoding Video Segments {video_name}"):
            batch_embeddings = encode_video_segments(_batch, embedder)
            embeddings.append(batch_embeddings)
        embeddings = torch.concat(embeddings, dim=0)
        embeddings = embeddings.numpy()
        for i, d in enumerate(list_data):
            d["__vector__"] = embeddings[i]
        results = self._client.upsert(datas=list_data)
        return results

    async def query(self, query: str):
        import os

        # Determine the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

        # Store the original working directory
        original_dir = os.getcwd()

        # Change to the project root directory
        os.chdir(project_root)

        # Load the model (this will look for .checkpoints relative to the project root)
        embedder = imagebind_model.imagebind_huge(pretrained=True).cuda()

        # Change back to the original directory
        os.chdir(original_dir)
        embedder.eval()

        embedding = encode_string_query(query, embedder)
        embedding = embedding[0]
        results = self._client.query(
            query=embedding,
            top_k=self.top_k,
            better_than_threshold=-1,
        )
        results = [{**dp, "id": dp["__id__"], "distance": dp["__metrics__"]} for dp in results]
        return results

    async def index_done_callback(self):
        self._client.save()

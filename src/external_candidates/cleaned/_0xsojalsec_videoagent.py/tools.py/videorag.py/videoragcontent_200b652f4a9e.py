# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\tools\videorag\videoragcontent.py
import asyncio
import json
import multiprocessing
import os
import shutil
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from functools import partial
from typing import Callable, Dict, List, Optional, Type, Union, cast

import tiktoken
from environment.config.llm import gemini

from ._opcontent import videorag_query
from ._storage import JsonKVStorage, NanoVectorDBVideoSegmentStorage
from ._utils import (
    always_get_an_event_loop,
    logger,
)
from ._videoutil import (
    merge_segment_information,
    saving_video_segments,
    segment_caption,
    speech_to_text,
    split_video,
)
from .base import (
    BaseKVStorage,
    BaseVectorStorage,
    QueryParam,
    StorageNameSpace,
)


@dataclass
class VideoRAG:
    working_dir: str = field(default_factory=lambda: f"./videorag_cache_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}")

    # video
    threads_for_split: int = 10
    video_segment_length: int = 10  # 30 seconds
    rough_num_frames_per_segment: int = 3  # 5 frames
    video_output_format: str = "mp4"
    audio_output_format: str = "mp3"
    video_embedding_batch_num: int = 2
    segment_retrieval_top_k: int = 30
    video_embedding_dim: int = 1024

    # storage
    key_string_value_json_storage_cls: Type[BaseKVStorage] = JsonKVStorage
    vs_vector_db_storage_cls: Type[BaseVectorStorage] = NanoVectorDBVideoSegmentStorage
    enable_llm_cache: bool = True

    # extension
    always_create_working_dir: bool = True
    addon_params: dict = field(default_factory=dict)

    def __post_init__(self):
        _print_config = ",\n  ".join([f"{k} = {v}" for k, v in asdict(self).items()])
        logger.debug(f"VideoRAG init with param:\n\n  {_print_config}\n")

        if not os.path.exists(self.working_dir) and self.always_create_working_dir:
            logger.info(f"Creating working directory {self.working_dir}")
            os.makedirs(self.working_dir)

        self.video_path_db = self.key_string_value_json_storage_cls(namespace="video_path", global_config=asdict(self))

        self.video_segments = self.key_string_value_json_storage_cls(
            namespace="video_segments", global_config=asdict(self)
        )

        self.video_segment_feature_vdb = self.vs_vector_db_storage_cls(
            namespace="video_segment_feature",
            global_config=asdict(self),
            embedding_func=None,  # we code the embedding process inside the insert() function.
        )

    def insert_video(self, video_path_list=None):
        loop = always_get_an_event_loop()
        for video_path in video_path_list:
            # Step0: check the existence
            video_name = os.path.basename(video_path).split(".")[0]
            if video_name in self.video_segments._data:
                logger.info(f"Find the video named {os.path.basename(video_path)} in storage and skip it.")
                continue
            loop.run_until_complete(self.video_path_db.upsert({video_name: video_path}))

            # Step1: split the videos
            segment_index2name, segment_times_info = split_video(
                video_path,
                self.working_dir,
                self.video_segment_length,
                self.rough_num_frames_per_segment,
                self.audio_output_format,
            )

            # Step2: obtain transcript with whisper
            transcripts = speech_to_text(
                video_name,
                self.working_dir,
                segment_index2name,
                self.audio_output_format,
            )

            # Step3: saving video segments **as well as** obtain caption with Gemini API
            manager = multiprocessing.Manager()
            captions = manager.dict()
            error_queue = manager.Queue()

            process_saving_video_segments = multiprocessing.Process(
                target=saving_video_segments,
                args=(
                    video_name,
                    video_path,
                    self.working_dir,
                    segment_index2name,
                    segment_times_info,
                    error_queue,
                    self.video_output_format,
                ),
            )

            process_segment_caption = multiprocessing.Process(
                target=segment_caption,
                args=(
                    video_name,
                    video_path,
                    segment_index2name,
                    transcripts,
                    segment_times_info,
                    captions,
                    error_queue,
                ),
            )

            process_saving_video_segments.start()
            process_segment_caption.start()
            process_saving_video_segments.join()
            process_segment_caption.join()

            # if raise error in this two, stop the processing
            while not error_queue.empty():
                error_message = error_queue.get()
                with open("error_log_videorag.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"Video Name:{video_name} Error processing:\n{error_message}\n\n")
                raise RuntimeError(error_message)

            # Step4: insert video segments information
            segments_information = merge_segment_information(
                segment_index2name,
                segment_times_info,
                transcripts,
                dict(captions),  # Convert manager.dict to regular dict
            )
            manager.shutdown()
            loop.run_until_complete(self.video_segments.upsert({video_name: segments_information}))

            # Step5: encode video segment features
            loop.run_until_complete(
                self.video_segment_feature_vdb.upsert(
                    video_name,
                    segment_index2name,
                    self.video_output_format,
                )
            )

            # Step6: delete the cache file
            video_segment_cache_path = os.path.join(self.working_dir, "_cache", video_name)
            if os.path.exists(video_segment_cache_path):
                shutil.rmtree(video_segment_cache_path)

            # Step 7: saving current video information
            loop.run_until_complete(self._save_video_segments())

    def query(self, query: str, param: QueryParam = QueryParam()):
        loop = always_get_an_event_loop()
        return loop.run_until_complete(self.aquery(query, param))

    async def aquery(self, query: str, param: QueryParam = QueryParam()):
        if param.mode == "videoragcontent":
            response = await videorag_query(
                query,
                self.video_segment_feature_vdb,
                param,
                asdict(self),
            )
        else:
            raise ValueError(f"Unknown mode {param.mode}")

        return response

    async def _save_video_segments(self):
        tasks = []
        for storage_inst in [
            self.video_segment_feature_vdb,
            self.video_segments,
            self.video_path_db,
        ]:
            if storage_inst is None:
                continue
            tasks.append(cast(StorageNameSpace, storage_inst).index_done_callback())
        await asyncio.gather(*tasks)

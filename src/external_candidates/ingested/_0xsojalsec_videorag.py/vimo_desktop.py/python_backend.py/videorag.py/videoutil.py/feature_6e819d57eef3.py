# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoRAG\Vimo-desktop\python_backend\videorag\_videoutil\feature.py
import os
import pickle

import torch
from imagebind import data
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ImageBindModel, ModalityType
from tqdm import tqdm


def encode_video_segments(video_paths, embedder: ImageBindModel):
    device = next(embedder.parameters()).device
    inputs = {
        ModalityType.VISION: data.load_and_transform_video_data(video_paths, device),
    }
    with torch.no_grad():
        embeddings = embedder(inputs)[ModalityType.VISION]
    if isinstance(embeddings, torch.Tensor):
        embeddings = embeddings.cpu()
    return embeddings


def encode_string_query(query: str, embedder: ImageBindModel):
    device = next(embedder.parameters()).device
    inputs = {
        ModalityType.TEXT: data.load_and_transform_text([query], device),
    }
    with torch.no_grad():
        embeddings = embedder(inputs)[ModalityType.TEXT]
    if isinstance(embeddings, torch.Tensor):
        embeddings = embeddings.cpu()
    return embeddings

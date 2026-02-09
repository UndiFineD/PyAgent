# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\store\image_document.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/22 18:16
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: image_document.py
from typing import List, Optional, Union

from PIL.Image import Image
from pydantic import Field

from .document import Document


class ImageDocument(Document):
    """The basic class for an ImageDocument.

    Attributes:
        origin_image (Optional[Union[Image, str]]): The original image or base64.
        image_embedding (List[float]): Embedding data associated with the image.
        ocr_text (Optional[str]): Text extracted from the image using OCR.
        ocr_text_embedding (Optional[List[float]]): Embedding data associated with the OCR text.
    """

    origin_image: Optional[Union[Image, str]]
    image_embedding: List[float] = Field(default_factory=list)
    ocr_text: Optional[str]
    ocr_text_embedding: Optional[List[float]]

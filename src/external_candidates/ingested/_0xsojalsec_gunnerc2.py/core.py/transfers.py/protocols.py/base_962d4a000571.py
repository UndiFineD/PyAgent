# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\transfers\protocols\base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..state import TransferState


class TransferProtocol(ABC):
    @abstractmethod
    def init_download(self, st: TransferState) -> TransferState:
        """
        Initalize Download
        """

    @abstractmethod
    def next_download_chunk(self, st: TransferState) -> Optional[int]:
        """
        Next Download Chunk
        """

    @abstractmethod
    def init_upload(self, st: TransferState) -> TransferState:
        """
        Initalize Upload
        """

    @abstractmethod
    def next_upload_chunk(self, st: TransferState) -> Optional[int]:
        """
        Next Upload Chunk
        """

    @abstractmethod
    def cleanup(self, st: TransferState) -> None:
        """
        Cleanup Artifacts
        """

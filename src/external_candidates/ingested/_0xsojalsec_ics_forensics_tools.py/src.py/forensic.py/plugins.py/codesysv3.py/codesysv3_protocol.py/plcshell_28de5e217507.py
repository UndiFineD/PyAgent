# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\plugins\CodeSysV3\codesysv3_protocol\plcshell.py
import logging

from .channel import CodeSysV3Channel
from .structures import *


class PLCShell:
    def __init__(self, channel: CodeSysV3Channel):
        self._channel = channel
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, command: str) -> str:
        if not self._channel.is_login:
            raise CodeSysProtocolV3Exception("Device is not connected")
        try:
            self.logger.info(
                f"Trying to run the shell command: {command} over the channel {self._channel.channel_id: 04X}"
            )

            self._channel.send(
                CmdGroup.PlcShell,
                0x01,
                Tag(0x11, self._channel.session_id.to_bytes(4, "little")),
                Tag(0x13, b"\x00" * 4),
                Tag(0x10, bytes(command, "ascii") + b"\x00" * 3, align=0x42),
            )
            resp, tags = self._channel.read()
            response_shell = str(tags[0x82][0x20].data, "utf-8")
            return response_shell
        except Exception as ex:
            self.logger.error(f"Failed to get the PLCShell response, error: {ex}")
        return ""

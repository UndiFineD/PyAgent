# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Web-Navigator\src\speech\__init__.py
import os
import wave
from tempfile import NamedTemporaryFile

import keyboard
from pyaudio import PyAudio, Stream, paInt16

from src.inference import BaseInference
from src.message import AIMessage


class Speech:
    def __init__(self, llm: BaseInference = None):
        self.chunk_size = 1024
        self.frame_rate = 44100
        self.channels = 1
        self.audio = PyAudio()
        self.stream = None
        self.llm = llm
        self.tempfile_path = ""

    def setup_stream(self):
        audio = self.audio
        self.stream = audio.open(
            **{
                "format": paInt16,
                "channels": self.channels,
                "rate": self.frame_rate,
                "input": True,
                "frames_per_buffer": self.chunk_size,
            }
        )

    def get_stream(self) -> Stream:
        if self.stream is None:
            self.setup_stream()
        return self.stream

    def record_audio(self) -> bytes:
        stream = self.get_stream()
        frames = []
        is_recording = True
        print("Recording audio...")
        print("Press enter to stop recording...")
        while is_recording:
            data = stream.read(self.chunk_size)
            frames.append(data)
            if keyboard.is_pressed("enter"):
                is_recording = False
        stream.stop_stream()
        print("Recording stopped...")
        return b"".join(frames)

    def bytes_to_tempfile(self, bytes: bytes):
        temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
        self.tempfile_path = temp_file.name
        temp_file.close()
        try:
            with wave.open(self.tempfile_path, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(paInt16))
                wf.setframerate(self.frame_rate)
                wf.writeframes(bytes)
        except Exception as e:
            raise Exception(f"Export failed. {e}")

    def close(self):
        if self.stream is not None:
            self.stream.close()
        if self.audio is not None:
            self.audio.terminate()
        self.stream = None
        self.audio = None
        os.remove(self.tempfile_path)

    def invoke(self) -> AIMessage:
        audio_bytes = self.record_audio()
        self.bytes_to_tempfile(audio_bytes)
        print(f"Using {self.llm.model} audio to text...")
        response = self.llm.invoke(file_path=self.tempfile_path)
        self.close()
        return response

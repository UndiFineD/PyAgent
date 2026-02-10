#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Tests to ensure basic type hints exist for LMStudio TTS stubs."""

from typing import get_type_hints

from importlib import import_module
import torch

lm_tts = import_module("src.infrastructure.compute.backend.llm_backends.lmstudio.tts")


def test_my_lm_plugin_forward_annotation():
    hints = get_type_hints(lm_tts.MyLMPlugin.forward)
    assert "x" in hints, "forward should have annotation for parameter 'x'"
    assert "return" in hints, "forward should have a return annotation"
    # Expect a torch.Tensor return type
    assert hints["return"] == torch.Tensor, f"Expected return type torch.Tensor, got {hints['return']}"


def test_speak_returns_str():
    hints = get_type_hints(lm_tts.speak)
    assert hints.get("return") == str, "speak() should be annotated to return str"

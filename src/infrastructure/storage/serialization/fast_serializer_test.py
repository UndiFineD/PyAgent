#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from infrastructure.storage.serialization.fast_serializer import SerializationFormat, SerializerStats, Serializer, JSONSerializer, PickleSerializer, MsgPackSerializer, CBORSerializer, BinarySerializer, SerializerRegistry, get_serializer_registry, fast_serialize, fast_deserialize, to_json, from_json, to_msgpack, from_msgpack


def test_serializationformat_basic():
    assert SerializationFormat is not None


def test_serializerstats_basic():
    assert SerializerStats is not None


def test_serializer_basic():
    assert Serializer is not None


def test_jsonserializer_basic():
    assert JSONSerializer is not None


def test_pickleserializer_basic():
    assert PickleSerializer is not None


def test_msgpackserializer_basic():
    assert MsgPackSerializer is not None


def test_cborserializer_basic():
    assert CBORSerializer is not None


def test_binaryserializer_basic():
    assert BinarySerializer is not None


def test_serializerregistry_basic():
    assert SerializerRegistry is not None


def test_get_serializer_registry_basic():
    assert callable(get_serializer_registry)


def test_fast_serialize_basic():
    assert callable(fast_serialize)


def test_fast_deserialize_basic():
    assert callable(fast_deserialize)


def test_to_json_basic():
    assert callable(to_json)


def test_from_json_basic():
    assert callable(from_json)


def test_to_msgpack_basic():
    assert callable(to_msgpack)


def test_from_msgpack_basic():
    assert callable(from_msgpack)

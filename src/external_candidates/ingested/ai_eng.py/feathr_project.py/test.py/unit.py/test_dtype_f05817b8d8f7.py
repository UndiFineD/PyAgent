# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\test\unit\test_dtype.py
import pytest
from feathr import INT32, Feature, TypedKey, ValueType


def test_key_type():
    key = TypedKey(key_column="key", key_column_type=ValueType.INT32)
    assert key.key_column_type == ValueType.INT32

    with pytest.raises(KeyError):
        key = TypedKey(key_column="key", key_column_type=INT32)


def test_feature_type():
    key = TypedKey(key_column="key", key_column_type=ValueType.INT32)

    feature = Feature(name="name", key=key, feature_type=INT32)

    assert feature.feature_type == INT32

    with pytest.raises(KeyError):
        feature = Feature(name="name", key=key, feature_type=ValueType.INT32)

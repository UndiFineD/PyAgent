# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\tests\deps\test_s3.py
import json

import pytest
from acontext_core.infra.s3 import S3Client

FAKE_KEY = "a" * 32


@pytest.mark.asyncio
async def test_s3():
    S3_CLIENT = S3Client()
    await S3_CLIENT.upload_object(
        "foo/ok.json",
        json.dumps({"a": 1}).encode("utf-8"),
        content_type="application/json",  # Use proper MIME type
    )

    assert (await S3_CLIENT.get_object_metadata("foo/ok.json")) is not None

    payload = await S3_CLIENT.download_object("foo/ok.json")
    _data = json.loads(payload.decode("utf-8"))
    assert _data == {"a": 1}
    await S3_CLIENT.get_object_metadata("foo/ok.json")

    await S3_CLIENT.delete_object("foo/ok.json")
    assert (await S3_CLIENT.get_object_metadata("foo/ok.json")) is None

    # await S3_CLIENT.delete_object("foo/ok.json")
    print("Upload successful!")

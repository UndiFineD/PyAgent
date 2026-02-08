# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_labelllm.py\backend.py\app.py\client.py\minio_213e9f0c440c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LabelLLM\backend\app\client\minio.py

from app.core.config import settings

from minio import Minio


class MinioClient:
    def __init__(self, ak: str, sk: str, endpoint: str, internal_endpoint: str, bucket: str):
        self.client = Minio(internal_endpoint, access_key=ak, secret_key=sk, secure=False)

        self.bucket = bucket

        self.endpoint = endpoint

        self.internal_endpoint = internal_endpoint


minio = MinioClient(
    settings.MINIO_ACCESS_KEY_ID,
    settings.MINIO_ACCESS_KEY_SECRET,
    settings.MINIO_ENDPOINT,
    settings.MINIO_INTERNAL_ENDPOINT,
    settings.MINIO_BUCKET,
)

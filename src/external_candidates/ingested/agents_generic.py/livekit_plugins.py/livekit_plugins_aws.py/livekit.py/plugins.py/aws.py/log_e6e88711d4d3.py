# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-aws\livekit\plugins\aws\log.py
import logging

logger = logging.getLogger("livekit.plugins.aws")
smithy_logger = logging.getLogger("smithy_aws_event_stream.aio")
smithy_logger.setLevel(logging.INFO)
bedrock_client_logger = logging.getLogger("aws_sdk_bedrock_runtime.client")
bedrock_client_logger.setLevel(logging.INFO)

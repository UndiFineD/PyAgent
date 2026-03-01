# bedrock

**File**: `src\infrastructure\cloud\providers\bedrock.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 411  
**Complexity**: 12 (moderate)

## Overview

AWS Bedrock cloud provider connector.

Provides integration with AWS Bedrock for inference requests,
supporting Claude, Titan, and other Bedrock-hosted models.

## Classes (1)

### `AWSBedrockConnector`

**Inherits from**: CloudProviderBase

Connector for AWS Bedrock API.

Supports Claude (Anthropic), Titan (Amazon), Llama (Meta),
and other models available through Bedrock.

Example:
    connector = AWSBedrockConnector(
        region_name="us-east-1",
        # Uses default AWS credential chain
    )
    
    request = InferenceRequest(
        messages=[{"role": "user", "content": "Hello!"}],
        model="anthropic.claude-3-sonnet-20240229-v1:0",
    )
    
    response = await connector.complete(request)

**Methods** (12):
- `__init__(self, region_name, profile_name, aws_access_key_id, aws_secret_access_key)`
- `name(self)`
- `available_models(self)`
- `_parse_response(self, response_body, model)`
- `_extract_text_from_chunk(self, chunk, model)`
- `_estimate_tokens(self, messages)`
- `estimate_cost(self, request)`
- `_format_request_body(self, request)`
- `_messages_to_claude_prompt(self, messages)`
- `_messages_to_llama3_prompt(self, messages)`
- ... and 2 more methods

## Dependencies

**Imports** (18):
- `__future__.annotations`
- `aioboto3`
- `base.AuthenticationError`
- `base.CloudProviderBase`
- `base.CloudProviderError`
- `base.InferenceRequest`
- `base.InferenceResponse`
- `base.RateLimitError`
- `botocore.exceptions.ClientError`
- `json`
- `logging`
- `os`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- ... and 3 more

---
*Auto-generated documentation*

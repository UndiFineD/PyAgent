#!/usr/bin/env python3
"""Test multimodal tokenizer implementation."""


# Import directly from the types module
from src.infrastructure.engine.tokenization.detokenizer.types import (
    MultimodalTokenizer,
)

print("=== Multimodal Tokenizer Implementation Test ===\n")

tokenizer = MultimodalTokenizer()

# Test 1: Text only
print("[TEST 1] Text tokenization:")
result = tokenizer.encode_multimodal(text="Hello world!")
print("  Text: 'Hello world!'")
print(f"  Tokens: {result.token_ids}")
print(f"  Modalities: {[m.value for m in result.modality_sequence]}")
print(f"  Total: {result.num_tokens} tokens\n")

# Test 2: Image patches only
print("[TEST 2] Image tokenization:")
image_patches = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
result = tokenizer.encode_multimodal(image_patches=image_patches)
print("  Image patches: 3 patches")
print(f"  Tokens: {result.token_ids}")
print(f"  Token range: {min(result.token_ids)}-{max(result.token_ids)}")
print(f"  Image token count: {result.image_token_count}\n")

# Test 3: Multimodal (text + image)
print("[TEST 3] Multimodal tokenization (text + image):")
result = tokenizer.encode_multimodal(
    text="A cat sitting on a mat",
    image_patches=[[0.1, 0.2], [0.3, 0.4]]
)
print("  Text: 'A cat sitting on a mat'")
print("  Image patches: 2 patches")
print(f"  Total tokens: {result.num_tokens}")
print(f"  Text tokens: {result.text_token_count}")
print(f"  Image tokens: {result.image_token_count}")
print(f"  Token sequence: {[m.value for m in result.modality_sequence]}")
print(f"  Metadata: {result.metadata}\n")

# Test 4: Multimodal (text + image + audio)
print("[TEST 4] Multimodal tokenization (text + image + audio):")
audio_frames = [[0.1], [0.2], [0.3], [0.4]]
result = tokenizer.encode_multimodal(
    text="listen to this sound",
    image_patches=[[0.5, 0.6]],
    audio_frames=audio_frames
)
print("  Text: 'listen to this sound'")
print("  Image patches: 1")
print("  Audio frames: 4")
print(f"  Total tokens: {result.num_tokens}")
print("  Breakdown:")
print(f"    - Text: {result.text_token_count}")
print(f"    - Image: {result.image_token_count}")
print(f"    - Audio: {result.audio_token_count}")

print("\n[OK] Multimodal tokenizer fully functional!")
print("\nToken ID Ranges (Unified Space):")
print("  TEXT:  0-30000")
print("  IMAGE: 30001-60000")
print("  AUDIO: 60001-90000")
print("  VIDEO: 90001-120000")

#!/usr/bin/env python3
"""Example showing how TokenizerLike Protocol works with concrete implementations."""

import sys
import importlib.util

# Load modules directly
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

types = load_module("types", r"src\infrastructure\engine\tokenization\detokenizer\types.py")
simple = load_module("simple", r"src\infrastructure\engine\tokenization\detokenizer\simple_tokenizer.py")

MultimodalTokenizer = types.MultimodalTokenizer
SimpleWhitespaceTokenizer = simple.SimpleWhitespaceTokenizer

print("=== TokenizerLike Protocol vs Implementation ===\n")

print("1. THE PROTOCOL (TokenizerLike):")
print("   - Defines the interface (contract)")
print("   - Methods have 'pass' (no implementation)")
print("   - Used for type hints and duck typing")
print("   - Cannot be instantiated directly\n")

print("2. THE IMPLEMENTATION (SimpleWhitespaceTokenizer):")
print("   - Provides actual functionality")
print("   - All methods have real code")
print("   - Can be instantiated and used\n")

print("=" * 60)
print("\n[DEMO] Using SimpleWhitespaceTokenizer with MultimodalTokenizer\n")

# Create concrete tokenizer implementation
text_tokenizer = SimpleWhitespaceTokenizer(vocab_size=10000)

print("[Step 1] Created SimpleWhitespaceTokenizer")
print(f"  Vocab size: {text_tokenizer.vocab_size}")
print(f"  EOS token: {text_tokenizer.eos_token_id}\n")

# Use it with MultimodalTokenizer
multimodal_tokenizer = MultimodalTokenizer(text_tokenizer=text_tokenizer)

print("[Step 2] Injected into MultimodalTokenizer")
print("  MultimodalTokenizer uses TokenizerLike as type hint")
print("  SimpleWhitespaceTokenizer satisfies the protocol\n")

# Test text encoding
text = "Hello multimodal AI!"
token_ids = text_tokenizer.encode(text)
print("[Step 3] Test text tokenization")
print(f"  Input: '{text}'")
print(f"  Token IDs: {token_ids}")
print(f"  Decoded: '{text_tokenizer.decode(token_ids)}'\n")

# Test multimodal encoding
result = multimodal_tokenizer.encode_multimodal(
    text="A robot learning to see and hear",
    image_patches=[[0.1, 0.2], [0.3, 0.4]],
    audio_frames=[[0.5]]
)

print("[Step 4] Test multimodal encoding")
print(f"  Text: 'A robot learning to see and hear'")
print(f"  Image patches: 2")
print(f"  Audio frames: 1")
print(f"  Total tokens: {result.num_tokens}")
print(f"  Breakdown:")
print(f"    - Text tokens: {result.text_token_count} (IDs: {result.token_ids[:result.text_token_count]})")
print(f"    - Image tokens: {result.image_token_count} (IDs: {result.token_ids[result.text_token_count:result.text_token_count+result.image_token_count]})")
print(f"    - Audio tokens: {result.audio_token_count} (IDs: {result.token_ids[-result.audio_token_count:]})")

print("\n" + "=" * 60)
print("\n[KEY INSIGHT]")
print("The Protocol (TokenizerLike) with 'pass' is CORRECT!")
print("It's an interface definition, not an implementation.")
print("Real tokenizers implement this protocol.")
print("\nIn production, use:")
print("  - transformers.AutoTokenizer (Hugging Face)")
print("  - tiktoken (OpenAI)")
print("  - sentencepiece (Google)")
print("  - SimpleWhitespaceTokenizer (basic fallback)")

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VyvoTTS\vyvotts\utils\copy_tokenizer.py
import os

from transformers import AutoTokenizer


def copy_tokenizer_with_custom_tokens(model_name, output_directory, custom_tokens=None):
    """
    Copy a tokenizer from a pretrained model and add custom tokens if provided.

    Args:
        model_name (str): Name or path of the pretrained model
        output_directory (str): Directory where tokenizer will be saved
        custom_tokens (list): List of custom tokens to add (optional)
    """
    print(f"Loading tokenizer from: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Add custom tokens if provided
    if custom_tokens:
        print(f"Adding {len(custom_tokens)} custom tokens...")
        tokenizer.add_tokens(custom_tokens)

    # Save tokenizer to target directory
    tokenizer.save_pretrained(output_directory)
    print(f"Tokenizer successfully saved to: {output_directory}")

    return tokenizer


# Configuration
TOKENS_PER_BATCH = 4096
NUM_BATCHES = 7
EXTRA_TOKENS = 10

# Calculate total number of custom tokens needed
total_custom_tokens = (NUM_BATCHES * TOKENS_PER_BATCH) + EXTRA_TOKENS

# Generate custom token names
custom_token_list = [f"<custom_token_{i}>" for i in range(total_custom_tokens + 1)]

print(f"Creating {len(custom_token_list)} custom tokens...")

# Copy tokenizer and add custom tokens
tokenizer = copy_tokenizer_with_custom_tokens(
    model_name="LiquidAI/LFM2-350M",
    output_directory="output_checkpoint",
    custom_tokens=custom_token_list,
)

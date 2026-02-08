# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VyvoTTS\vyvotts\inference\transformers_hqq_inference.py
import time
from typing import Any, Dict, List, Optional, Tuple

import torch
import yaml
from hqq.core.quantize import BaseQuantizeConfig
from hqq.models.hf.base import AutoHQQHFModel
from hqq.utils.generation_hf import patch_model_for_compiled_runtime
from hqq.utils.patching import prepare_for_inference
from snac import SNAC
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


# Load configuration
config = load_config("vyvotts/configs/inference/lfm2.yaml")
TOKENIZER_LENGTH = config["TOKENIZER_LENGTH"]
START_OF_TEXT = config["START_OF_TEXT"]
END_OF_TEXT = config["END_OF_TEXT"]
START_OF_SPEECH = config["START_OF_SPEECH"]
END_OF_SPEECH = config["END_OF_SPEECH"]
START_OF_HUMAN = config["START_OF_HUMAN"]
END_OF_HUMAN = config["END_OF_HUMAN"]
START_OF_AI = config["START_OF_AI"]
END_OF_AI = config["END_OF_AI"]
PAD_TOKEN = config["PAD_TOKEN"]
AUDIO_TOKENS_START = config["AUDIO_TOKENS_START"]

# Model configuration
model_name = "Vyvo/VyvoTTS-LFM2-Neuvillette"
device = "cuda:0"
compute_dtype = torch.float16


def initialize_models():
    """Initialize SNAC model, language model, and tokenizer with HQQ optimization."""
    # Initialize SNAC model
    snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz")
    snac_model = snac_model.to(device)

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Initialize and optimize language model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=compute_dtype,
        # attn_implementation="kernels-community/flash-attn3:flash_attention",
        device_map=device,
        # quantization_config=HqqConfig(nbits=4, group_size=64),
    )

    model.config.use_cache = True
    model.generation_config.cache_implementation = "static"

    # Apply HQQ quantization
    AutoHQQHFModel.quantize_model(
        model,
        quant_config=BaseQuantizeConfig(nbits=4, group_size=64, axis=1),
        compute_dtype=compute_dtype,
        device=device,
    )

    # Prepare for optimized inference
    prepare_for_inference(model, backend="gemlite")
    patch_model_for_compiled_runtime(
        model,
        tokenizer,
        warmup=False,
        max_new_tokens=1000,
        patch_accelerate=True,
        pre_compile=None,
    )

    return snac_model, model, tokenizer


def preprocess_prompts(
    prompts: List[str],
    tokenizer,
    chosen_voice: Optional[str] = None,
    device: str = "cuda",
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Preprocess prompts by tokenizing, adding special tokens, and padding."""
    if chosen_voice:
        prompts = [f"{chosen_voice}: " + p for p in prompts]

    all_input_ids = []
    for prompt in prompts:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        all_input_ids.append(input_ids)

    start_token = torch.tensor([[START_OF_HUMAN]], dtype=torch.int64)
    end_tokens = torch.tensor([[END_OF_TEXT, END_OF_HUMAN]], dtype=torch.int64)

    all_modified_input_ids = []
    for input_ids in all_input_ids:
        modified_input_ids = torch.cat([start_token, input_ids, end_tokens], dim=1)  # SOH SOT Text EOT EOH
        all_modified_input_ids.append(modified_input_ids)

    all_padded_tensors = []
    all_attention_masks = []
    max_length = max([modified_input_ids.shape[1] for modified_input_ids in all_modified_input_ids])

    for modified_input_ids in all_modified_input_ids:
        padding = max_length - modified_input_ids.shape[1]
        padded_tensor = torch.cat(
            [
                torch.full((1, padding), PAD_TOKEN, dtype=torch.int64),
                modified_input_ids,
            ],
            dim=1,
        )
        attention_mask = torch.cat(
            [
                torch.zeros((1, padding), dtype=torch.int64),
                torch.ones((1, modified_input_ids.shape[1]), dtype=torch.int64),
            ],
            dim=1,
        )
        all_padded_tensors.append(padded_tensor)
        all_attention_masks.append(attention_mask)

    all_padded_tensors = torch.cat(all_padded_tensors, dim=0)
    all_attention_masks = torch.cat(all_attention_masks, dim=0)

    input_ids = all_padded_tensors.to(device)
    attention_mask = all_attention_masks.to(device)

    return input_ids, attention_mask


def generate_text(
    model,
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    do_sample: bool = True,
    max_new_tokens: int = 1200,
    temperature: float = 0.6,
    top_p: float = 0.95,
    repetition_penalty: float = 1.1,
) -> Tuple[torch.Tensor, float]:
    """Generate text using the language model."""
    torch.cuda.synchronize()
    start_time = time.time()

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            cache_implementation="static",
            do_sample=do_sample,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            num_return_sequences=1,
            eos_token_id=END_OF_SPEECH,
        )

    torch.cuda.synchronize()
    generation_time = time.time() - start_time

    return generated_ids, generation_time


def redistribute_codes(code_list: List[int], snac_model) -> torch.Tensor:
    """Redistribute codes into layers and decode to audio."""
    layer_1 = []
    layer_2 = []
    layer_3 = []
    for i in range((len(code_list) + 1) // 7):
        layer_1.append(code_list[7 * i])
        layer_2.append(code_list[7 * i + 1] - 4096)
        layer_3.append(code_list[7 * i + 2] - (2 * 4096))
        layer_3.append(code_list[7 * i + 3] - (3 * 4096))
        layer_2.append(code_list[7 * i + 4] - (4 * 4096))
        layer_3.append(code_list[7 * i + 5] - (5 * 4096))
        layer_3.append(code_list[7 * i + 6] - (6 * 4096))

    codes = [
        torch.tensor(layer_1).unsqueeze(0),
        torch.tensor(layer_2).unsqueeze(0),
        torch.tensor(layer_3).unsqueeze(0),
    ]

    codes = [c.to(device) for c in codes]
    audio_hat = snac_model.decode(codes)
    return audio_hat


def parse_output_to_audio(generated_ids: torch.Tensor, snac_model) -> Tuple[List[torch.Tensor], float]:
    """Parse generated token IDs and convert to audio samples."""
    torch.cuda.synchronize()
    start_time = time.time()

    token_to_find = AUDIO_TOKENS_START
    token_to_remove = END_OF_SPEECH

    token_indices = (generated_ids == token_to_find).nonzero(as_tuple=True)

    if len(token_indices[1]) > 0:
        last_occurrence_idx = token_indices[1][-1].item()
        cropped_tensor = generated_ids[:, last_occurrence_idx + 1 :]
    else:
        cropped_tensor = generated_ids

    processed_rows = []
    for row in cropped_tensor:
        masked_row = row[row != token_to_remove]
        processed_rows.append(masked_row)

    code_lists = []
    for row in processed_rows:
        row_length = row.size(0)
        new_length = (row_length // 7) * 7
        trimmed_row = row[:new_length]
        trimmed_row = [t - AUDIO_TOKENS_START for t in trimmed_row]
        code_lists.append(trimmed_row)

    my_samples = []
    for code_list in code_lists:
        samples = redistribute_codes(code_list, snac_model)
        my_samples.append(samples)

    torch.cuda.synchronize()
    audio_processing_time = time.time() - start_time

    return my_samples, audio_processing_time


def process_single_prompt(
    prompt: str, snac_model, model, tokenizer, chosen_voice: Optional[str] = None
) -> Tuple[torch.Tensor, Dict[str, float]]:
    """Process a single prompt and return audio with timing information."""
    torch.cuda.synchronize()
    total_start_time = time.time()

    # Preprocessing
    torch.cuda.synchronize()
    preprocess_start = time.time()
    input_ids, attention_mask = preprocess_prompts([prompt], tokenizer, chosen_voice, device)
    torch.cuda.synchronize()
    preprocess_time = time.time() - preprocess_start

    # Text generation
    generated_ids, generation_time = generate_text(model, input_ids, attention_mask)

    # Audio processing
    audio_samples, audio_processing_time = parse_output_to_audio(generated_ids, snac_model)

    torch.cuda.synchronize()
    total_time = time.time() - total_start_time

    timing_info = {
        "preprocessing_time": preprocess_time,
        "generation_time": generation_time,
        "audio_processing_time": audio_processing_time,
        "total_time": total_time,
    }

    return audio_samples[0] if audio_samples else None, timing_info


def text_to_speech(text: str, voice: Optional[str] = None) -> torch.Tensor:
    """Generate speech from text using HQQ-optimized model.

    Args:
        text: Input text to convert to speech
        voice: Optional voice identifier

    Returns:
        Audio tensor containing the generated speech
    """
    snac_model, model, tokenizer = initialize_models()
    audio_sample, _ = process_single_prompt(text, snac_model, model, tokenizer, voice)
    return audio_sample

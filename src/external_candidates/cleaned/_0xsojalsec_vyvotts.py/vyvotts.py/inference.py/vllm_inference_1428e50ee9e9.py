# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VyvoTTS\vyvotts\inference\vllm_inference.py
from typing import Any, Dict, List, Optional

import torch
import yaml
from snac import SNAC
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


class VyvoTTSInference:
    """High-performance TTS inference engine using vLLM backend."""

    CODES_PER_GROUP = 7

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        config_path: Optional[str] = None,
        model_name: str = "Vyvo/VyvoTTS-LFM2-Neuvillette",
        snac_model_name: str = "hubertsiuzdak/snac_24khz",
    ):
        """Initialize the TTS inference engine.

        Args:
            config: Configuration dictionary containing token constants
            config_path: Path to YAML config file (alternative to config dict)
            model_name: HuggingFace model identifier for the TTS model
            snac_model_name: HuggingFace model identifier for SNAC audio decoder
        """
        # Load configuration
        if config is not None:
            self.config = config
        elif config_path is not None:
            self.config = load_config(config_path)
        else:
            # Default config path
            self.config = load_config("vyvotts/configs/inference/lfm2.yaml")

        # Set token constants from config
        self.TOKENIZER_LENGTH = self.config["TOKENIZER_LENGTH"]
        self.START_OF_TEXT = self.config["START_OF_TEXT"]
        self.END_OF_TEXT = self.config["END_OF_TEXT"]
        self.START_OF_SPEECH = self.config["START_OF_SPEECH"]
        self.END_OF_SPEECH = self.config["END_OF_SPEECH"]
        self.START_OF_HUMAN = self.config["START_OF_HUMAN"]
        self.END_OF_HUMAN = self.config["END_OF_HUMAN"]
        self.START_OF_AI = self.config["START_OF_AI"]
        self.END_OF_AI = self.config["END_OF_AI"]
        self.PAD_TOKEN = self.config["PAD_TOKEN"]
        self.AUDIO_TOKENS_START = self.config["AUDIO_TOKENS_START"]

        # For compatibility with existing code
        self.AUDIO_MARKER_TOKEN = self.AUDIO_TOKENS_START
        self.STOP_TOKEN_ID = self.END_OF_SPEECH
        self.AUDIO_OFFSET = self.AUDIO_TOKENS_START
        self.model_name = model_name
        self.engine = LLM(model=model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.snac_model = SNAC.from_pretrained(snac_model_name)

    def _extract_audio_tokens(self, generated_ids: torch.Tensor) -> torch.Tensor:
        """Extract audio tokens from generated sequence."""
        token_indices = (generated_ids == self.AUDIO_MARKER_TOKEN).nonzero(as_tuple=True)

        if len(token_indices[1]) > 0:
            last_occurrence_idx = token_indices[1][-1].item()
            return generated_ids[:, last_occurrence_idx + 1 :]
        return generated_ids

    def _clean_tokens(self, tokens: torch.Tensor) -> List[torch.Tensor]:
        """Remove stop tokens and prepare for processing."""
        return [row[row != self.STOP_TOKEN_ID] for row in tokens]

    def _group_and_offset_codes(self, processed_rows: List[torch.Tensor]) -> List[List[int]]:
        """Group tokens into groups of 7 and apply offset correction."""
        code_lists = []

        for row in processed_rows:
            row_length = row.size(0)
            new_length = (row_length // self.CODES_PER_GROUP) * self.CODES_PER_GROUP
            trimmed_row = row[:new_length]
            code_lists.append([t.item() - self.AUDIO_OFFSET for t in trimmed_row])

        return code_lists

    def _redistribute_codes(self, code_list: List[int]) -> torch.Tensor:
        """Redistribute codes into SNAC layers and decode to audio."""
        num_groups = len(code_list) // self.CODES_PER_GROUP

        layer_1, layer_2, layer_3 = [], [], []

        for i in range(num_groups):
            base_idx = self.CODES_PER_GROUP * i

            layer_1.append(code_list[base_idx])
            layer_2.extend([code_list[base_idx + 1] - 4096, code_list[base_idx + 4] - (4 * 4096)])
            layer_3.extend(
                [
                    code_list[base_idx + 2] - (2 * 4096),
                    code_list[base_idx + 3] - (3 * 4096),
                    code_list[base_idx + 5] - (5 * 4096),
                    code_list[base_idx + 6] - (6 * 4096),
                ]
            )

        codes = [
            torch.tensor(layer_1).unsqueeze(0),
            torch.tensor(layer_2).unsqueeze(0),
            torch.tensor(layer_3).unsqueeze(0),
        ]

        return self.snac_model.decode(codes)

    def parse_tokens_to_audio(self, generated_ids: torch.Tensor) -> List[torch.Tensor]:
        """Convert generated token IDs to audio waveforms.

        Args:
            generated_ids: Raw token IDs from model generation

        Returns:
            List of decoded audio tensors
        """
        # Extract audio portion of tokens
        cropped_tokens = self._extract_audio_tokens(generated_ids)

        # Clean and prepare tokens
        processed_rows = self._clean_tokens(cropped_tokens)

        # Group and apply offsets
        code_lists = self._group_and_offset_codes(processed_rows)

        # Decode to audio
        return [self._redistribute_codes(code_list) for code_list in code_lists]

    def generate(self, text: str, voice: Optional[str] = None) -> torch.Tensor:
        """Generate speech from text input.

        Args:
            text: Input text to convert to speech
            voice: Optional voice identifier

        Returns:
            Audio tensor containing the generated speech
        """
        # Construct the prompt with optional voice prefix
        if voice:
            adapted_prompt = f"{voice}: {text}"
            prompt_tokens = self.tokenizer(adapted_prompt, return_tensors="pt")
        else:
            prompt_tokens = self.tokenizer(text, return_tensors="pt")

        # Insert special tokens
        start_token = torch.tensor([[self.START_OF_HUMAN]], dtype=torch.int64)
        end_tokens = torch.tensor([[self.END_OF_TEXT, self.END_OF_HUMAN]], dtype=torch.int64)
        all_input_ids = torch.cat([start_token, prompt_tokens.input_ids, end_tokens], dim=1)

        # Decode to string for LLM
        final_prompt = self.tokenizer.decode(all_input_ids[0])

        # Sampling parameters
        params = SamplingParams(
            temperature=0.6,
            top_p=0.8,
            max_tokens=1200,
            stop_token_ids=[self.STOP_TOKEN_ID],
            repetition_penalty=1.3,
        )

        # Generate token IDs from the model
        outputs = self.engine.generate([final_prompt], [params])
        token_ids = outputs[0].outputs[0].token_ids
        generated_ids = torch.tensor([token_ids], dtype=torch.long)

        # Convert generated tokens into audio
        audio_samples = self.parse_tokens_to_audio(generated_ids)
        return audio_samples[0] if audio_samples else None


def text_to_speech(prompt, voice=None, config_path=None):
    """
    Given a text prompt and optional voice, generates audio tokens using
    the Vyvo TTS model and decodes them into audio samples via SNAC.
    """
    # Initialize TTS engine
    engine = VyvoTTSInference(config_path=config_path)

    # Generate audio
    audio_samples = engine.generate(prompt, voice)
    return audio_samples


# Example usage
if __name__ == "__main__":
    audio_output = text_to_speech("Hello world", voice="zoe")
    print("Decoded audio (tensors):", audio_output)

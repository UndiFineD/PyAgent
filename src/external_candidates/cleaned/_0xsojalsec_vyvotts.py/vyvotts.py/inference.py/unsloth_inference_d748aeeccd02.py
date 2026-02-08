# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VyvoTTS\vyvotts\inference\unsloth_inference.py
from pathlib import Path
from typing import Any, Dict, List, Optional

import soundfile as sf
import torch
import yaml
from snac import SNAC
from unsloth import FastLanguageModel


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


class VyvoTTSUnslothInference:
    """Memory-efficient TTS inference engine using Unsloth backend."""

    CODES_PER_GROUP = 7
    SAMPLE_RATE = 24000

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        config_path: Optional[str] = None,
        model_name: str = "Vyvo/VyvoTTS-v2-Neuvillette",
        snac_model_name: str = "hubertsiuzdak/snac_24khz",
        max_seq_length: int = 8192,
        load_in_4bit: bool = False,
        load_in_8bit: bool = False,
    ):
        """Initialize the TTS inference engine.

        Args:
            config: Configuration dictionary containing token constants
            config_path: Path to YAML config file (alternative to config dict)
            model_name: HuggingFace model identifier for the TTS model
            snac_model_name: HuggingFace model identifier for SNAC audio decoder
            max_seq_length: Maximum sequence length for the model
            load_in_4bit: Whether to load model in 4-bit precision
            load_in_8bit: Whether to load model in 8-bit precision
        """
        # Load configuration
        if config is not None:
            self.config = config
        elif config_path is not None:
            self.config = load_config(config_path)
        else:
            # Default config path
            default_config_path = "vyvotts/configs/inference/lfm2.yaml"
            self.config = load_config(default_config_path)

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
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            dtype=None,  # Auto detection
            load_in_4bit=load_in_4bit,
            load_in_8bit=load_in_8bit,
        )

        # Enable fast inference
        FastLanguageModel.for_inference(self.model)

        # Initialize SNAC model on CPU to save GPU memory
        self.snac_model = SNAC.from_pretrained(snac_model_name)
        self.snac_model.to("cpu")

    def _prepare_prompt(self, text: str, voice: Optional[str] = None) -> torch.Tensor:
        """Prepare input prompt with special tokens."""
        # Add voice prefix if specified
        prompt_text = f"{voice}: {text}" if voice else text

        # Tokenize
        input_ids = self.tokenizer(prompt_text, return_tensors="pt").input_ids

        # Add special tokens
        start_token = torch.tensor([[self.START_OF_HUMAN]], dtype=torch.int64)
        end_tokens = torch.tensor([[self.END_OF_TEXT, self.END_OF_HUMAN]], dtype=torch.int64)

        # Combine tokens
        modified_input_ids = torch.cat([start_token, input_ids, end_tokens], dim=1)

        return modified_input_ids.to("cuda")

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

    def _parse_tokens_to_audio(self, generated_ids: torch.Tensor) -> List[torch.Tensor]:
        """Parse generated token IDs and convert to audio samples."""
        # Find start of speech tokens
        token_indices = (generated_ids == self.START_OF_SPEECH).nonzero(as_tuple=True)

        if len(token_indices[1]) > 0:
            last_occurrence_idx = token_indices[1][-1].item()
            cropped_tensor = generated_ids[:, last_occurrence_idx + 1 :]
        else:
            cropped_tensor = generated_ids

        # Remove end of speech tokens
        processed_rows = [row[row != self.END_OF_SPEECH] for row in cropped_tensor]

        # Group tokens and apply offset
        audio_samples = []
        for row in processed_rows:
            row_length = row.size(0)
            new_length = (row_length // self.CODES_PER_GROUP) * self.CODES_PER_GROUP
            trimmed_row = row[:new_length]
            code_list = [t.item() - self.AUDIO_TOKENS_START for t in trimmed_row]

            if code_list:  # Only process if we have codes
                audio = self._redistribute_codes(code_list)
                audio_samples.append(audio)

        return audio_samples

    def generate(
        self,
        text: str,
        voice: Optional[str] = None,
        max_new_tokens: int = 1200,
        temperature: float = 0.6,
        top_p: float = 0.95,
        repetition_penalty: float = 1.1,
        do_sample: bool = True,
    ) -> torch.Tensor:
        """Generate speech from text input.

        Args:
            text: Input text to convert to speech
            voice: Optional voice identifier for voice cloning
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            repetition_penalty: Penalty for token repetition
            do_sample: Whether to use sampling

        Returns:
            Audio tensor containing the generated speech
        """
        # Prepare input
        input_ids = self._prepare_prompt(text, voice)
        attention_mask = torch.ones_like(input_ids)

        # Generate tokens
        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                num_return_sequences=1,
                eos_token_id=self.END_OF_SPEECH,
                use_cache=True,
            )

        # Convert to audio
        audio_samples = self._parse_tokens_to_audio(generated_ids)
        return audio_samples[0] if audio_samples else None

    def save_audio(
        self,
        audio_tensor: torch.Tensor,
        output_path: str | Path,
        sample_rate: int = None,
    ) -> None:
        """Save audio tensor to file.

        Args:
            audio_tensor: Audio tensor to save
            output_path: Path to save the audio file
            sample_rate: Sample rate for the audio (defaults to class default)
        """
        if audio_tensor is None:
            raise ValueError("No audio tensor provided")

        sample_rate = sample_rate or self.SAMPLE_RATE
        output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to numpy and save
        audio_numpy = audio_tensor.detach().squeeze().cpu().numpy()
        sf.write(output_path, audio_numpy, sample_rate)


# Convenience function for backward compatibility
def text_to_speech(text: str, voice: Optional[str] = None, output_path: Optional[str] = None, **kwargs) -> torch.Tensor:
    """Generate speech from text using Unsloth model.

    Args:
        text: Input text to convert to speech
        voice: Optional voice identifier
        output_path: Optional path to save audio file
        **kwargs: Additional generation parameters

    Returns:
        Audio tensor containing the generated speech
    """
    engine = VyvoTTSUnslothInference()
    audio = engine.generate(text, voice, **kwargs)

    if output_path and audio is not None:
        engine.save_audio(audio, output_path)

    return audio


if __name__ == "__main__":
    # Example usage
    engine = VyvoTTSUnslothInference(load_in_4bit=True)

    test_text = "Hey there my name is Elise, and I'm a speech generation model that can sound like a person."
    audio = engine.generate(test_text)

    if audio is not None:
        engine.save_audio(audio, "output.wav")
        print(f"Audio saved with shape: {audio.shape}")
    else:
        print("Failed to generate audio")

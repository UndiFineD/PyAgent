# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\stream_omni.py\eval.py\run_stream_omni_44d1a4dd6465.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\eval\run_stream_omni.py

import argparse

import hashlib

import os

import re

import sys

import time

from io import BytesIO

from typing import List, Optional

import requests

import torch

import torchaudio

from PIL import Image

from stream_omni.constants import (
    DEFAULT_IM_END_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IMAGE_TOKEN,
    IMAGE_TOKEN_INDEX,
)

from stream_omni.conversation import SeparatorStyle, conv_templates

from stream_omni.mm_utils import (
    get_model_name_from_path,
    process_images,
    tokenizer_image_token,
)

from stream_omni.model.builder import load_pretrained_model

from stream_omni.utils import disable_torch_init

sys.path.append("./CosyVoice")

from cosyvoice.cli.cosyvoice import CosyVoice


class CosyVoiceModel:
    """Handles speech-to-token and token-to-speech conversion using CosyVoice."""

    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = device

        self.cosyvoice = CosyVoice(model_path)

        del self.cosyvoice.model.llm

    def generate_speech_token(self, tensor: torch.Tensor) -> str:
        """Generate a speech token string from a tensor of audio tokens."""

        if len(tensor.shape) > 1:
            tensor = tensor.view(-1)

        return "".join(f"<Audio_{num.item()}>" for num in tensor)

    def extract_speech_token(self, input_string: str) -> List[int]:
        """Extract a list of speech tokens from a string."""

        numbers = re.findall(r"<Audio_(\d+)>", input_string)

        return list(map(int, numbers))

    def speech_to_token(self, audio_file: str) -> str:
        """Convert speech from an audio file into speech tokens."""

        speech, sample_rate = torchaudio.load(audio_file)

        speech_16k = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(speech)

        speech_token, _ = self.cosyvoice.frontend._extract_speech_token(speech_16k)

        return self.generate_speech_token(speech_token)

    def speech_to_token_wo_file(self, speech: torch.Tensor, sample_rate: int) -> str:
        """Convert speech tensor into speech tokens."""

        speech_16k = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(speech)

        speech_token, _ = self.cosyvoice.frontend._extract_speech_token(speech_16k)

        return self.generate_speech_token(speech_token)

    def token_to_speech(self, tokens: str) -> torch.Tensor:
        """Convert speech tokens back into audio."""

        tts_speech_token = torch.tensor(self.extract_speech_token(tokens)).long().unsqueeze(0).to(self.device)

        embedding = self.cosyvoice.frontend.get_spk_embedding("英文女").to(self.device)

        flow_prompt_speech_token = torch.zeros(1, 0, dtype=torch.int32)

        flow_prompt_speech_token_len = torch.zeros(1, dtype=torch.int32)

        prompt_speech_feat = torch.zeros(1, 0, 80)

        prompt_speech_feat_len = torch.zeros(1, dtype=torch.int32)

        tts_mel, _ = self.cosyvoice.model.flow.inference(
            token=tts_speech_token,
            token_len=torch.tensor([tts_speech_token.size(1)], dtype=torch.int32).to(self.device),
            prompt_token=flow_prompt_speech_token.to(self.device),
            prompt_token_len=flow_prompt_speech_token_len.to(self.device),
            prompt_feat=prompt_speech_feat.to(self.device),
            prompt_feat_len=prompt_speech_feat_len.to(self.device),
            embedding=embedding.to(self.device),
            flow_cache=torch.zeros(1, 80, 0, 2).to(self.device),
        )

        tts_speech, _ = self.cosyvoice.model.hift.inference(speech_feat=tts_mel)

        return tts_speech


def generate_output_path() -> str:
    """Generate a unique output path based on current timestamp."""

    timestamp = str(time.time()).encode("utf-8")

    hash_object = hashlib.md5(timestamp)

    return f"./output_{hash_object.hexdigest()}.wav"


def image_parser(image_file: str, sep: str) -> List[str]:
    """Parse image file paths from a string."""

    return image_file.split(sep) if image_file else []


def load_image(image_file: str) -> Image.Image:
    """Load an image from a file path or URL."""

    try:
        if image_file.startswith(("http", "https")):
            response = requests.get(image_file)

            response.raise_for_status()

            return Image.open(BytesIO(response.content)).convert("RGB")

        return Image.open(image_file).convert("RGB")

    except Exception as e:
        print(f"Error loading image {image_file}: {str(e)}")

        raise


def load_images(image_files: List[str]) -> List[Image.Image]:
    """Load multiple images from file paths or URLs."""

    return [load_image(image_file) for image_file in image_files]


def determine_conv_mode(model_name: str, args_conv_mode: Optional[str]) -> str:
    """Determine the conversation mode based on model name."""

    if "llama-2" in model_name.lower():
        conv_mode = "llava_llama_2"

    elif "mistral" in model_name.lower():
        conv_mode = "mistral_instruct"

    elif "v1.6-34b" in model_name.lower():
        conv_mode = "chatml_direct"

    elif "v1" in model_name.lower():
        conv_mode = "llava_v1"

    elif "mpt" in model_name.lower():
        conv_mode = "mpt"

    else:
        conv_mode = "llava_v0"

    if args_conv_mode and conv_mode != args_conv_mode:
        print(f"Inferred conv mode: {conv_mode}, but using {args_conv_mode} from args")

        return args_conv_mode

    return conv_mode


# Initialize CosyVoice model

"""

# download CosyVoice-300M-25Hz checkpoint

from modelscope import snapshot_download

snapshot_download('iic/CosyVoice-300M-25Hz', local_dir='./CosyVoice-300M-25Hz')

"""

cosyvoice = CosyVoiceModel("./CosyVoice-300M-25Hz")


def eval_model(args):
    """Evaluate the model with given arguments."""

    disable_torch_init()

    # Load model and tokenizer

    model_name = args.model_name

    tokenizer, model, image_processor, context_len = load_pretrained_model(
        args.model_path, args.model_base, model_name, load_8bit=args.load_8bit
    )

    # Process query (audio file or text)

    query = cosyvoice.speech_to_token(args.query) if os.path.isfile(args.query) else args.query

    # Add image token if applicable

    if args.image_file:
        image_token_se = f"{DEFAULT_IM_START_TOKEN}{DEFAULT_IMAGE_TOKEN}{DEFAULT_IM_END_TOKEN}"

        query = f"{image_token_se}\n{query}" if model.config.mm_use_im_start_end else f"{DEFAULT_IMAGE_TOKEN}\n{query}"

    # Determine conversation mode

    conv_mode = determine_conv_mode(model_name, args.conv_mode)

    conv = conv_templates[conv_mode].copy()

    conv.append_message(conv.roles[0], query)

    conv.append_message(conv.roles[1], None)

    prompt = conv.get_prompt()

    # Process images if provided

    images_tensor, image_sizes = None, None

    if args.image_file:
        image_files = image_parser(args.image_file, args.sep)

        images = load_images(image_files)

        image_sizes = [x.size for x in images]

        images_tensor = process_images(images, image_processor, model.config).to(model.device, dtype=torch.float16)

    # Tokenize input

    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).cuda()

    # Prepare prefill audio IDs

    conv = conv_templates[conv_mode].copy()

    conv.append_message(conv.roles[0], " ")

    conv.append_message(conv.roles[1], None)

    prefill_audio_ids = tokenizer(conv.get_prompt(), return_tensors="pt").input_ids.cuda()

    # Generate output

    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=images_tensor,
            image_sizes=image_sizes,
            do_sample=args.temperature > 0,
            temperature=args.temperature,
            top_p=args.top_p,
            num_beams=args.num_beams,
            max_new_tokens=args.max_new_tokens,
            use_cache=True,
            inference_type="speech_to_speech",
        )

    # Process ASR output

    ctc_asr_ids = model.asr_ids[0, 43:-3]

    asr_ids = []

    prev_token = -1

    for token in ctc_asr_ids.tolist():
        if token != 128002 and token != prev_token:
            asr_ids.append(token)

        prev_token = token

    asr_ids = torch.tensor(asr_ids).long().unsqueeze(0).type_as(input_ids)

    asr_outputs = tokenizer.batch_decode(asr_ids, skip_special_tokens=True)[0].strip()

    # Decode LLM and speech token outputs

    llm_outputs = tokenizer.batch_decode(torch.cat(model.llm_ids, dim=-1), skip_special_tokens=True)[0].strip()

    outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()

    # Convert tokens to speech and save

    tts_speech = cosyvoice.token_to_speech(outputs)

    output_path = generate_output_path()

    torchaudio.save(output_path, tts_speech.cpu(), 22050)

    try:
        from rich.console import Console

        from rich.text import Text

        # Initialize rich console for colored output

        console = Console()

        # Print outputs with rich formatting

        console.print(Text("ASR Outputs:", style="bold cyan"))

        console.print(Text(asr_outputs, style="white"))

        console.print(Text("LLM Outputs:", style="bold magenta"))

        console.print(Text(llm_outputs, style="white"))

        console.print(Text("Speech Tokens:", style="bold green"))

        console.print(Text(outputs, style="white"))

        console.print(Text("Speech Outputs:", style="bold blue"))

        console.print(Text(f"Audio saved at {output_path}", style="white"))

    except:
        # Fallback to standard print statements

        print("ASR Outputs:")

        print(asr_outputs)

        print("\nLLM Outputs:")

        print(llm_outputs)

        print("\nSpeech Tokens:")

        print(outputs)

        print("\nSpeech Outputs:")

        print(f"Speech response saved at {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a multimodal model with speech and image inputs.")

    parser.add_argument("--model-path", type=str, default="facebook/opt-350m", help="Path to the model")

    parser.add_argument("--model-base", type=str, default=None, help="Base model path")

    parser.add_argument("--model-name", type=str, default="llava.llama.audio", help="Name of the model")

    parser.add_argument("--image-file", type=str, default=None, help="Path or URL to image file(s)")

    parser.add_argument("--query", type=str, required=True, help="Input query (text or audio file)")

    parser.add_argument("--conv-mode", type=str, default=None, help="Conversation mode")

    parser.add_argument("--sep", type=str, default=",", help="Separator for multiple image files")

    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")

    parser.add_argument("--top_p", type=float, default=None, help="Top-p sampling probability")

    parser.add_argument("--num_beams", type=int, default=1, help="Number of beams for beam search")

    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=4096,
        help="Maximum new tokens to generate",
    )

    parser.add_argument(
        "--load-8bit",
        action="store_true",
        help="Whether to load the model in 8-bit mode",
    )

    args = parser.parse_args()

    eval_model(args)

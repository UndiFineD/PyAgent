# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\eval\vision_speech_to_speech\model_sqa_loader_llama.py
import argparse
import json
import math
import os
import re
import sys

import shortuuid
import torch
import torchaudio
from datasets import Dataset as HF_Dataset
from datasets import load_from_disk
from jiwer import wer
from llava.constants import (
    DEFAULT_IM_END_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IMAGE_TOKEN,
    IMAGE_TOKEN_INDEX,
)
from PIL import Image
from stream_omni.conversation import SeparatorStyle, conv_templates
from stream_omni.mm_utils import (
    get_model_name_from_path,
    process_images,
    tokenizer_image_token,
)
from stream_omni.model.builder import load_pretrained_model
from stream_omni.utils import disable_torch_init
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

sys.path.append("./CosyVoice")
import os
import re

import torch
import tqdm
from cosyvoice.cli.cosyvoice import CosyVoice
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class ASRModel:
    def __init__(self, model_path: str, device: str = None, torch_dtype=torch.float16):
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.torch_dtype = (
            torch_dtype
            if torch_dtype
            else (torch.float16 if torch.cuda.is_available() else torch.float32)
        )

        # Load the model
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        ).to(self.device)

        # Load the processor
        self.processor = AutoProcessor.from_pretrained(model_path)

        # Set up the pipeline
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def asr_from_file(self, file_path: str):
        """Performs ASR from an audio file."""
        result = self.pipe(file_path)
        return result["text"]

    def asr(self, speech, sample_rate=22050):
        """Performs ASR from an audio file."""
        if speech.shape[0] > 1:
            speech = torch.mean(speech, dim=0, keepdim=False)

        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=16000
            )
            speech = resampler(speech)

        if len(speech.shape) > 1:
            speech = speech.squeeze()

        result = self.pipe(speech.numpy())

        return result["text"]


class CosyVoiceModel:
    def __init__(self, model_path, device="cuda"):
        self.device = device
        self.cosyvoice = CosyVoice(model_path)
        del self.cosyvoice.model.llm

    def generate_speech_token(self, tensor):
        """Generate a speech token string from a tensor of audio tokens."""
        if len(tensor.shape) > 1:
            tensor = tensor.view(-1)
        audio_strings = [f"<Audio_{num.item()}>" for num in tensor]
        return "".join(audio_strings)

    def extract_speech_token(self, input_string):
        """Extract a list of speech tokens from a string."""
        numbers = re.findall(r"<Audio_(\d+)>", input_string)
        return list(map(int, numbers))

    def speech_to_token(self, audio_file):
        """Convert speech from an audio file into speech tokens."""
        speech, sample_rate = torchaudio.load(audio_file)
        speech_16k = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=16000
        )(speech)
        speech_token, _ = self.cosyvoice.frontend._extract_speech_token(speech_16k)
        return self.generate_speech_token(speech_token)

    def speech_to_token_wo_file(self, speech, sample_rate):
        """Convert speech from an audio file into speech tokens."""
        # speech, sample_rate = torchaudio.load(audio_file)
        speech_16k = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=16000
        )(speech)
        speech_token, _ = self.cosyvoice.frontend._extract_speech_token(speech_16k)
        return self.generate_speech_token(speech_token)

    def token_to_speech(self, tokens):
        """Convert speech tokens back into audio."""
        tts_speech_token = (
            torch.tensor(self.extract_speech_token(tokens))
            .long()
            .unsqueeze(0)
            .to(self.device)
        )
        embedding = self.cosyvoice.frontend.get_spk_embedding("英文女").to(self.device)
        flow_prompt_speech_token = torch.zeros(1, 0, dtype=torch.int32)
        flow_prompt_speech_token_len = torch.zeros(1, dtype=torch.int32)
        prompt_speech_feat = torch.zeros(1, 0, 80)
        prompt_speech_feat_len = torch.zeros(1, dtype=torch.int32)

        tts_mel, _ = self.cosyvoice.model.flow.inference(
            token=tts_speech_token,
            token_len=torch.tensor([tts_speech_token.size(1)], dtype=torch.int32).to(
                self.device
            ),
            prompt_token=flow_prompt_speech_token.to(self.device),
            prompt_token_len=flow_prompt_speech_token_len.to(self.device),
            prompt_feat=prompt_speech_feat.to(self.device),
            prompt_feat_len=prompt_speech_feat_len.to(self.device),
            embedding=embedding.to(self.device),
            flow_cache=torch.zeros(1, 80, 0, 2).to(self.device),
        )
        tts_speech, _ = self.cosyvoice.model.hift.inference(speech_feat=tts_mel)
        return tts_speech


# Initialize CosyVoice model
"""
# download CosyVoice-300M-25Hz checkpoint
from modelscope import snapshot_download
snapshot_download('iic/CosyVoice-300M-25Hz', local_dir='./CosyVoice-300M-25Hz')
"""
cosyvoice = CosyVoiceModel("./CosyVoice-300M-25Hz")
asr_model = ASRModel("openai/whisper-large-v3")


def get_chunk(dataset: Dataset, num_chunks: int, chunk_idx: int) -> Dataset:
    total_length = len(dataset)
    chunk_size = math.ceil(total_length / num_chunks)
    start = chunk_idx * chunk_size
    end = min(start + chunk_size, total_length)
    return dataset.select(range(start, end))


# Custom dataset class
class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, model_config):
        self.data = data
        self.tokenizer = tokenizer
        self.model_config = model_config

    def __getitem__(self, index):
        item = self.data[index]
        qs = item["QuestionText"]
        conv = conv_templates[args.conv_mode].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)

        prompt = conv.get_prompt()

        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids[0]

        return input_ids

    def __len__(self):
        return len(self.data)


def collate_fn(batch):
    input_ids = torch.stack(batch, dim=0)
    return input_ids


# DataLoader
def create_data_loader(
    data, tokenizer, image_processor, model_config, batch_size=1, num_workers=1
):
    assert batch_size == 1, "batch_size must be 1"
    dataset = CustomDataset(data, tokenizer, model_config)
    data_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=False,
        collate_fn=collate_fn,
    )
    return data_loader


def eval_model(args):
    # Model
    disable_torch_init()
    model_path = os.path.expanduser(args.model_path)
    model_name = args.model_name
    tokenizer, model, image_processor, context_len = load_pretrained_model(
        model_path, args.model_base, model_name
    )
    tokenizer.model_max_length = 2048
    model.config.tokenizer_model_max_length = 2048
    questions = load_from_disk(args.data)

    questions = get_chunk(questions, args.num_chunks, args.chunk_idx)
    answers_file = os.path.expanduser(args.answers_file)
    os.makedirs(os.path.dirname(answers_file), exist_ok=True)
    ans_file = open(answers_file, "w")

    if (
        "plain" in model_name
        and "finetune" not in model_name.lower()
        and "mmtag" not in args.conv_mode
    ):
        args.conv_mode = args.conv_mode + "_mmtag"
        print(
            f"It seems that this is a plain model, but it is not using a mmtag prompt, auto switching to {args.conv_mode}."
        )

    data_loader = create_data_loader(
        questions, tokenizer, image_processor, model.config
    )

    for input_ids, line in tqdm.tqdm(zip(data_loader, questions), total=len(questions)):
        idx = line["Wav Filename"]
        cur_prompt = line["QuestionText"]
        speech = line["audio"]["array"]
        sample_rate = line["audio"]["sampling_rate"]

        speech = torch.tensor(speech, dtype=torch.float32).unsqueeze(0)

        speech_token = cosyvoice.speech_to_token_wo_file(speech, sample_rate)

        conv = conv_templates[args.conv_mode].copy()
        conv.append_message(conv.roles[0], speech_token)
        conv.append_message(conv.roles[1], None)

        prompt = conv.get_prompt()
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

        with torch.inference_mode():
            model.reset()
            output_ids = model.generate(
                input_ids,
                do_sample=True if args.temperature > 0 else False,
                temperature=args.temperature,
                top_p=args.top_p,
                num_beams=args.num_beams,
                max_new_tokens=args.max_new_tokens,
                use_cache=True,
                inference_type="speech_to_speech",
            )

        outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[
            0
        ].strip()
        tts_speech = cosyvoice.token_to_speech(outputs)
        whisper_asr = asr_model.asr(tts_speech.cpu())
        whisper_asr = whisper_asr.strip()
        print(whisper_asr)
        ans_id = shortuuid.uuid()
        ans_file.write(
            json.dumps(
                {
                    "question_id": idx,
                    "prompt": cur_prompt,
                    "output": whisper_asr,
                    "answer": line["Answer"],
                    "speech_token": speech_token,
                    "answer_id": ans_id,
                    "model_id": model_name,
                    "metadata": {},
                },
                ensure_ascii=True,
            )
            + "\n"
        )
    ans_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="facebook/opt-350m")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--model-name", type=str, default="llava")
    parser.add_argument("--data", type=str, default="tables/question.jsonl")
    parser.add_argument("--answers-file", type=str, default="answer.jsonl")
    parser.add_argument("--conv-mode", type=str, default="llava_v1")
    parser.add_argument("--num-chunks", type=int, default=1)
    parser.add_argument("--chunk-idx", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top_p", type=float, default=None)
    parser.add_argument("--num_beams", type=int, default=1)
    parser.add_argument("--max_new_tokens", type=int, default=1024)
    args = parser.parse_args()

    eval_model(args)

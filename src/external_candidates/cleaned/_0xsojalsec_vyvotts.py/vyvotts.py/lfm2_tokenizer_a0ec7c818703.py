# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VyvoTTS\vyvotts\lfm2_tokenizer.py
import torch
import torchaudio.transforms as T
from datasets import load_dataset
from snac import SNAC

dataset = load_dataset("hf/dataset-path", split="train")

ds_sample_rate = dataset[0]["audio"]["sampling_rate"]

tokeniser_length = 64400
start_of_text = 1
end_of_text = 7

start_of_speech = tokeniser_length + 1
end_of_speech = tokeniser_length + 2

start_of_human = tokeniser_length + 3
end_of_human = tokeniser_length + 4

start_of_ai = tokeniser_length + 5
end_of_ai = tokeniser_length + 6
pad_token = tokeniser_length + 7

audio_tokens_start = tokeniser_length + 10

snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz")
snac_model = snac_model.to("cuda")


def tokenise_audio(waveform):
    waveform = torch.from_numpy(waveform).unsqueeze(0)
    waveform = waveform.to(dtype=torch.float32)
    resample_transform = T.Resample(orig_freq=ds_sample_rate, new_freq=24000)
    waveform = resample_transform(waveform)

    waveform = waveform.unsqueeze(0).to("cuda")

    # generate the codes from snac
    with torch.inference_mode():
        codes = snac_model.encode(waveform)

    all_codes = []
    for i in range(codes[0].shape[1]):
        all_codes.append(codes[0][0][i].item() + audio_tokens_start)
        all_codes.append(codes[1][0][2 * i].item() + audio_tokens_start + 4096)
        all_codes.append(codes[2][0][4 * i].item() + audio_tokens_start + (2 * 4096))
        all_codes.append(codes[2][0][(4 * i) + 1].item() + audio_tokens_start + (3 * 4096))
        all_codes.append(codes[1][0][(2 * i) + 1].item() + audio_tokens_start + (4 * 4096))
        all_codes.append(codes[2][0][(4 * i) + 2].item() + audio_tokens_start + (5 * 4096))
        all_codes.append(codes[2][0][(4 * i) + 3].item() + audio_tokens_start + (6 * 4096))

    return all_codes


def add_codes(example):
    # Always initialize codes_list to None
    codes_list = None

    try:
        answer_audio = example.get("audio")
        # If there's a valid audio array, tokenise it
        if answer_audio and "array" in answer_audio:
            audio_array = answer_audio["array"]
            codes_list = tokenise_audio(audio_array)
    except Exception as e:
        print(f"Skipping row due to error: {e}")
        # Keep codes_list as None if we fail
    example["codes_list"] = codes_list

    return example


dataset = dataset.map(add_codes, remove_columns=["audio"])
dataset = dataset.filter(lambda x: x["codes_list"] is not None)
dataset = dataset.filter(lambda x: len(x["codes_list"]) > 0)


def remove_duplicate_frames(example):
    vals = example["codes_list"]
    if len(vals) % 7 != 0:
        raise ValueError("Input list length must be divisible by 7")

    result = vals[:7]

    removed_frames = 0

    for i in range(7, len(vals), 7):
        current_first = vals[i]
        previous_first = result[-7]

        if current_first != previous_first:
            result.extend(vals[i : i + 7])
        else:
            removed_frames += 1

    example["codes_list"] = result

    return example


dataset = dataset.map(remove_duplicate_frames)

tok_info = """*** HERE you can modify the text prompt
If you are training a multi-speaker model (e.g., canopylabs/orpheus-3b-0.1-ft),
ensure that the dataset includes a "source" field and format the input accordingly:
- Single-speaker: f"{example['text']}"
- Multi-speaker: f"{example['source']}: {example['text']}"
"""
print(tok_info)


def create_input_ids(example):
    # Determine whether to include the source field
    text_prompt = f"{example['source']}: {example['text']}" if "source" in example else example["text"]

    text_ids = tokenizer.encode(text_prompt, add_special_tokens=True)
    text_ids.append(end_of_text)

    example["text_tokens"] = text_ids
    input_ids = (
        [start_of_human]
        + example["text_tokens"]
        + [end_of_human]
        + [start_of_ai]
        + [start_of_speech]
        + example["codes_list"]
        + [end_of_speech]
        + [end_of_ai]
    )
    example["input_ids"] = input_ids
    example["labels"] = input_ids
    example["attention_mask"] = [1] * len(input_ids)

    return example


dataset = dataset.map(create_input_ids, remove_columns=["text", "codes_list"])
columns_to_keep = ["input_ids", "labels", "attention_mask"]
columns_to_remove = [col for col in dataset.column_names if col not in columns_to_keep]

dataset = dataset.remove_columns(columns_to_remove)

dataset.push_to_hub("your-username/your-dataset")

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\stream_omni.py\scripts.py\archived.py\merge_lora_weights_797cadee8e97.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\scripts\archived\merge_lora_weights.py

import argparse

from llava.mm_utils import get_model_name_from_path

from llava.model.builder import load_pretrained_model

def merge_lora(args):

    model_name = get_model_name_from_path(args.model_path)

    tokenizer, model, image_processor, context_len = load_pretrained_model(

        args.model_path, args.model_base, model_name, device_map="cpu"

    )

    model.save_pretrained(args.save_model_path)

    tokenizer.save_pretrained(args.save_model_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--model-path", type=str, required=True)

    parser.add_argument("--model-base", type=str, required=True)

    parser.add_argument("--save-model-path", type=str, required=True)

    args = parser.parse_args()

    merge_lora(args)


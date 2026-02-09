#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\serve\model_worker.py
"""
A model worker executes the model.
"""

import argparse
import asyncio
import json
import threading
import time
import uuid
from functools import partial
from threading import Thread

import requests
import torch
import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import StreamingResponse
from stream_omni.constants import (
    DEFAULT_IM_END_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IMAGE_TOKEN,
    IMAGE_TOKEN_INDEX,
    WORKER_HEART_BEAT_INTERVAL,
)
from stream_omni.conversation import SeparatorStyle, conv_templates
from stream_omni.mm_utils import (
    KeywordsStoppingCriteria,
    load_image_from_base64,
    process_images,
    tokenizer_image_token,
)
from stream_omni.model.builder import load_pretrained_model
from stream_omni.utils import build_logger, pretty_print_semaphore, server_error_msg
from transformers import TextIteratorStreamer

GB = 1 << 30

worker_id = str(uuid.uuid4())[:6]
logger = build_logger("model_worker", f"model_worker_{worker_id}.log")
global_counter = 0

model_semaphore = None


from queue import Queue
from typing import Optional

import numpy as np
from transformers import AutoTokenizer


class AudioIteratorStreamer(TextIteratorStreamer):
    """
    Streamer that stores audio-ready data in a queue, to be used by a downstream application as an iterator.
    This is useful for applications that benefit from accessing the generated audio data in a non-blocking way
    (e.g., in an interactive audio demo).

    Parameters:
        tokenizer (`AutoTokenizer`):
            The tokenizer used to decode the tokens.
        skip_prompt (`bool`, *optional*, defaults to `False`):
            Whether to skip the prompt to `.generate()` or not. Useful for applications like speech generation.
        timeout (`float`, *optional*):
            The timeout for the audio queue. If `None`, the queue will block indefinitely. Useful to handle exceptions
            in `.generate()` when it is called in a separate thread.
        decode_kwargs (`dict`, *optional*):
            Additional keyword arguments to pass to the tokenizer's `decode` method.
    """

    def __init__(
        self,
        tokenizer: "AutoTokenizer",
        skip_prompt: bool = False,
        timeout: Optional[float] = None,
        **decode_kwargs,
    ):
        super().__init__(tokenizer, skip_prompt, **decode_kwargs)

    def put(self, value):
        """
        Receives tokens, decodes them, and prints them to stdout as soon as they form entire words.
        """
        if len(value.shape) > 1 and value.shape[0] > 1:
            raise ValueError("TextStreamer only supports batch size 1")
        elif len(value.shape) > 1:
            value = value[0]

        if self.skip_prompt and self.next_tokens_are_prompt:
            self.next_tokens_are_prompt = False
            return

        # Add the new token to the cache and decodes the entire thing.
        self.token_cache.extend(value.tolist())
        text = self.tokenizer.decode(self.token_cache, **self.decode_kwargs)

        # After the symbol for a new line, we flush the cache.
        if text.endswith("\n"):
            printable_text = text[self.print_len :]
            self.token_cache = []
            self.print_len = 0
        # If the last token is a CJK character, we print the characters.
        elif len(text) > 0 and self._is_chinese_char(ord(text[-1])):
            printable_text = text[self.print_len :]
            self.print_len += len(printable_text)
        # Otherwise, prints until the last space char (simple heuristic to avoid printing incomplete words,
        # which may change with the subsequent token -- there are probably smarter ways to do this!)
        else:
            printable_text = text[self.print_len : text.rfind(">") + 1]
            self.print_len += len(printable_text)

        self.on_finalized_text(printable_text)


def heart_beat_worker(controller):

    while True:
        time.sleep(WORKER_HEART_BEAT_INTERVAL)
        controller.send_heart_beat()


class ModelWorker:
    def __init__(
        self,
        controller_addr,
        worker_addr,
        worker_id,
        no_register,
        model_path,
        model_base,
        model_name,
        load_8bit,
        load_4bit,
    ):
        self.controller_addr = controller_addr
        self.worker_addr = worker_addr
        self.worker_id = worker_id
        if model_path.endswith("/"):
            model_path = model_path[:-1]
        if model_name is None:
            model_paths = model_path.split("/")
            if model_paths[-1].startswith("checkpoint-"):
                self.model_name = model_paths[-2] + "_" + model_paths[-1]
            else:
                self.model_name = model_paths[-1]
        else:
            self.model_name = model_name

        logger.info(f"Loading the model {self.model_name} on worker {worker_id} ...")
        self.tokenizer, self.model, self.image_processor, self.context_len = (
            load_pretrained_model(
                model_path, model_base, self.model_name, load_8bit, load_4bit
            )
        )
        self.is_multimodal = (
            "llava" in self.model_name.lower() or "omni" in self.model_name.lower()
        )

        if not no_register:
            self.register_to_controller()
            self.heart_beat_thread = threading.Thread(
                target=heart_beat_worker, args=(self,)
            )
            self.heart_beat_thread.start()

    def register_to_controller(self):
        logger.info("Register to controller")

        url = self.controller_addr + "/register_worker"
        data = {
            "worker_name": self.worker_addr,
            "check_heart_beat": True,
            "worker_status": self.get_status(),
        }
        r = requests.post(url, json=data)
        assert r.status_code == 200

    def send_heart_beat(self):
        logger.info(
            f"Send heart beat. Models: {[self.model_name]}. "
            f"Semaphore: {pretty_print_semaphore(model_semaphore)}. "
            f"global_counter: {global_counter}"
        )

        url = self.controller_addr + "/receive_heart_beat"

        while True:
            try:
                ret = requests.post(
                    url,
                    json={
                        "worker_name": self.worker_addr,
                        "queue_length": self.get_queue_length(),
                    },
                    timeout=5,
                )
                exist = ret.json()["exist"]
                break
            except requests.exceptions.RequestException as e:
                logger.error(f"heart beat error: {e}")
            time.sleep(5)

        if not exist:
            self.register_to_controller()

    def get_queue_length(self):
        if model_semaphore is None:
            return 0
        else:
            return (
                args.limit_model_concurrency
                - model_semaphore._value
                + (
                    len(model_semaphore._waiters)
                    if model_semaphore._waiters is not None
                    else 0
                )
            )

    def get_status(self):
        return {
            "model_names": [self.model_name],
            "speed": 1,
            "queue_length": self.get_queue_length(),
        }

    @torch.inference_mode()
    def generate_stream(self, params):
        tokenizer, model, image_processor = (
            self.tokenizer,
            self.model,
            self.image_processor,
        )
        print("================", params["prompt"])
        prompt = params["prompt"]
        ori_prompt = prompt
        images = params.get("images", None)
        inference_type = params.get("inference_type", "speech_to_speech")
        num_image_tokens = 0
        model.reset()
        if images is not None and len(images) > 0 and self.is_multimodal:
            if len(images) > 0:
                if len(images) != prompt.count(DEFAULT_IMAGE_TOKEN):
                    raise ValueError(
                        "Number of images does not match number of <image> tokens in prompt"
                    )

                images = [load_image_from_base64(image) for image in images]
                image_sizes = [image.size for image in images]
                images = process_images(images, image_processor, model.config)

                if type(images) is list:
                    images = [
                        image.to(self.model.device, dtype=torch.float16)
                        for image in images
                    ]
                else:
                    images = images.to(self.model.device, dtype=torch.float16)

                replace_token = DEFAULT_IMAGE_TOKEN
                if getattr(self.model.config, "mm_use_im_start_end", False):
                    replace_token = (
                        DEFAULT_IM_START_TOKEN + replace_token + DEFAULT_IM_END_TOKEN
                    )
                prompt = prompt.replace(DEFAULT_IMAGE_TOKEN, replace_token)

                num_image_tokens = (
                    prompt.count(replace_token) * model.get_vision_tower().num_patches
                )
            else:
                images = None
                image_sizes = None
            image_args = {"images": images, "image_sizes": image_sizes}
        else:
            images = None
            image_args = {}
        print("111111111")
        temperature = float(params.get("temperature", 1.0))
        top_p = float(params.get("top_p", 1.0))
        max_context_length = getattr(model.config, "max_position_embeddings", 4096)
        max_new_tokens = min(int(params.get("max_new_tokens", 256)), 1024)
        stop_str = params.get("stop", None)
        do_sample = True if temperature > 0.001 else False
        print("22222222")
        input_ids = (
            tokenizer_image_token(
                prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt"
            )
            .unsqueeze(0)
            .cuda()
        )
        print("3333333")
        # keywords = [stop_str]
        # stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
        if inference_type in ["text_to_speech", "speech_to_speech"]:
            streamer = AudioIteratorStreamer(
                tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=100
            )
        else:
            streamer = TextIteratorStreamer(
                tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=100
            )
        print("444444")
        max_new_tokens = min(
            max_new_tokens, max_context_length - input_ids.shape[-1] - num_image_tokens
        )

        if max_new_tokens < 1:
            yield json.dumps(
                {
                    "text": ori_prompt
                    + "Exceeds max token length. Please start a new conversation, thanks.",
                    "error_code": 0,
                }
            ).encode() + b"\0"
            return

        conv = conv_templates["stream_omni_llama_3_1"].copy()
        conv.append_message(conv.roles[0], " ")
        conv.append_message(conv.roles[1], None)

        prefill_prompt = conv.get_prompt()
        prefill_audio_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()
        thread = Thread(
            target=model.generate,
            kwargs=dict(
                inputs=input_ids,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
                streamer=streamer,
                # stopping_criteria=[stopping_criteria],
                inference_type=inference_type,
                use_cache=True,
                prefill_audio_ids=(
                    prefill_audio_ids if inference_type == "text_to_speech" else None
                ),
                **image_args,
            ),
        )
        thread.start()

        print("+++++++++++")

        start_time = time.time()
        generated_text = ori_prompt
        for new_text in streamer:
            generated_text += new_text
            if generated_text.endswith(stop_str):
                generated_text = generated_text[: -len(stop_str)]
            # print("++++++++++++",new_text)
            try:
                if model.asr_ids is not None:
                    # Process ASR output
                    ctc_asr_ids = model.asr_ids[0, 43:-3]
                    asr_ids = []
                    prev_token = -1
                    for token in ctc_asr_ids.tolist():
                        if token != 128002 and token != prev_token:
                            asr_ids.append(token)
                        prev_token = token
                    asr_ids = (
                        torch.tensor(asr_ids).long().unsqueeze(0).type_as(input_ids)
                    )
                    asr_outputs = tokenizer.batch_decode(
                        asr_ids, skip_special_tokens=True
                    )[0].strip()
                else:
                    asr_outputs = ""

                if len(model.llm_ids) > 0:

                    # Decode LLM and speech token outputs
                    llm_outputs = tokenizer.batch_decode(
                        torch.cat(model.llm_ids, dim=-1), skip_special_tokens=True
                    )[0].strip()
                else:
                    llm_outputs = ""
            except:
                asr_outputs = ""
                llm_outputs = ""

            yield json.dumps(
                {
                    "text": generated_text,
                    "asr_outputs": asr_outputs,
                    "llm_outputs": llm_outputs,
                    "error_code": 0,
                }
            ).encode() + b"\0"

        end_time = time.time()

        new_generated = generated_text[len(ori_prompt) :]
        new_generated_tokens = tokenizer(new_generated).input_ids
        token_per_second = len(new_generated_tokens) / (end_time - start_time)
        print(f"token_per_second: {token_per_second}")

    def generate_stream_gate(self, params):
        try:
            for x in self.generate_stream(params):
                yield x
        except ValueError as e:
            print("Caught ValueError:", e)
            ret = {
                "text": server_error_msg,
                "error_code": 1,
            }
            yield json.dumps(ret).encode() + b"\0"
        except torch.cuda.CudaError as e:
            print("Caught torch.cuda.CudaError:", e)
            ret = {
                "text": server_error_msg,
                "error_code": 1,
            }
            yield json.dumps(ret).encode() + b"\0"
        except Exception as e:
            print("Caught Unknown Error", e)
            ret = {
                "text": server_error_msg,
                "error_code": 1,
            }
            yield json.dumps(ret).encode() + b"\0"


app = FastAPI()


def release_model_semaphore(fn=None):
    model_semaphore.release()
    if fn is not None:
        fn()


@app.post("/worker_generate_stream")
async def generate_stream(request: Request):
    global model_semaphore, global_counter
    global_counter += 1
    params = await request.json()

    if model_semaphore is None:
        model_semaphore = asyncio.Semaphore(args.limit_model_concurrency)
    await model_semaphore.acquire()
    worker.send_heart_beat()
    generator = worker.generate_stream_gate(params)
    background_tasks = BackgroundTasks()
    background_tasks.add_task(
        partial(release_model_semaphore, fn=worker.send_heart_beat)
    )
    return StreamingResponse(generator, background=background_tasks)


@app.post("/worker_get_status")
async def get_status(request: Request):
    return worker.get_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=21002)
    parser.add_argument("--worker-address", type=str, default="http://localhost:21002")
    parser.add_argument(
        "--controller-address", type=str, default="http://localhost:21001"
    )
    parser.add_argument("--model-path", type=str, default="facebook/opt-350m")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--model-name", type=str)
    parser.add_argument(
        "--multi-modal",
        action="store_true",
        help="Multimodal mode is automatically detected with model name, please make sure `llava` is included in the model path.",
    )
    parser.add_argument("--limit-model-concurrency", type=int, default=5)
    parser.add_argument("--stream-interval", type=int, default=1)
    parser.add_argument("--no-register", action="store_true")
    parser.add_argument("--load-8bit", action="store_true")
    parser.add_argument("--load-4bit", action="store_true")
    args = parser.parse_args()
    logger.info(f"args: {args}")

    if args.multi_modal:
        logger.warning(
            "Multimodal mode is automatically detected with model name, please make sure `llava` is included in the model path."
        )

    worker = ModelWorker(
        args.controller_address,
        args.worker_address,
        worker_id,
        args.no_register,
        args.model_path,
        args.model_base,
        args.model_name,
        args.load_8bit,
        args.load_4bit,
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

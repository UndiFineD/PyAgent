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

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\serve\gradio_web.py
import argparse
import datetime
import hashlib
import json
import os
import time

import gradio as gr
import requests
import torchaudio
from stream_omni.constants import LOGDIR
from stream_omni.conversation import (
    ChatItem,
    SeparatorStyle,
    conv_templates,
    default_conversation,
)
from stream_omni.utils import (
    build_logger,
    moderation_msg,
    server_error_msg,
    violates_moderation,
)


def speech_to_token_from_file(file_path):
    url = "http://localhost:21003/speech_to_token"  # The FastAPI endpoint
    headers = {
        "accept": "application/json",
    }
    # Open the file in binary mode and send it as part of the request
    with open(file_path, "rb") as file:
        files = {
            "file": (file.name, file, "audio/wav")
        }  # Name, file object, and file type
        response = requests.post(url, headers=headers, files=files)

    # Handle the response (assumed to be JSON based on the FastAPI code)
    if response.status_code == 200:
        return response.json()  # Returns the response in JSON format (contains tokens)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def token_to_speech_from_tokens(tokens):
    url = "http://localhost:21003/token_to_speech"  # The FastAPI endpoint
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    # Create the payload with the tokens
    data = {"tokens": tokens}

    # Send the POST request with the JSON data
    response = requests.post(url, headers=headers, json=data)

    # Handle the response
    if response.status_code == 200:
        # Assuming the response contains the path to the generated audio file
        return response.json()  # Contains the audio file path or URL
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


logger = build_logger("gradio_web_server", "gradio_web_server.log")

headers = {"User-Agent": "LLaVA Client"}

no_change_btn = gr.Button()
enable_btn = gr.Button(interactive=True)
disable_btn = gr.Button(interactive=False)

priority = {
    "vicuna-13b": "aaaaaaa",
    "koala-13b": "aaaaaab",
}


def get_conv_log_filename():
    t = datetime.datetime.now()
    name = os.path.join(LOGDIR, f"{t.year}-{t.month:02d}-{t.day:02d}-conv.json")
    return name


def get_model_list():
    ret = requests.post(args.controller_url + "/refresh_all_workers")
    assert ret.status_code == 200
    ret = requests.post(args.controller_url + "/list_models")
    models = ret.json()["models"]
    models.sort(key=lambda x: priority.get(x, x))
    logger.info(f"Models: {models}")
    return models


get_window_url_params = """
function() {
    const params = new URLSearchParams(window.location.search);
    url_params = Object.fromEntries(params);
    console.log(url_params);
    return url_params;
    }
"""


def load_demo(url_params, request: gr.Request):
    logger.info(f"load_demo. ip: {request.client.host}. params: {url_params}")

    dropdown_update = gr.Dropdown(visible=True)
    if "model" in url_params:
        model = url_params["model"]
        if model in models:
            dropdown_update = gr.Dropdown(value=model, visible=True)

    state = default_conversation.copy()

    state.multimodal_files = []
    return state, dropdown_update


def load_demo_refresh_model_list(request: gr.Request):
    logger.info(f"load_demo. ip: {request.client.host}")
    models = get_model_list()
    state = default_conversation.copy()
    dropdown_update = gr.Dropdown(
        choices=models, value=models[0] if len(models) > 0 else ""
    )
    return state, dropdown_update


def vote_last_response(state, vote_type, model_selector, request: gr.Request):
    with open(get_conv_log_filename(), "a") as fout:
        data = {
            "tstamp": round(time.time(), 4),
            "type": vote_type,
            "model": model_selector,
            "state": state.dict(),
            "ip": request.client.host,
        }
        fout.write(json.dumps(data) + "\n")


def upvote_last_response(state, model_selector, request: gr.Request):
    logger.info(f"upvote. ip: {request.client.host}")
    vote_last_response(state, "upvote", model_selector, request)
    return ("",) + (disable_btn,) * 3


def downvote_last_response(state, model_selector, request: gr.Request):
    logger.info(f"downvote. ip: {request.client.host}")
    vote_last_response(state, "downvote", model_selector, request)
    return ("",) + (disable_btn,) * 3


def flag_last_response(state, model_selector, request: gr.Request):
    logger.info(f"flag. ip: {request.client.host}")
    vote_last_response(state, "flag", model_selector, request)
    return ("",) + (disable_btn,) * 3


def regenerate(state, image_process_mode, request: gr.Request):
    logger.info(f"regenerate. ip: {request.client.host}")

    state.messages[-1][-1] = None
    prev_human_msg = state.messages[-2]
    if type(prev_human_msg[1]) in (tuple, list):
        prev_human_msg[1] = (*prev_human_msg[1][:2], image_process_mode)
    state.skip_next = False
    return (state, state.to_gradio_chatbot_from_chat(), "", None) + (disable_btn,) * 5


def clear_history(request: gr.Request):
    logger.info(f"clear_history. ip: {request.client.host}")
    state = default_conversation.copy()
    return (state, state.to_gradio_chatbot_from_chat(), "", None) + (disable_btn,) * 5


def is_audio_file(filename):
    if filename is None:
        return False
    audio_extensions = {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
        ".m4a",
        ".wma",
        ".alac",
    }
    return any(filename.lower().endswith(ext) for ext in audio_extensions)


def add(state, text, audio, image, image_process_mode, request: gr.Request):
    if is_audio_file(audio):
        return add_audio(state, audio, image, image_process_mode, request)
    return add_text(state, text, image, image_process_mode, request)


def add_text(state, text, image, image_process_mode, request: gr.Request):
    logger.info(f"add_text. ip: {request.client.host}. len: {len(text)}")
    if len(text) <= 0 and image is None:
        state.skip_next = True
        return (state, state.to_gradio_chatbot_from_chat(), "", None) + (
            no_change_btn,
        ) * 5
    if args.moderate:
        flagged = violates_moderation(text)
        if flagged:
            state.skip_next = True
            return (
                state,
                state.to_gradio_chatbot_from_chat(),
                moderation_msg,
                None,
            ) + (no_change_btn,) * 5

    _text = text
    text = text[:1536]  # Hard cut-off
    if image is not None:
        text = text[:1200]  # Hard cut-off for images
        if "<image>" not in text:
            # text = '<Image><image></Image>' + text
            # text = text + "\n<image>"
            text = "<image>\n" + text
        text = (text, image, image_process_mode)
        if len(state.get_images(return_pil=True)) > 0:
            state = default_conversation.copy()
    state.append_message(state.roles[0], text)
    state.append_message(state.roles[1], None)
    state.chatbot.append(
        ChatItem(msg=_text, image=image, image_process_mode=image_process_mode)
    )
    state.chatbot.append(ChatItem())

    state.skip_next = False
    return (state, state.to_gradio_chatbot_from_chat(), "", None) + (disable_btn,) * 5


def add_audio(state, audio, image, image_process_mode, request: gr.Request):

    speech, sample_rate = torchaudio.load(audio)
    audio_hash = hashlib.md5(speech.numpy().tobytes()).hexdigest()
    t = datetime.datetime.now()
    audio_file = os.path.join(
        LOGDIR,
        "serve_audios",
        f"{t.year}-{t.month:02d}-{t.day:02d}",
        f"{audio_hash}.wav",
    )
    if not os.path.isfile(audio_file):
        os.makedirs(os.path.dirname(audio_file), exist_ok=True)
        torchaudio.save(audio_file, speech, sample_rate)
    logger.info(f"add_audio. ip: {request.client.host}. {audio_file}")
    text = speech_to_token_from_file(audio)["tokens"]
    if len(text) <= 0 and image is None:
        state.skip_next = True
        return (state, state.to_gradio_chatbot_from_chat(), "", None) + (
            no_change_btn,
        ) * 5
    if args.moderate:
        flagged = violates_moderation(text)
        if flagged:
            state.skip_next = True
            return (
                state,
                state.to_gradio_chatbot_from_chat(),
                moderation_msg,
                None,
            ) + (no_change_btn,) * 5

    _text = text
    text = text[:1536]  # Hard cut-off
    if image is not None:
        text = text[:1200]  # Hard cut-off for images
        if "<image>" not in text:
            # text = '<Image><image></Image>' + text
            # text = text + "\n<image>"
            text = "<image>\n" + text
        if audio is not None:
            text = (text, image, image_process_mode, audio_file)
        else:
            text = (text, image, image_process_mode)
        if len(state.get_images(return_pil=True)) > 0:
            state = default_conversation.copy()

    state.append_message(state.roles[0], text)
    state.append_message(state.roles[1], None)
    state.chatbot.append(
        ChatItem(
            msg=_text,
            image=image,
            image_process_mode=image_process_mode,
            audio=audio_file if audio else None,
        )
    )
    state.chatbot.append(ChatItem())

    state.skip_next = False

    return (state, state.to_gradio_chatbot_from_chat(), "", None) + (disable_btn,) * 5


def http_bot(
    state,
    model_selector,
    temperature,
    top_p,
    max_new_tokens,
    request: gr.Request,
    template_name=None,
):
    logger.info(f"http_bot. ip: {request.client.host}")
    start_tstamp = time.time()
    model_name = model_selector

    if state.skip_next:
        # This generate call is skipped due to invalid inputs
        yield (state, state.to_gradio_chatbot_from_chat()) + (no_change_btn,) * 5
        return

    if len(state.messages) == state.offset + 2:
        # First round of conversation
        if "llava" in model_name.lower():
            if "llama-2" in model_name.lower():
                template_name = "llava_llama_2"
            elif "mistral" in model_name.lower() or "mixtral" in model_name.lower():
                if "orca" in model_name.lower():
                    template_name = "mistral_orca"
                elif "hermes" in model_name.lower():
                    template_name = "mistral_direct"
                else:
                    template_name = "mistral_instruct"
            elif "zephyr" in model_name.lower():
                template_name = "mistral_zephyr"
            elif "hermes" in model_name.lower():
                template_name = "mistral_direct"
            elif "v1" in model_name.lower():
                if "mmtag" in model_name.lower():
                    template_name = "llava_v1_mmtag"
                elif (
                    "plain" in model_name.lower()
                    and "finetune" not in model_name.lower()
                ):
                    template_name = "llava_v1_mmtag"
                else:
                    template_name = "llava_v1"
            elif "mpt" in model_name.lower():
                template_name = "mpt"
            else:
                if "mmtag" in model_name.lower():
                    template_name = "v0_plain"
                elif (
                    "plain" in model_name.lower()
                    and "finetune" not in model_name.lower()
                ):
                    template_name = "v0_plain"
                else:
                    template_name = "llava_v0"
        elif "mistral" in model_name.lower() or "mixtral" in model_name.lower():
            if "orca" in model_name.lower():
                template_name = "mistral_orca"
            elif "hermes" in model_name.lower():
                template_name = "mistral_direct"
            else:
                template_name = "mistral_instruct"
        elif "hermes" in model_name.lower():
            template_name = "mistral_direct"
        elif "zephyr" in model_name.lower():
            template_name = "mistral_zephyr"
        elif "mpt" in model_name:
            template_name = "mpt_text"
        elif "llama-2" in model_name:
            template_name = "llama_2"
        else:
            template_name = "vicuna_v1"

        template_name = "stream_omni_llama_3_1"
        new_state = conv_templates[template_name].copy()
        new_state.append_message(new_state.roles[0], state.messages[-2][1])
        new_state.append_message(new_state.roles[1], None)

        new_state.chatbot = []
        new_state.chatbot.append(state.chatbot[-2])
        new_state.chatbot.append(ChatItem())

        state = new_state

    # Query worker address
    controller_url = args.controller_url
    ret = requests.post(
        controller_url + "/get_worker_address", json={"model": model_name}
    )
    worker_addr = ret.json()["address"]
    logger.info(f"model_name: {model_name}, worker_addr: {worker_addr}")

    # No available worker
    if worker_addr == "":
        state.messages[-1][-1] = server_error_msg
        state.chatbot[-1].msg = server_error_msg
        yield (
            state,
            state.to_gradio_chatbot_from_chat(),
            disable_btn,
            disable_btn,
            disable_btn,
            enable_btn,
            enable_btn,
        )
        return

    # Construct prompt
    prompt = state.get_prompt()

    all_images = state.get_images(return_pil=True)
    all_image_hash = [hashlib.md5(image.tobytes()).hexdigest() for image in all_images]
    for image, hash in zip(all_images, all_image_hash):
        t = datetime.datetime.now()
        filename = os.path.join(
            LOGDIR, "serve_images", f"{t.year}-{t.month:02d}-{t.day:02d}", f"{hash}.jpg"
        )
        if not os.path.isfile(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            image.save(filename)
    stop = state.sep2
    if state.sep_style in [SeparatorStyle.SINGLE, SeparatorStyle.MPT]:
        stop = state.sep
    if state.sep_style in [SeparatorStyle.LLAMA_3_1]:
        stop = state.stop_str

    if "<Audio_" in prompt:
        inference_type = "speech_to_speech"
    else:
        inference_type = "text_to_text"
    # Make requests
    pload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": float(temperature),
        "top_p": float(top_p),
        "max_new_tokens": min(int(max_new_tokens), 1536),
        "stop": stop,
        "inference_type": inference_type,
        "images": f"List of {len(state.get_images())} images: {all_image_hash}",
    }
    logger.info(f"==== request ====\n{pload}")

    pload["images"] = state.get_images()

    state.messages[-1][-1] = "▌"
    state.chatbot[-1].msg = "▌"
    yield (state, state.to_gradio_chatbot_from_chat()) + (disable_btn,) * 5

    try:
        # Stream output
        response = requests.post(
            worker_addr + "/worker_generate_stream",
            headers=headers,
            json=pload,
            stream=True,
            timeout=100,
        )
        last_print_time = time.time()
        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if chunk:
                data = json.loads(chunk.decode())
                if data["error_code"] == 0:
                    output = data["text"][len(prompt) :].strip()
                    llm_outputs = data["llm_outputs"].strip() + "▌"

                    asr_outputs = data["asr_outputs"].strip()
                    state.messages[-1][-1] = (output + "▌", llm_outputs)

                    state.chatbot[-2].text = asr_outputs
                    state.chatbot[-1].msg = output + "▌"
                    state.chatbot[-1].text = llm_outputs

                    if time.time() - last_print_time > 0.05:
                        last_print_time = time.time()
                        yield (state, state.to_gradio_chatbot_from_chat()) + (
                            disable_btn,
                        ) * 5
                else:
                    output = data["text"] + f" (error_code: {data['error_code']})"
                    state.messages[-1][-1] = output
                    state.chatbot[-1].msg = output
                    yield (state, state.to_gradio_chatbot_from_chat()) + (
                        disable_btn,
                        disable_btn,
                        disable_btn,
                        enable_btn,
                        enable_btn,
                    )
                    return
                time.sleep(0.03)
    except requests.exceptions.RequestException as e:
        state.messages[-1][-1] = server_error_msg
        state.chatbot[-1].msg = server_error_msg
        yield (state, state.to_gradio_chatbot_from_chat()) + (
            disable_btn,
            disable_btn,
            disable_btn,
            enable_btn,
            enable_btn,
        )
        return

    try:
        if inference_type == "speech_to_speech":
            final_audio, final_text = state.messages[-1][-1]

            state.messages[-1][-1] = final_audio[:-1]
            generate_audio = token_to_speech_from_tokens(state.messages[-1][-1])[
                "audio_file"
            ]
            state.messages[-1][-1] = (
                state.messages[-1][-1],
                final_text[:-1],
                generate_audio,
            )

            state.chatbot[-1].msg = state.chatbot[-1].msg[:-1]
            if state.chatbot[-1].text is not None:
                state.chatbot[-1].text = state.chatbot[-1].text[:-1]
            state.chatbot[-1].audio = generate_audio
    except:
        pass

    yield (state, state.to_gradio_chatbot_from_chat()) + (enable_btn,) * 5

    finish_tstamp = time.time()
    logger.info(f"{output}")

    with open(get_conv_log_filename(), "a") as fout:
        data = {
            "tstamp": round(finish_tstamp, 4),
            "type": "chat",
            "model": model_name,
            "start": round(start_tstamp, 4),
            "finish": round(start_tstamp, 4),
            "state": state.dict(),
            "images": all_image_hash,
            "ip": request.client.host,
        }
        fout.write(json.dumps(data) + "\n")


title_markdown = """
# **Stream-Omni**: Simultaneous Multimodal Interactions with Large Language-Vision-Speech Model
"""

tos_markdown = """
"""


learn_more_markdown = """
### License
The service is a research preview intended for non-commercial use only, subject to the model [License](https://github.com/facebookresearch/llama/blob/main/MODEL_CARD.md) of LLaMA, [Terms of Use](https://openai.com/policies/terms-of-use) of the data generated by OpenAI, and [Privacy Practices](https://chrome.google.com/webstore/detail/sharegpt-share-your-chatg/daiacboceoaocpibfodeljbdfacokfjb) of ShareGPT. Please contact us if you find any potential violation.
"""

block_css = """

#buttons button {
    min-width: min(120px,100%);
}

"""


def build_demo(embed_mode):
    textbox = gr.Textbox(
        show_label=False, placeholder="Enter text and press ENTER", container=False
    )
    # audio_input = gr.Audio(label = "Audio Inputs", sources=['upload','microphone'], type="filepath")
    with gr.Blocks(title="LLaVA", theme=gr.themes.Default(), css=block_css) as demo:
        state = gr.State()

        if not embed_mode:
            gr.Markdown(title_markdown)

        with gr.Row():
            with gr.Column(scale=4):
                model_selector = gr.Dropdown(
                    choices=models,
                    value=models[0] if len(models) > 0 else "",
                    interactive=True,
                    show_label=False,
                    container=False,
                )
                imagebox = gr.Image(type="pil", height=200)
                image_process_mode = gr.Radio(
                    ["Crop", "Resize", "Pad", "Default"],
                    value="Default",
                    label="Preprocess for non-square image",
                    visible=False,
                )

            with gr.Column(scale=8):
                # audio_input.render()
                audio_input = gr.Audio(
                    label="Audio Inputs",
                    sources=["upload", "microphone"],
                    interactive=True,
                    type="filepath",
                )
        with gr.Row():
            chatbot = gr.Chatbot(elem_id="chatbot", label="LLaVA Chatbot", height=600)
        with gr.Row():
            with gr.Column(scale=10):
                textbox.render()
            with gr.Column(scale=2, min_width=50):
                submit_btn = gr.Button(value="Send", variant="primary")
        with gr.Row(elem_id="buttons") as button_row:
            upvote_btn = gr.Button(value="👍  Upvote", interactive=False)
            downvote_btn = gr.Button(value="👎  Downvote", interactive=False)
            flag_btn = gr.Button(value="⚠️  Flag", interactive=False)
            regenerate_btn = gr.Button(value="🔄  Regenerate", interactive=False)
            clear_btn = gr.Button(value="🗑️  Clear", interactive=False)
        with gr.Row():
            with gr.Column(scale=6):
                cur_dir = os.path.dirname(os.path.abspath(__file__))
                gr.Examples(
                    examples=[
                        # [f"{cur_dir}/examples/extreme_ironing.jpg", "What is unusual about this image?"],
                        # [f"{cur_dir}/examples/waterview.jpg", "What are the things I should be cautious about when I visit here?"],
                        [
                            f"{cur_dir}/examples/zebra.jpg",
                            f"{cur_dir}/examples/zebra.wav",
                        ],
                        [
                            f"{cur_dir}/examples/cat.jpg",
                            f"{cur_dir}/examples/cat_color.wav",
                        ],
                    ],
                    inputs=[imagebox, audio_input],
                )
            with gr.Column(scale=6):
                with gr.Accordion("Parameters", open=False) as parameter_row:
                    temperature = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.0,
                        step=0.1,
                        interactive=True,
                        label="Temperature",
                    )
                    top_p = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        interactive=True,
                        label="Top P",
                    )
                    max_output_tokens = gr.Slider(
                        minimum=0,
                        maximum=4096,
                        value=1024,
                        step=64,
                        interactive=True,
                        label="Max output tokens",
                    )

        if not embed_mode:
            gr.Markdown(tos_markdown)
            # gr.Markdown(learn_more_markdown)
        url_params = gr.JSON(visible=False)

        # Register listeners
        btn_list = [upvote_btn, downvote_btn, flag_btn, regenerate_btn, clear_btn]
        upvote_btn.click(
            upvote_last_response,
            [state, model_selector],
            [textbox, upvote_btn, downvote_btn, flag_btn],
            queue=False,
        )
        downvote_btn.click(
            downvote_last_response,
            [state, model_selector],
            [textbox, upvote_btn, downvote_btn, flag_btn],
            queue=False,
        )
        flag_btn.click(
            flag_last_response,
            [state, model_selector],
            [textbox, upvote_btn, downvote_btn, flag_btn],
            queue=False,
        )

        regenerate_btn.click(
            regenerate,
            [state, image_process_mode],
            [state, chatbot, textbox, imagebox] + btn_list,
            queue=False,
        ).then(
            http_bot,
            [state, model_selector, temperature, top_p, max_output_tokens],
            [state, chatbot] + btn_list,
        )

        clear_btn.click(
            clear_history,
            None,
            [state, chatbot, textbox, imagebox] + btn_list,
            queue=False,
        )

        textbox.submit(
            add,
            [state, textbox, audio_input, imagebox, image_process_mode],
            [state, chatbot, textbox, imagebox] + btn_list,
            queue=False,
        ).then(
            http_bot,
            [state, model_selector, temperature, top_p, max_output_tokens],
            [state, chatbot] + btn_list,
        )

        submit_btn.click(
            add,
            [state, textbox, audio_input, imagebox, image_process_mode],
            [state, chatbot, textbox, imagebox] + btn_list,
            queue=False,
        ).then(
            http_bot,
            [state, model_selector, temperature, top_p, max_output_tokens],
            [state, chatbot] + btn_list,
        )

        if args.model_list_mode == "once":
            demo.load(
                load_demo,
                [url_params],
                [state, model_selector],
                _js=get_window_url_params,
                queue=False,
            )
        elif args.model_list_mode == "reload":
            demo.load(
                load_demo_refresh_model_list, None, [state, model_selector], queue=False
            )
        else:
            raise ValueError(f"Unknown model list mode: {args.model_list_mode}")

    return demo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int)
    parser.add_argument("--controller-url", type=str, default="http://localhost:21001")
    parser.add_argument("--concurrency-count", type=int, default=10)
    parser.add_argument(
        "--model-list-mode", type=str, default="once", choices=["once", "reload"]
    )
    parser.add_argument("--share", action="store_true")
    parser.add_argument("--moderate", action="store_true")
    parser.add_argument("--embed", action="store_true")
    args = parser.parse_args()
    logger.info(f"args: {args}")

    models = get_model_list()

    logger.info(args)
    demo = build_demo(args.embed)
    demo.queue(api_open=False).launch(
        server_name=args.host, server_port=args.port, share=args.share
    )

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\CosyVoice\cosyvoice_worker.py
import argparse
import re
import time
from io import BytesIO
from pathlib import Path

import torch
import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

# 初始化 FastAPI 应用
app = FastAPI()

# 全局变量定义
cosyvoice = None
wav_dir = None
device = "cuda"


# 定义 helper 函数
def generate_speech_token(tensor):
    if len(tensor.shape) > 1:
        tensor = tensor.view(-1)
    audio_strings = [f"<Audio_{num.item()}>" for num in tensor]
    return "".join(audio_strings)


def extract_speech_token(input_string):
    numbers = re.findall(r"<Audio_(\d+)>", input_string)
    return list(map(int, numbers))


def speech_to_token(audio_file):
    speech, sample_rate = torchaudio.load(audio_file)
    speech_16k = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(speech)
    speech_token, _ = cosyvoice.frontend._extract_speech_token(speech_16k)
    return generate_speech_token(speech_token)


def token_to_speech(tokens):
    tts_speech_token = torch.tensor(extract_speech_token(tokens)).long().unsqueeze(0).to(device)
    embedding = cosyvoice.frontend.get_spk_embedding("英文女").to(device)
    flow_prompt_speech_token = torch.zeros(1, 0, dtype=torch.int32)
    flow_prompt_speech_token_len = torch.zeros(1, dtype=torch.int32)
    prompt_speech_feat = torch.zeros(1, 0, 80)
    prompt_speech_feat_len = torch.zeros(1, dtype=torch.int32)

    tts_mel, _ = cosyvoice.model.flow.inference(
        token=tts_speech_token,
        token_len=torch.tensor([tts_speech_token.size(1)], dtype=torch.int32).to(device),
        prompt_token=flow_prompt_speech_token.to(device),
        prompt_token_len=flow_prompt_speech_token_len.to(device),
        prompt_feat=prompt_speech_feat.to(device),
        prompt_feat_len=prompt_speech_feat_len.to(device),
        embedding=embedding.to(device),
        flow_cache=torch.zeros(1, 80, 0, 2).to(device),
    )
    tts_speech, _ = cosyvoice.model.hift.inference(speech_feat=tts_mel)
    # 使用时间戳命名输出文件
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    Path(wav_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(wav_dir).joinpath(f"generated_audio_{timestamp}.wav")

    torchaudio.save(output_path, tts_speech.cpu(), 22050)
    return output_path


# 请求体模型
class TokenRequest(BaseModel):
    tokens: str


# 语音转 token 接口
@app.post("/speech_to_token")
async def speech_to_token_endpoint(file: UploadFile = File(...)):
    try:
        audio_file = await file.read()
        audio_file = BytesIO(audio_file)
        token_string = speech_to_token(audio_file)
        return {"tokens": token_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


# token 合成语音接口
@app.post("/token_to_speech")
async def token_to_speech_endpoint(request: TokenRequest):
    try:
        tokens = request.tokens
        audio_path = token_to_speech(tokens)
        return {"audio_file": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI server for speech processing")
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=21003)
    parser.add_argument("--model", type=str, required=True, help="Path to CosyVoice model")
    parser.add_argument("--wav_dir", type=str, required=True, help="Directory to save generated audio")
    args = parser.parse_args()

    # 初始化全局 cosyvoice 和输出目录变量
    cosyvoice = CosyVoice(args.model)
    wav_dir = args.wav_dir

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)

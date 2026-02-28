# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\tts\tts_writer.py
import os

from environment.agents.base import BaseTool
from environment.config.llm import claude, deepseek
from pydantic import BaseModel, Field


class TTSWriter(BaseTool):
    """
    Application scenario: A reworded version of the original video
    Prerequisite： Transcriber must be called
    Rewrite the transcript of the sliced audio segments based on user requirements.
    """

    def __init__(self):
        super().__init__()

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(..., description="User requirements for text writing")
        audio_path: str = Field(
            ..., description="File path to the audio track of the video"
        )
        # slice_dir: str = Field(
        #     ...,
        #     description="Directory for the sliced audio (transcribed)"
        # )

    class OutputSchema(BaseModel):
        speech_path: str = Field(
            ..., description="File path to save the rewritten text"
        )

    def execute(self, **kwargs):

        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        lab_path = os.path.splitext(params.audio_path)[0] + ".lab"
        slice_lab_dir = os.path.splitext(params.audio_path)[0]

        slice_lab = []
        file_list = sorted([f for f in os.listdir(slice_lab_dir) if f.endswith(".lab")])

        for filename in file_list:
            file_path = os.path.join(slice_lab_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                slice_lab.append(file.read().strip())
        with open(lab_path, "r", encoding="utf-8") as f:
            text = f.read()

        output_format = "\n".join(
            [
                f"{i + 1}. 原切片内容：{content}\n   二创："
                for i, content in enumerate(slice_lab)
            ]
        )

        user_prompt = f"""
        你是一位鬼畜文本二创专家，擅长生成符合新场景的鬼畜文本。以下是你的任务：

        我将提供音频文本，以及该文本的切片，你需要根据以下几点和用户要求来进行二创：
        1. 在确保切片之间行文流畅的前提下，对每个切片进行二创
        2. 模仿每个切片的语言风格、句式结构等，只做具体内容上的替换
        3. 替换原文词汇时，长度变化不超过两个字 
        
        用户要求：
            {params.reqs}

        原文本：
            {text}

        输出格式：
            {output_format}
        
        输出内容前后不要添加无关字符，或者解释
        """
        try:
            response = claude(user=user_prompt)
        except Exception as e:
            print(e)
        generated_text = response.choices[0].message.content
        speech_path = os.path.join(os.path.dirname(lab_path), "raw_speech.txt")

        with open(speech_path, "w", encoding="utf-8") as f:
            f.write(generated_text)

        extract_prompt = f"""
        你是一位文本提取专家。以下是你的任务：
        
        我将提供类似如下形式的文本：
         1. 原切片内容：...
        二创：...
        
        2. 原切片内容：...
        二创：...
        
        具体要求：
        你需要提取每段切片的**二创**内容，并分行输出
        
        输出格式：
        切片1的二创
        切片2的二创
        
        需提取的文本：
        {generated_text}
        
        输出内容前后不要添加无关字符，或者解释
        """
        response = deepseek(user=extract_prompt)
        extract_text = response.choices[0].message.content

        speech_path = os.path.join(os.path.dirname(lab_path), "speech.txt")

        with open(speech_path, "w", encoding="utf-8") as f:
            f.write(extract_text)

        return {"speech_path": speech_path}

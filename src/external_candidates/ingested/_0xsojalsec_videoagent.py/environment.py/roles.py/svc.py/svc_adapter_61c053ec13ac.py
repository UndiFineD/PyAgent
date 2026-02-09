# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\svc\svc_adapter.py
import json
import os

from environment.agents.base import BaseTool
from environment.config.llm import claude, deepseek
from pydantic import BaseModel, Field


class SVCAdapter(BaseTool):
    """
    Application scenario: Music cover (maintaining original melody with modified lyrics and vocal timbre alteration)
    Adapt the original lyrics
    """

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(..., description="User requirements for lyrics adaptation")
        analysis_path: str = Field(
            ..., description="File path to the MIDI analysis results"
        )
        name: str = Field(..., description="Name of the song")

    class OutputSchema(BaseModel):
        adapted_lyrics: str = Field(..., description="String of the adapted lyrics")

    def __init__(self):
        super().__init__()

    def parse_lyrics_structure(self, lyrics):
        """解析歌词结构，返回包含AP和歌词的list，以及LYRICS部分的原歌词"""

        parts = lyrics.split("AP")
        structure = []
        lyrics_parts = []
        for i, part in enumerate(parts):
            if part:
                structure.append("LYRICS")  # 用 "LYRICS" 占位
                lyrics_parts.append(part)  # 存储原歌词
            if i < len(parts) - 1:  # 如果不是最后一个部分
                structure.append("AP")  # 添加 "AP"
        return structure, lyrics_parts

    def generate_lyrics_template(self, lyrics_parts):
        """生成歌词模板，原歌词内容紧接在原歌词片段后面，并留出二创空间和字数限制"""
        template = []
        for index, part in enumerate(lyrics_parts):
            cleaned_part = part.strip()
            word_count = len(cleaned_part)
            template.append(f"{index + 1}. 原歌词片段：{cleaned_part}")
            template.append(f"\t字数限制：{word_count}")
            template.append("\t二创：")
        return "\n".join(template)

    def align_lyrics_template(self, lyrics_part, extract_part):
        """
        生成原歌词片段、字数限制和二创信息的模板
        """
        template = f"""
            原歌词片段：{lyrics_part}
            字数限制：{len(lyrics_part)}
            二创：{extract_part}
        """
        return template

    def generate_full_lyrics(self, original_lyrics, reqs, template):
        """全歌词生成（含自动修正）"""

        prompt = f"""
                你是一个专业歌词改编AI，需要根据用户要求对整首歌词进行高质量二创。

                我将提供原歌词信息，以及输出格式，你需要根据以下几点和用户要求来进行二创：
                1. 严格遵循输出格式中对于每个二创片段的字数限制
                2. 歌词在叙事的同时，注重押韵和节奏感
                3. 填词需要保证句子语义完整
                4. 词语搭配要合理
                5. 二创歌词片段间注意押韵

                用户要求：
                {reqs}

                原歌词信息:
                - AP代表段落分隔，帮助你理解断句
                - 完整原歌词：
                {original_lyrics}

                输出格式：
                {template}

                输出要求:
                1. 补全输出格式的二创部分
                2. 输出内容前后不要添加无关字符、标点符号或者解释
                3. 不要添加AP标志
                """

        response = claude(user=prompt)
        generated_lyrics = response.choices[0].message.content.strip()
        return generated_lyrics

    def extract_full_lyrics(self, generated_lyrics):
        extract_prompt = f"""
                        你是一位歌词提取专家。以下是你的任务：

                        我将提供类似如下形式的文本：
                        1. 原歌词片段：...
                        字数限制：...
                        二创：...

                        2. 原歌词片段：...
                        字数限制：...
                        二创：...

                        具体要求：
                        你需要提取每个歌词片段的**二创**内容，并分行输出

                        输出格式：
                        片段1的二创
                        片段2的二创

                        需提取的文本：
                        {generated_lyrics}

                        输出内容前后不要添加无关字符，或者解释
                        """
        try:
            print(extract_prompt)
            response = deepseek(user=extract_prompt)
            extract_lyrics = response.choices[0].message.content.strip()
            return extract_lyrics
        except Exception as e:
            print(e)

    def align_extract_parts(self, lyrics_parts, extract_parts, reqs):
        """
        对齐 extract_parts 和 lyrics_parts 的长度，并生成反思提示
        """
        if len(extract_parts) != len(lyrics_parts):
            extract_parts.extend([""] * (len(lyrics_parts) - len(extract_parts)))

        for i in range(len(lyrics_parts)):
            target_length = len(lyrics_parts[i])
            retry_count = 0
            while len(extract_parts[i]) != target_length and retry_count < 5:
                previous_lyrics_context = lyrics_parts[i - 1] if i > 0 else ""
                previous_extract_context = extract_parts[i - 1] if i > 0 else ""
                problem_segment = extract_parts[i]
                next_lyrics_context = (
                    lyrics_parts[i + 1] if i < len(lyrics_parts) - 1 else ""
                )
                next_extract_context = (
                    extract_parts[i + 1] if i < len(lyrics_parts) - 1 else ""
                )

                previous_lyrics_template = (
                    self.align_lyrics_template(
                        previous_lyrics_context, previous_extract_context
                    )
                    if previous_lyrics_context
                    else ""
                )
                problem_segment_template = self.align_lyrics_template(
                    lyrics_parts[i], problem_segment
                )
                next_lyrics_template = (
                    self.align_lyrics_template(
                        next_lyrics_context, next_extract_context
                    )
                    if next_lyrics_context
                    else ""
                )

                align_prompt = f"""
                    你是一位歌词对齐专家。以下是你的任务:

                    我将提供你之前生成的二创问题片段，以及问题片段的上下文信息，你需要根据以下几点和用户要求来进行对齐：
                    1. 你之前的二创版本与对应的原歌词片段存在字数不匹配的问题
                    2. 你需要根据对应的歌词字数限制，重新生成该字数的二创片段

                    生成要求：
                    1. 严格按照问题片段中给定的字数要求二创
                    2. 填词需要保证句子语义完整
                    3. 词语搭配要合理
                    4. 二创歌词片段间注意押韵

                    根据语境，选择性地满足用户要求：
                    {reqs}

                    问题片段上文信息:
                    {previous_lyrics_template}

                    问题片段信息：
                    {problem_segment_template}

                    问题片段下文信息：
                    {next_lyrics_template}

                    输出要求:
                    1. 只输出问题片段对齐后的**二创**歌词
                    2. 输出内容前后不要添加无关字符、标点符号或者解释
                    3. 不要添加原歌词、字数限制等其他信息  
                """

                response = claude(user=align_prompt)
                new_extract_part = response.choices[0].message.content.strip()
                extract_parts[i] = new_extract_part
                retry_count += 1
            if len(extract_parts[i]) != target_length:
                while len(extract_parts[i]) < target_length:
                    extract_parts[i] += "啦"
                if len(extract_parts[i]) > target_length:
                    extract_parts[i] = extract_parts[i][:target_length]

        return extract_parts

    def execute(self, **kwargs):

        params = self.InputSchema(**kwargs)
        print(f"Parameters validated successfully")

        reqs = params.reqs
        analysis_path = params.analysis_path
        name = params.name

        with open(analysis_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        original_lyrics = data["text"]

        lyrics_structure, lyrics_parts = self.parse_lyrics_structure(original_lyrics)
        template = self.generate_lyrics_template(lyrics_parts)
        print("-------------------------------------------------")
        print("Creating Lyrics.....")
        generated_lyrics = self.generate_full_lyrics(
            original_lyrics,
            reqs,
            template,
        )

        output_path = os.path.join(os.path.dirname(analysis_path), "raw_lyrics.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated_lyrics)

        extract_lyrics = self.extract_full_lyrics(generated_lyrics)
        print(extract_lyrics)
        extract_parts = extract_lyrics.strip().split("\n")

        print("-------------------------------------------------")
        print("Aligning Lyrics...")
        aligned_extract_parts = self.align_extract_parts(
            lyrics_parts, extract_parts, reqs
        )
        output_path = os.path.join(os.path.dirname(analysis_path), "lyrics.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(aligned_extract_parts))

        if len(lyrics_structure) != len(aligned_extract_parts) + lyrics_structure.count(
            "AP"
        ):
            raise ValueError("structure 和 aligned_extract_parts 的长度不匹配")

        extract_index = 0
        for i in range(len(lyrics_structure)):
            if lyrics_structure[i] == "LYRICS":
                lyrics_structure[i] = aligned_extract_parts[extract_index].strip()
                extract_index += 1

        result = "".join(lyrics_structure)
        with open(
            os.path.join(os.path.dirname(analysis_path), "script.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(result)
        data["text"] = result
        with open(
            os.path.join(os.path.dirname(analysis_path), f"{name}_cover.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"adapted_lyrics": result}

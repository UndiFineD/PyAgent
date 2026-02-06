# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_news\news_story_gen.py
import json
import logging
import os
import time
from typing import Dict

from environment.agents.base import BaseTool
from environment.config.llm import gpt
from pydantic import BaseModel, Field
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NewsContentGenerator(BaseTool):
    """
    Prerequisite: Must Call the AudioExtractor and Transcriber agent
    Agent that generates news summary based on user ideas and reference materials.
    """

    def __init__(self):
        super().__init__()
        self.max_tokens = 15000
        self.timeout = 45

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(
            ...,
            description="User's creative requirements for the news summarization video",
        )
        news_present_style: str = Field(
            ...,
            description="File path to news presentation style for content generation",
        )
        video_path: str = Field(
            ..., description="Directory containing reference news videos"
        )

    class OutputSchema(BaseModel):
        video_scene_path: str = Field(
            ...,
            description="File path storing scene semantics for video storyboard sound synthesis.",
        )

    def _find_first_lab_file(self, directory: str) -> str:
        """
        Find the first .lab file in the given directory

        Args:
            directory (str): Directory path to search for .lab files

        Returns:
            str: Path to the first .lab file found

        Raises:
            FileNotFoundError: If no .lab file is found in the directory
        """
        try:
            if not os.path.exists(directory):
                raise FileNotFoundError(f"Directory does not exist: {directory}")

            if not os.path.isdir(directory):
                raise ValueError(f"Path is not a directory: {directory}")

            # Search for .lab files in the directory
            lab_files = []
            for filename in os.listdir(directory):
                if filename.lower().endswith(".lab"):
                    lab_files.append(os.path.join(directory, filename))

            if not lab_files:
                raise FileNotFoundError(
                    f"No .lab files found in directory: {directory}"
                )

            # Sort to ensure consistent behavior and return the first one
            lab_files.sort()
            first_lab_file = lab_files[0]

            logger.info(
                f"Found {len(lab_files)} .lab file(s), using: {os.path.basename(first_lab_file)}"
            )
            return first_lab_file

        except Exception as e:
            logger.error(f"Error finding .lab file in {directory}: {e}")
            raise

    def _load_lab_file(self, lab_path: str) -> str:
        """
        Load content from a .lab file
        .lab files typically contain timestamped transcriptions
        Directly reads all content
        """
        try:
            logger.info(f"Loading .lab file: {lab_path}")

            encodings_to_try = [
                "utf-8",
                "gb18030",
                "gbk",
                "gb2312",
                "cp1252",
                "iso-8859-1",
            ]

            # Try different encodings
            for encoding in encodings_to_try:
                try:
                    with open(
                        lab_path, "r", encoding=encoding, errors="replace"
                    ) as file:
                        text_content = file.read()

                        logger.info(
                            f"Successfully read .lab file with encoding: {encoding}"
                        )
                        return text_content.strip()
                except UnicodeDecodeError:
                    continue

            # Fallback to binary reading
            logger.info("Trying binary reading approach for .lab file")
            with open(lab_path, "rb") as file:
                content = file.read().decode("utf-8", errors="replace")
                return content.strip()

        except Exception as e:
            logger.error(f"Error loading .lab file: {e}")
            return ""

    def _load_text(self, txt_path: str) -> str:
        """Load content from a text file"""
        encodings_to_try = ["utf-8", "gb18030", "gbk", "gb2312", "cp1252", "iso-8859-1"]

        for encoding in encodings_to_try:
            try:
                logger.info(f"Trying to read file with encoding: {encoding}")
                with open(txt_path, "r", encoding=encoding, errors="replace") as file:
                    content = file.read()
                logger.info(f"Successfully read file with encoding: {encoding}")
                return content
            except UnicodeDecodeError:
                continue

        try:
            logger.info("Trying binary reading approach")
            with open(txt_path, "rb") as file:
                content = file.read().decode("utf-8", errors="replace")
            return content
        except Exception as e:
            logger.error(f"Error loading text file: {e}")
            return ""

    @retry(
        retry=retry_if_exception_type((Exception)),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _make_api_call(
        self,
        system_message,
        user_message,
        temperature=0.7,
        max_tokens=None,
        timeout=None,
    ):
        """Make an API call with retries and exponential backoff using tenacity"""
        if max_tokens is None:
            max_tokens = min(2000, self.max_tokens)
        if timeout is None:
            timeout = self.timeout

        try:
            logger.info(
                f"Making API call with system and user messages, timeout={timeout}s"
            )
            start_time = time.time()

            # Use llm function with system and user parameters
            response = gpt(system=system_message, user=user_message)

            elapsed_time = time.time() - start_time
            logger.info(f"API call completed in {elapsed_time:.2f}s")
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"API call failed with error: {e}, retrying...")
            raise e  # Re-raise to trigger tenacity retry

    def _presenter_agent(
        self, user_idea: str, content: str, present_content: str
    ) -> str:
        """Process content and adapt to user's idea - directly using input content"""

        prompt = f"""
        Create a skit narration copy, strictly following the user's ideas and presentation methods.

        User's idea:
        "{user_idea}"
        
        Grounded text content:
        {content}

        Follow this presentation method, read it and apply it carefully:
        {present_content}
        
        Requirements:
        1. Format and Structure:
        - Remove all sections numbers
        - Don't write too short sentences (Each sentence should contain more than 11 words) !!!
        - Present as one combined, coherent paragraph
        - Begin with clear news background establishment
        
        2. Content Guidelines:
        - Strictly abide by the user's words/字数 count requirements
        - Use only original key dialogues (no fabricated dialogues)
        - Remove unnecessary environmental descriptions
        - Focus on plot-advancing elements
        - Do not use the " " symbol
        
        3. Language and Style:
        - Third-person perspective
        - Process in text language (English/中文)
        - Do not use Arabic numerals. Change all numbers to English words, such as 5 becomes five
        - Do not use slash '/' within the writing
        - When encountering abbreviations of proper nouns, separate the word and the abbreviation appropriately, for example, ChatGPT becomes Chat GPT, OpenAI becomes Open AI, and AndroidOS becomes Android OS
        - Maintain clear narrative flow
        - Never mention or show user's requirements in content
        - Remove duplicated sentences
        
        Create a single, polished version that meets all these requirements.
        """

        try:
            system_message = "You are an experienced expert in news writing skit review copy. Pay special attention to user's words/字数 count requirements."

            logger.info("Starting presenter agent processing")
            result = self._make_api_call(
                system_message=system_message,
                user_message=prompt,
                temperature=0.7,
                timeout=120,  # Increased timeout for processing larger content
            )

            logger.info("Completed skit narration generation")
            return result

        except Exception as e:
            logger.error(f"Error in presenter_agent: {e}")
            return content[:15000]

    def _judger_agent(self, user_idea: str, presenter_output: str) -> str:
        """Structure the content with proper formatting based on presentation method"""
        prompt = f"""
        User's idea/用户的想法: "{user_idea}"

        Content to format/要结构化的内容:
        {presenter_output}

        Format above content into sections with requirements:

        - Remove all commas, 
        - Start /////\n
        - Chunk each period with \n\n/////\n and No need to chunk at the end of the content !
        - Remove any chapter numbers
        - Keep original content 
        - The purpose is to separate each sentence
        - Align 

        Example format:

        Input:
        /////\nGood morning everyone, nice to meet you again.\n\n/////\nThe weather is very nice today.

        Output:

        /////\nGood morning everyone nice to meet you again.\n\n/////\nThe weather is very nice today.

        
        #################

        - 删除所有逗号
        - 以 /////\n 开头
        - 用 \n\n////\n 分割每个句号，内容的最末尾无需分割！
        - 删除任何章节号
        - 保留原始内容
        - 目的是将每个句子分开

        示例格式：

        输入：
        /////\n大家早上好，很高兴再次见到你。\n\n/////\n今天天气很好。

        输出：

        /////\n大家早上好很高兴再次见到你。\n\n/////\n今天天气很好。
        """

        for attempt in range(2):
            try:
                logger.info(f"Starting judger agent (attempt {attempt+1}/2)")
                system_message = "You are a content formatting specialist with expertise in following guidelines"

                result = self._make_api_call(
                    system_message=system_message,
                    user_message=prompt,
                    temperature=0.4,
                    timeout=60,
                )
                logger.info("Judger agent completed successfully")
                return result
            except Exception as e:
                logger.error(f"Error in judger_agent (attempt {attempt+1}/2): {e}")
                if attempt < 1:
                    time.sleep(2)
                    # Truncate output if needed
                    if len(presenter_output) > 15000:
                        presenter_output = presenter_output[:15000]
                        # Create a new prompt with truncated content
                        prompt = prompt.replace(
                            "Content to format/要结构化的内容:",
                            f"Content to format/要结构化的内容:\n{presenter_output}",
                        )
                    logger.info("Truncated presenter output for retry")
                else:
                    logger.info("Using simple formatting fallback")
                    return f"/////\n{presenter_output}"

    def _process_pipeline(
        self, user_idea: str, txt_path: str, pre_txt_path: str
    ) -> str:
        """Main pipeline process - directly using presenter agent"""
        # Check if pre_txt_path is a file path or direct content
        if os.path.exists(pre_txt_path):
            present_content = self._load_text(pre_txt_path)
            logger.info("Loaded presentation method from file")
        else:
            present_content = pre_txt_path  # Use the string directly
            logger.info("Using provided presentation method string")

        # Load content, handling different file extensions
        file_ext = os.path.splitext(txt_path)[1].lower()
        if file_ext == ".lab":
            book_content = self._load_lab_file(txt_path)
            logger.info("Loaded content from .lab file")
        else:
            book_content = self._load_text(txt_path)
            logger.info("Loaded content from text file")

        word_count = len(book_content.split())
        char_count = len(book_content)
        logger.info(
            f"Text data statistics: {word_count} words, {char_count} characters"
        )

        # Limit content length if necessary
        if len(book_content) > 30000:
            logger.warning(
                f"Content too large ({len(book_content)} chars), truncating to 30K"
            )
            book_content = book_content[:30000]

        try:
            # Pass content directly to presenter agent
            presenter_output = self._presenter_agent(
                user_idea, book_content, present_content
            )
            logger.info("Successfully generated presentation")
        except Exception as e:
            logger.error(f"Error in presenter_agent: {e}")
            presenter_output = book_content[:15000]
            logger.info("Used truncated content as fallback")

        try:
            formatted_content = self._judger_agent(user_idea, presenter_output)
            logger.info("Successfully structured content with judger_agent")
        except Exception as e:
            logger.error(f"Error in judger_agent: {e}")
            formatted_content = f"/////\n{presenter_output}"
            logger.info("Used simple formatting fallback")

        return formatted_content

    def _create_content(
        self, user_idea: str, txt_path: str, pre_txt_path: str
    ) -> Dict[str, str]:
        """Generate video content incorporating user ideas and reference materials."""
        try:
            # Get formatted content from the pipeline
            formatted_content = self._process_pipeline(
                user_idea, txt_path, pre_txt_path
            )
            general_content = formatted_content

            scene_translation_prompt = f"""
            Key requirements:
            - Keep the number of "/////" mark unchanged.
            - You CAN ONLY deduce by English visual-scene description.
            - Deduce visual-scene keywords in English, each sections of content deduce some scene keywords (especially proper noun, eg. iphone 16, SWE Arena Benchmark ...).
            - Keep the same number of paragraph separators and spacing.
            - Each scene sections' description don't exceed 1 sentences.
            - Don't directly translate each sentences.


            Content for to process:
            "{general_content}"

            ############################

            Example Input:

            /////\nEmily and Jackson stood together, the ocean breeze ruffling their hair, both soaking up the moment, surrounded by the vastness of the ocean, which reflected their budding love.\n\n/////\nThe leader increased Xiao Wang's business freedom by changing the company's management rules.

            Example Output:

            /////\nA couple standing together on the sunset seaside with hair blown by the wind\n\n/////\nyoung employees within office environment

            """

            system_message = "You are a English text-scene description expert"
            response = gpt(system=system_message, user=scene_translation_prompt)

            query_content = response.choices[0].message.content

            return {"query": query_content, "general": general_content}

        except Exception as e:
            return {"error": f"Error: {e}"}

    def _count_content_sections(self, content: str) -> int:
        """
        Count the number of sections in the content marked by '/////'.

        Args:
            content (str): Content string with section markers

        Returns:
            int: Number of sections found
        """
        try:
            # Count sections by splitting on the marker
            sections = content.split("/////")

            # Filter out empty sections
            valid_sections = [s.strip() for s in sections if s.strip()]

            # Print each section with its number
            print("\nContent Sections Found:")
            for i, section in enumerate(valid_sections, 1):
                print(f"\nSection {i}:")
                print(
                    section.strip()[:100] + "..."
                    if len(section) > 100
                    else section.strip()
                )

            return len(valid_sections)

        except Exception as e:
            print(f"Error counting sections: {e}")
            return 0

    def execute(self, **kwargs):
        """Generate news content based on user ideas and reference materials."""
        # Validate input parameters
        params = self.InputSchema(**kwargs)
        user_idea = params.reqs

        # Get the current file's directory
        current_dir = os.getcwd()
        video_edit_dir = os.path.join(current_dir, "dataset/video_edit")

        # Ensure required directories exist
        scene_output_dir = os.path.join(video_edit_dir, "scene_output")
        os.makedirs(video_edit_dir, exist_ok=True)
        os.makedirs(scene_output_dir, exist_ok=True)

        # Define file paths
        video_scene_path = os.path.join(scene_output_dir, "video_scene.json")

        # Find the first .lab file in the video directory
        try:
            transcript_path = self._find_first_lab_file(params.video_path)
        except Exception as e:
            raise RuntimeError(f"Failed to find .lab file: {e}")

        # Get presentation style
        present_style = params.news_present_style

        print("\n=== CREATING VIDEO OVERVIEW CONTENT ===")
        print(f"\nUsing idea: {user_idea}")
        print(f"Using text source: {transcript_path}")

        # Generate content
        content_result = self._create_content(user_idea, transcript_path, present_style)

        if "error" in content_result:
            raise RuntimeError(f"Failed to create content: {content_result['error']}")

        content_output = {
            "user_idea": user_idea,
            "content_created": content_result.get("general", ""),
            "segment_scene": content_result.get("query", ""),
        }

        with open(video_scene_path, "w", encoding="utf-8") as f:
            json.dump(content_output, f, indent=2, ensure_ascii=False)

        print("\nContent saved to", video_scene_path)
        num_sections = self._count_content_sections(content_result.get("general", ""))
        print(f"\n{num_sections} Sections have been created")

        return {"video_scene_path": video_scene_path}

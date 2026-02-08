# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VideoAgent\environment\roles\vid_comm\comm_story_gen.py
import json
import logging
import os
import time

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
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class CommentaryContentGenerator(BaseTool):
    """
    Agent that generates commentary content based on user ideas and text source materials with specialized formatting for video presentations.
    """

    def __init__(self):
        super().__init__()
        self.max_tokens = 15000
        self.timeout = 45

    class InputSchema(BaseTool.BaseInputSchema):
        reqs: str = Field(
            ...,
            description="User's idea for the commentary video including word count requirements",
        )
        source_text: str = Field(..., description="File path to the novel source text")
        comm_present_style: str = Field(
            ...,
            description="File path to commentary presentation style for content generation",
        )

    class OutputSchema(BaseModel):
        video_scene_path: str = Field(
            ...,
            description="File path storing scene semantics for video storyboard sound synthesis.",
        )

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
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    def _make_api_call(self, messages, temperature=0.7, max_tokens=None, timeout=None):
        """Make an API call with retries and exponential backoff using tenacity"""
        if max_tokens is None:
            max_tokens = min(2000, self.max_tokens)
        if timeout is None:
            timeout = self.timeout

        try:
            logger.info(f"Making API call with {len(messages)} messages, timeout={timeout}s")
            start_time = time.time()

            # Extract system and user messages from the messages array
            system_message = None
            user_message = None

            for message in messages:
                if message["role"] == "system":
                    system_message = message["content"]
                elif message["role"] == "user":
                    user_message = message["content"]

            # Call llm with the extracted messages
            response = gpt(system=system_message, user=user_message)

            elapsed_time = time.time() - start_time
            logger.info(f"API call completed in {elapsed_time:.2f}s")
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"API call failed with error: {e}, retrying...")
            raise e  # Re-raise to trigger tenacity retry

    def _presenter_agent(self, user_idea: str, content: str, present_content: str) -> str:
        """Process content and adapt to user's idea - directly using input content"""

        # Create a unified conversation history
        messages = [
            {
                "role": "system",
                "content": "You are an experienced expert in writing review copy. Pay special attention to user's words/字数 count requirements.",
            },
            {
                "role": "user",
                "content": f"""
            You can only create a narration copy, strictly following the user's ideas and presentation methods.


            User idea:
            "{user_idea}"
            
            Grounded text content:
            {content}

            Follow this presentation method, read it and apply it carefully:
            {present_content}
            
            Requirements:
            1. Format and Structure:
            - Response in grounded text language (English/中文)
            - Remove all chapter numbers
            - No more than 3 commas are allowed in a sentence
            - Present as one combined, coherent paragraph
            - Begin with clear story background establishment
            
            2. Content Guidelines:
            - Strictly follow user's words count/总字数 requirements
            - Use only original key dialogues (no fabricated dialogues)
            - Remove unnecessary environmental descriptions
            - Focus on plot-advancing elements
            - Do not use the " " and symbol
            
            3. Language and Style:
            - Maintain clear narrative flow (Be careful not to lose the plot in the second half of the narration copy)
            - Never mention or show user's requirements in content
            - Remove duplicated sentences
            
            Create a single, polished version that meets all these requirements.
            """,
            },
        ]

        try:
            logger.info("Starting presenter agent processing")
            result = self._make_api_call(
                messages,
                temperature=0.7,
                timeout=120,  # Increased timeout for processing full content
                max_tokens=16384,
            )

            logger.info("Completed skit narration generation")
            print(result)
            return result

        except Exception as e:
            logger.error(f"Error in presenter_agent: {e}")
            return content[:15000]

    def _judger_agent(self, user_idea: str, presenter_output: str) -> str:
        """Structure the content with proper formatting based on presentation method"""

        # Unified conversation history for judger
        messages = [
            {
                "role": "system",
                "content": "You are a content formatting specialist with expertise in following guidelines",
            },
            {
                "role": "user",
                "content": f"""
            User's idea/用户的想法: "{user_idea}"

            Content to format/要结构化的内容:
            {presenter_output}

            Format above content into sections with requirements:


            - Don't response anything unrelated
            - Start each sentence with /////
            - Remove any chapter numbers
            - Keep original content 
            - The purpose is to separate each sentence
            - Remove all punctuation marks after segmentation

            Example format:
            /////\nsentence one. \n\n/////\nsentence two.
            
            #################

            将上述内容格式化为符合要求的部分：

            - 根据每个句子以 ///// 开头
            - 删除所有章节编号
            - 保留原始内容
            - 目的是为了分割每一句话
            - 划分完成后去除所有标点符号

            示例格式：
            /////\n你好吗。 \n\n/////\n早上好。
            """,
            },
        ]

        for attempt in range(2):
            try:
                logger.info(f"Starting judger agent (attempt {attempt + 1}/2)")

                result = self._make_api_call(messages, temperature=0.4, timeout=60, max_tokens=16384)
                logger.info("Judger agent completed successfully")
                return result
            except Exception as e:
                logger.error(f"Error in judger_agent (attempt {attempt + 1}/2): {e}")
                if attempt < 1:
                    time.sleep(2)
                    # Truncate presenter output for the retry
                    if len(presenter_output) > 15000:
                        presenter_output = presenter_output[:15000]
                        # Update the message for retry
                        messages[1]["content"] = messages[1]["content"].replace(
                            f"Content to format/要结构化的内容:\n{presenter_output}",
                            f"Content to format/要结构化的内容:\n{presenter_output[:15000]}",
                        )
                    logger.info("Truncated presenter output for retry")
                else:
                    logger.info("Using simple formatting fallback")
                    return f"/////\n{presenter_output}"

    def _process_pipeline(self, user_idea: str, txt_path: str, present_style: str) -> str:
        """Main pipeline process - simplified to directly use presenter agent"""
        logger.info("Using presentation style from config")

        book_content = self._load_text(txt_path)

        word_count = len(book_content.split())
        char_count = len(book_content)
        logger.info(f"Text data statistics: {word_count} words, {char_count} characters")

        # Limit book content if it's too large for direct processing
        if len(book_content) > 30000:
            logger.warning(f"Content too large ({len(book_content)} chars), truncating to 30K")
            book_content = book_content[:30000]

        try:
            # Pass content directly to presenter agent
            presenter_output = self._presenter_agent(user_idea, book_content, present_style)
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

    def _create_scene_descriptions(self, general_content: str) -> str:
        """Generate visual scene descriptions from the formatted content"""

        scene_translation_prompt = f"""
        Key requirements:

        - Keep the number of "/////" mark unchanged.
        - You CAN ONLY deduce by English visual-scene description.
        - Deduce visual-scene description in English for each sections.
        - Keep the same number of paragraph separators and spacing.
        - Each scene sections' description don't exceed 1 sentences.
        - Don't directly translate each sentences.
        - If the sections do not have high-quality scene descriptions (eg. declarative or interrogative sentence), replace the scene descriptions of the sections with some conflict scenes that are high-ignition points in the story (eg. a fight scene of a certain protagonist)
        - Whenever a character is mentioned by name within the sections, the scene description must describe the character's appearance (eg. gender, physical features)

        Content for to process:
        "{general_content}"

        ############################

        Example Input:

        /////\nEmily and Jackson stood together, the ocean breeze ruffling their hair, both soaking up the moment, surrounded by the vastness of the ocean, which reflected their budding love.\n\n/////\nThe leader increased Xiao Wang's business freedom by changing the company's management rules.

        Example Output:

        /////\nA Red hair Emily and brown hair Jackson standing together on the sunset seaside with hair blown by the wind\n\n/////\nwhite t-shirt young employees within office environment

        """

        system_message = "You are an expert in inference of converting English text into scene descriptions"

        response = gpt(system=system_message, user=scene_translation_prompt)
        return response.choices[0].message.content

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
                print(section.strip()[:100] + "..." if len(section) > 100 else section.strip())

            return len(valid_sections)

        except Exception as e:
            print(f"Error counting sections: {e}")
            return 0

    def execute(self, **kwargs):
        """Generate commentary content based on user ideas and reference materials."""
        # Validate input parameters
        params = self.InputSchema(**kwargs)
        reqs = params.reqs

        # Get the current file's directory
        current_dir = os.getcwd()

        # Ensure required directories exist
        video_edit_dir = os.path.join(current_dir, "dataset/video_edit")
        scene_output_dir = os.path.join(video_edit_dir, "scene_output")
        os.makedirs(video_edit_dir, exist_ok=True)
        os.makedirs(scene_output_dir, exist_ok=True)
        # Define file paths
        video_scene_path = os.path.join(scene_output_dir, "video_scene.json")

        # source text path
        txt_path = params.source_text

        # Get presentation style
        present_style = params.comm_present_style

        print("\n=== CREATING COMMENTARY CONTENT ===")
        print(f"\nUsing idea: {reqs}")
        print(f"Using source text: {txt_path}")

        # Process the content through the pipeline
        formatted_content = self._process_pipeline(reqs, txt_path, present_style)

        # Generate scene descriptions
        query_content = self._create_scene_descriptions(formatted_content)

        # Create output structure
        content_output = {
            "reqs": reqs,
            "content_created": formatted_content,
            "segment_scene": query_content,
        }

        # Save to file
        with open(video_scene_path, "w", encoding="utf-8") as f:
            json.dump(content_output, f, indent=2, ensure_ascii=False)

        print("\nContent saved to", video_scene_path)
        num_sections = self._count_content_sections(formatted_content)
        print(f"\n{num_sections} Sections have been created")

        return {"video_scene_path": video_scene_path}

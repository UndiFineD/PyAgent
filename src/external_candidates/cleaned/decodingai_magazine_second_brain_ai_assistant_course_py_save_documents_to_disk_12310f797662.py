# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\steps.py\infrastructure.py\save_documents_to_disk_12310f797662.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\steps\infrastructure\save_documents_to_disk.py

import shutil

from pathlib import Path

from second_brain_offline.domain import Document

from typing_extensions import Annotated

from zenml import get_step_context, step


@step
def save_documents_to_disk(
    documents: Annotated[list[Document], "documents"],
    output_dir: Path,
) -> Annotated[str, "output"]:
    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True)

    for document in documents:
        document.write(output_dir=output_dir, obfuscate=True, also_save_as_txt=True)

    step_context = get_step_context()

    step_context.add_output_metadata(
        output_name="output",
        metadata={
            "count": len(documents),
            "output_dir": str(output_dir),
        },
    )

    return str(output_dir)

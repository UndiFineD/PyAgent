# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\decodingai_magazine_second_brain_ai_assistant_course.py\apps.py\second_brain_offline.py\steps.py\infrastructure.py\save_dataset_to_disk_97143feb6d7b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\decodingai-magazine-second-brain-ai-assistant-course\apps\second-brain-offline\steps\infrastructure\save_dataset_to_disk.py

import shutil

from pathlib import Path

from loguru import logger

from second_brain_offline.domain import InstructDataset

from typing_extensions import Annotated

from zenml import get_step_context, step


@step
def save_dataset_to_disk(
    dataset: Annotated[InstructDataset, "instruct_dataset"],
    output_dir: Path,
) -> Annotated[str, "output"]:
    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True)

    logger.info(f"Saving dataset to '{output_dir}'")

    output_dir = dataset.write(output_dir=output_dir)

    step_context = get_step_context()

    step_context.add_output_metadata(
        output_name="output",
        metadata={
            "train_samples": len(dataset.train),
            "validation_samples": len(dataset.validation),
            "test_samples": len(dataset.test),
            "output_dir": str(output_dir),
        },
    )

    return str(output_dir)

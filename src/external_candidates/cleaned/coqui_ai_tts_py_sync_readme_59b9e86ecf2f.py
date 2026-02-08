# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\scripts.py\sync_readme_59b9e86ecf2f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\scripts\sync_readme.py

import argparse

from pathlib import Path


def replace_between_markers(content, marker: str, replacement: str) -> str:
    start_marker = f"<!-- begin-{marker} -->\n\n"

    end_marker = f"\n\n<!-- end-{marker} -->\n"

    start_index = content.index(start_marker) + len(start_marker)

    end_index = content.index(end_marker)

    content = content[:start_index] + replacement + content[end_index:]

    return content


def sync_readme():
    ap = argparse.ArgumentParser()

    ap.add_argument("--check", action="store_true", default=False)

    args = ap.parse_args()

    readme_path = Path(__file__).parent.parent / "README.md"

    orig_content = readme_path.read_text()

    from TTS.bin.synthesize import description

    new_content = replace_between_markers(orig_content, "tts-readme", description.strip())

    if args.check:
        if orig_content != new_content:
            print(
                "README.md is out of sync; please reconcile README.md and TTS/bin/synthesize.py and run scripts/sync_readme.py"
            )

            exit(42)

        print("All good, files in sync")

        exit(0)

    readme_path.write_text(new_content)

    print("Updated README.md")


if __name__ == "__main__":
    sync_readme()

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\utils.py\seq_151adace7d0d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\utils\seq.py

from Bio import Align


def align_protein_global(a: str, b: str) -> Align.Alignment:
    aligner = Align.PairwiseAligner(mode="global", scoring="blastp")

    alignments = aligner.align(a, b)

    return alignments[0]

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\utils\seq.py
from Bio import Align


def align_protein_global(a: str, b: str) -> Align.Alignment:
    aligner = Align.PairwiseAligner(mode="global", scoring="blastp")
    alignments = aligner.align(a, b)
    return alignments[0]

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tts.py\tts.py\utils.py\measures_cf6d5edf6761.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\tts\utils\measures.py


def alignment_diagonal_score(alignments, binary=False):
    """

    Compute how diagonal alignment predictions are. It is useful

    to measure the alignment consistency of a model

    Args:

        alignments (torch.Tensor): batch of alignments.

        binary (bool): if True, ignore scores and consider attention

        as a binary mask.

    Shape:

        - alignments : :math:`[B, T_de, T_en]`

    """

    maxs = alignments.max(dim=1)[0]

    if binary:
        maxs[maxs > 0] = 1

    return maxs.mean(dim=1).mean(dim=0).item()

# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whisperlivekit.py\whisperlivekit.py\trail_repetition_46097b132a61.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-WhisperLiveKit\whisperlivekit\trail_repetition.py

from typing import Any, Callable, Dict, Optional, Sequence


def _detect_tail_repetition(
    seq: Sequence[Any],
    key: Callable[[Any], Any] = lambda x: x,  # extract comparable value
    min_block: int = 1,  # set to 2 to ignore 1-token loops like "."
    max_tail: int = 300,  # search window from the end for speed
    prefer: str = "longest",  # "longest" coverage or "smallest" block
) -> Optional[Dict]:

    vals = [key(x) for x in seq][-max_tail:]

    n = len(vals)

    best = None

    # try every possible block length

    for b in range(min_block, n // 2 + 1):
        block = vals[-b:]

        # count how many times this block repeats contiguously at the very end

        count, i = 0, n

        while i - b >= 0 and vals[i - b : i] == block:
            count += 1

            i -= b

        if count >= 2:
            cand = {
                "block_size": b,
                "count": count,
                "start_index": len(seq) - count * b,  # in original seq
                "end_index": len(seq),
            }

            if (
                best is None
                or (prefer == "longest" and count * b > best["count"] * best["block_size"])
                or (prefer == "smallest" and b < best["block_size"])
            ):
                best = cand

    return best


def trim_tail_repetition(
    seq: Sequence[Any],
    key: Callable[[Any], Any] = lambda x: x,
    min_block: int = 1,
    max_tail: int = 300,
    prefer: str = "longest",
    keep: int = 1,  # how many copies of the repeating block to keep at the end (0 or 1 are common)
):
    """

    Returns a new sequence with repeated tail trimmed.

    keep=1 -> keep a single copy of the repeated block.

    keep=0 -> remove all copies of the repeated block.

    """

    rep = _detect_tail_repetition(seq, key, min_block, max_tail, prefer)

    if not rep:
        return seq, False  # nothing to trim

    b, c = rep["block_size"], rep["count"]

    if keep < 0:
        keep = 0

    if keep >= c:
        return seq, False  # nothing to trim (already <= keep copies)

    # new length = total - (copies_to_remove * block_size)

    new_len = len(seq) - (c - keep) * b

    return seq[:new_len], True

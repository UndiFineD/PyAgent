# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\utils.py\residue_selection_24c542fe9ce8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\utils\residue_selection.py

import itertools

import json

from collections import defaultdict

from io import StringIO

from typing import Dict, List

from Bio.PDB import PDBParser


def from_residues_to_segments(
    chain_id: str,
    residues: list[int],
    start_res: int | None = None,
    end_res: int | None = None,
) -> list[str]:
    """Convert a list of residues [3,4,5,6,9,10,...] into a list of segments [3-6,9-10,...].

    Args:

        chain_id (str): Required. The chain ID.

        residues (list[int]): Required. A list of residues.

        start_res (int, optional): The start residue. If specified, trims residues from start_res. Defaults to None.

        end_res (int, optional): The end residue. If specified, trims residues to end_res. Defaults to None.

    Returns:

        list(str): A list of segments, i.e. [3-6,9-10,...]

    """

    if not residues:
        return []

    if start_res is not None:
        residues = [res for res in residues if res >= start_res]

    if end_res is not None:
        residues = [res for res in residues if res <= end_res]

    segments = []

    start = end = residues[0]

    for i in range(1, len(residues)):
        if residues[i] == residues[i - 1] + 1:
            end = residues[i]

        else:
            segments.append(f"{chain_id}{start}-{end}")

            start = end = residues[i]

    segments.append(f"{chain_id}{start}-{end}")

    return segments


def from_residues_to_hotspots(chain_id: str, residues: list[int]):
    """Convert a chain_id (i.e. A) and list of residues [3,4,...] into list of hotspots [A3, A4, ...]."""

    return [f"{chain_id}{res}" for res in residues]


def parse_selections(selections: str) -> list[str]:
    """

    Input: a JSON-encoded representation of the selections that looks like this

        {"sequenceSelections":[{"chainId":"A","residues":[10,11,12,13,15,16,17,18,19,20"]}]}

    Outputs list o segments ["A10-13", "A15-20"]

    """

    if selections is None:
        return []

    selections_json = json.loads(selections)

    selections_list = selections_json["sequenceSelections"]

    # for each of these, let's create a different representation

    result = []

    for selection in selections_list:
        chain_id = selection["chainId"]

        residues = selection["residues"]

        result += from_residues_to_segments(chain_id, residues)

    return result


def get_chains_and_contigs(pdb_str: str | None) -> Dict[str, str] | None:

    if pdb_str is None:
        return None

    parser = PDBParser(QUIET=True)

    struc = parser.get_structure("PDB_structure", StringIO(pdb_str))

    segments_by_chain = {}

    # Iterate through models, chains, and residues

    for model in struc:
        for chain in model:
            chain_id = chain.id  # Get the chain identifier

            residues = set()  # Use a set to hold unique residues

            for residue in chain:
                # Ensure the residue is an ATOM or ALA/GLY/other relevant residue

                if residue.id[0] == " " and int(residue.id[1]) > -1:
                    residues.add(int(residue.get_id()[1]))  # Get the residue number (not the insertion code)

            segments_by_chain[chain_id] = sorted(residues)

    segments_by_chain_json = {
        chain: parse_selections(json.dumps({"sequenceSelections": [{"chainId": chain, "residues": list(residues)}]}))
        for chain, residues in segments_by_chain.items()
    }

    return {chain: "/".join(segments) for chain, segments in segments_by_chain_json.items()}


def from_hotspots_to_segments(hotspots: str) -> list[str] | None:

    hotspots_by_chain = defaultdict(list)

    if not hotspots:
        return None

    # TODO: Maybe some more regex checks?

    for s in hotspots.split(","):
        hotspots_by_chain[s[0]].append(int(s[1:].replace(" ", "")))

    result = []

    for chain, hotspot_nums in hotspots_by_chain.items():
        hotspot_nums.sort()

        result.extend(from_residues_to_segments(chain, hotspot_nums))

    return result


def from_segments_to_hotspots(segments: list[str] | None) -> str:
    """Convert a list of segments ["A3-5","A9-10",...] to a STRING of hotspots "A3,A4,A5,A9,A10"."""

    if not segments:
        return ""

    hotspots = []

    for segment in segments:
        chain = segment[0]

        start_resnum = int(segment[1:].split("-")[0])

        end_resnum = int(segment[1:].split("-")[-1])

        hotspots.extend([f"{chain}{resnum}" for resnum in range(start_resnum, end_resnum + 1)])

    return ",".join(hotspots)


def from_contig_to_residues(chain_segment: str | None) -> list[int] | None:
    """Convert a str chain_segment / contig "A3-5/A9-10" to a list of residues [3,4,5,9,10]."""

    if not chain_segment:
        return None

    contig_segments = chain_segment.split(" ")[0].removesuffix("/0").split("/")

    residues = []

    # Merge non-consecutive residues into a list

    for segment in contig_segments:
        start_resnum = int(segment[1:].split("-")[0])

        end_resnum = int(segment[1:].split("-")[-1])

        residues += list(range(start_resnum, end_resnum + 1))

    return residues


def from_residues_to_chain_breaks(residues: list[int]) -> List[str] | None:

    residues.sort()

    chain_break_segments = []

    for i in range(1, len(residues)):
        # Check for a gap between consecutive numbers

        if residues[i] - residues[i - 1] > 1:
            missing_start_res = residues[i - 1]

            missing_end_res = residues[i]

            chain_break_segments.append(f"{missing_start_res}-{missing_end_res}")

    return chain_break_segments


def parse_partial_diffusion_binder_contig(binder_contig: str) -> tuple[int, list[str]]:
    """Get binder length and DESIGNED segments from binder contig as they correspond to positions in binder chain A

    default case for a peptide of 12 residues is simply binder_contig="12-12" turned into ["A1-12"]

    or when redesigning only A1 and A3-7 in a peptide of 12 residues, this would be

    binder_contig="1-1/A2-2/5-5/A8-12" turned into ["A1-1", "A3-7"]

    :param binder_contig: binder contig, e.g. 12-12 or 1-1/A2-2/5-5/A8-12

    :return: binder length (int) and list of designed segments (list of str, e.g. ["A1-1", "A3-7"])

    """

    assert " " not in binder_contig, f"Expected single chain in binder_contig, got: {binder_contig}"

    pos = 0

    designed_segments = []

    for segment in binder_contig.split("/"):
        if segment[0].isalpha():
            # fixed segment

            assert segment[0] == "A", f"Expected first contig in partial diffusion to be in chain A, got: {segment}"

            assert "-" in segment, f"Expected fixed segment in partial diffusion to be in format A2-3, got: {segment}"

            start, end = segment[1:].split("-")

            assert int(start) <= int(end), (
                f"Invalid fixed segment in partial diffusion, start must be <= end, got: {segment}"
            )

            assert int(start) == pos + 1, (
                f"Segment {segment} at generated position {pos + 1} should start with A{pos + 1} in partial diffusion"
            )

            pos += int(end) - int(start) + 1

        else:
            # designed segment

            assert "-" in segment, f"Expected designed segment in partial diffusion to be in format 5-5, got: {segment}"

            segment_length, _ = segment.split("-")

            assert segment_length == _, (
                f"Designed segments should have same start and end residue in partial diffusion, got: {segment}"
            )

            designed_segments.append(f"A{pos + 1}-{pos + int(segment_length)}")

            pos += int(segment_length)

    return pos, designed_segments


def create_partial_diffusion_binder_contig(redesigned_segments: list[str], binder_length: int) -> str:
    """Create a new binder contig for partial diffusion from the designed segments and old binder contig

    default case for a peptide of 12 residues:

    redesigned_segments=[] -> binder_contig="12-12"

    or when redesigning only A1 and A3-7 in a peptide of 12 residues,

    redesigned_segments=["A1-1", "A3-7"] -> binder_contig="1-1/A2-2/5-5/A8-12"

    :param redesigned_segments: list of designed segments (list of str, e.g. ["A1-1", "A3-7"])

    :param binder_length: length of binder (int)

    :return: new binder contig (str)

    """

    assert all([segment[0] == "A" for segment in redesigned_segments]), (
        f"Expected all redesigned segments to be in chain A, got: {redesigned_segments}"
    )

    redesigned_str = from_segments_to_hotspots(redesigned_segments)

    redesigned_positions = [int(res[1:]) for res in redesigned_str.split(",")] if redesigned_str else []

    all_positions = list(range(1, binder_length + 1))

    new_binder_segments = []

    for is_redesigned, positions in itertools.groupby(all_positions, lambda x: x in redesigned_positions):
        positions = list(positions)

        if is_redesigned:
            new_binder_segments.append(f"{len(positions)}-{len(positions)}")

        else:
            new_binder_segments.append(f"A{positions[0]}-{positions[-1]}")

    return "/".join(new_binder_segments)

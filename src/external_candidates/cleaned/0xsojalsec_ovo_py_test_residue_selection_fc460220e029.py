# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\tests.py\unit_tests.py\test_residue_selection_fc460220e029.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\test_residue_selection.py

import json

from ovo.core.utils.residue_selection import (
    create_partial_diffusion_binder_contig,
    from_contig_to_residues,
    from_hotspots_to_segments,
    from_residues_to_chain_breaks,
    from_residues_to_hotspots,
    from_residues_to_segments,
    from_segments_to_hotspots,
    get_chains_and_contigs,
    parse_partial_diffusion_binder_contig,
    parse_selections,
)


def test_from_residues_to_segments_simple():

    assert from_residues_to_segments("A", [3, 4, 5, 6, 9, 10]) == ["A3-6", "A9-10"]


def test_from_residues_to_hotspots_simple():

    assert from_residues_to_hotspots("A", [3, 4]) == ["A3", "A4"]


def test_parse_selections_simple():

    selections = json.dumps({"sequenceSelections": [{"chainId": "A", "residues": [10, 11, 12, 15, 16]}]})

    assert parse_selections(selections) == ["A10-12", "A15-16"]


def test_get_chains_and_contigs_simple():

    pdb_str = """\

ATOM      1  N   ALA A   1      11.104  13.207   2.100  1.00 20.00           N  

ATOM      2  CA  ALA A   2      12.000  13.000   3.000  1.00 20.00           C  

ATOM      3  N   GLY B   5      10.000  10.000   1.000  1.00 20.00           N  

ATOM      4  CA  GLY B   6      10.500  11.000   1.500  1.00 20.00           C  

END

"""

    result = get_chains_and_contigs(pdb_str)

    assert result == {"A": "A1-2", "B": "B5-6"}


def test_from_hotspots_to_segments_simple():

    assert from_hotspots_to_segments("A3,A4,A5,A9,A10") == ["A3-5", "A9-10"]


def test_from_segments_to_hotspots_simple():

    assert from_segments_to_hotspots(["A3-5", "A9-10"]) == "A3,A4,A5,A9,A10"


def test_from_contig_to_residues_simple():

    assert from_contig_to_residues("A3-5/A9-10") == [3, 4, 5, 9, 10]


def test_from_residues_to_chain_breaks_simple():

    assert from_residues_to_chain_breaks([1, 2, 5, 6]) == ["2-5"]


def test_parse_partial_diffusion_binder_contig_default():

    length, designed = parse_partial_diffusion_binder_contig("12-12")

    assert length == 12

    assert designed == ["A1-12"]


def test_parse_partial_diffusion_binder_contig_no_redesigned():

    length, designed = parse_partial_diffusion_binder_contig("A1-12")

    assert length == 12

    assert designed == []


def test_parse_partial_diffusion_binder_contig_simple():

    length, designed = parse_partial_diffusion_binder_contig("1-1/A2-2/5-5/A8-12")

    assert length == 12

    assert designed == ["A1-1", "A3-7"]


def test_create_partial_diffusion_binder_contig_default():

    result = create_partial_diffusion_binder_contig(["A1-12"], 12)

    assert result == "12-12"


def test_create_partial_diffusion_binder_contig_no_redesigned():

    result = create_partial_diffusion_binder_contig([], 12)

    assert result == "A1-12"


def test_create_partial_diffusion_binder_contig_simple():

    result = create_partial_diffusion_binder_contig(["A1-1", "A3-7"], 12)

    assert result == "1-1/A2-2/5-5/A8-12"

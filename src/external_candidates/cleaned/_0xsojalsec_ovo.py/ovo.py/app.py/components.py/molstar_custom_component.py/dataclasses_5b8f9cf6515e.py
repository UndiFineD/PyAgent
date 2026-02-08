# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\molstar_custom_component\dataclasses.py
import dataclasses
import json
from typing import Literal


@dataclasses.dataclass
class ContigSegment:
    """Class for storing data about individual contig regions."""

    value: str
    length: int
    type: str
    input_res_start: int
    input_res_end: int
    input_res_chain: str
    out_res_start: int
    out_res_end: int
    out_res_chain: str
    color: str | None = None


class EnhancedJSONEncoder(json.JSONEncoder):
    """A JSON encoder for enabling the export of dataclasses."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # type: ignore
        return super().default(o)


@dataclasses.dataclass
class ChainVisualization:
    """Class for storing data about individual chains.

    Parameters
    ----------
    chain_id : str
        The chain ID.
    color : Literal["uniform", "chain-id", "hydrophobicity", "plddt", "molecule-type", "secondary-structure", "residue-name"], optional
        The color scheme to use, by default "uniform".
    color_params : dict, optional
        Color parameters.
        In the case of "uniform", the `color_params` field should be for example {"value": "0x00ff00"}.
        In the case of "chain-id", the `color_params` field should be for example {"palette": "pastel-1"}.
    representation_type : Literal["cartoon", "cartoon+ball-and-stick", "molecular-surface", "gaussian-surface", "ball-and-stick"], optional
        The representation type to use, by default "cartoon".
    residues : list[int], optional
        Create a representation just for the specified residues, by default None (all residues).
    label : str, optional
        The label to show when hovering over the visualization, by default None.
    """

    chain_id: str
    color: Literal[
        "uniform",
        "chain-id",
        "hydrophobicity",
        "plddt",
        "molecule-type",
        "secondary-structure",
        "residue-name",
    ] = "uniform"
    color_params: dict | None = None
    representation_type: Literal[
        "cartoon",
        "cartoon+ball-and-stick",
        "molecular-surface",
        "gaussian-surface",
        "ball-and-stick",
    ] = "cartoon"
    residues: list[int] | None = None
    label: str | None = None


@dataclasses.dataclass
class StructureVisualization:
    """Class for storing data about structures shown in the Mol* component.

    Parameters
    ----------
    pdb : str
        A PDB/mmCIF content of the structure to visualize. Can also be a URL to a PDB/mmCIF file.
    contigs : list[ContigSegment], optional
        A list of contig segments to show (e.g. on the top of the viewer), by default None.
    color : Literal["uniform", "chain-id", "hydrophobicity", "plddt", "molecule-type", "secondary-structure", "residue-name"], optional
        The color scheme to use, by default "uniform".
    color_params : dict, optional
        Color parameters.
        In the case of "uniform", the `color_params` field should be for example {"value": "0x00ff00"}.
        In the case of "chain-id", the `color_params` field should be for example {"palette": "pastel-1"}.
    representation_type : Literal["cartoon", "cartoon+ball-and-stick", "molecular-surface", "gaussian-surface", "ball-and-stick"], optional
        The representation type to use, by default "cartoon".
    highlighted_selections : list[str], optional
        A list of selections to select and highlight in green color, by default None.
    chains : list[ChainVisualization], optional
        A list of separate chain visualizations, useful for individual coloring and representation, by default None. Available only for PDB files in a string format.
    """

    pdb: str
    contigs: str | list[ContigSegment] | None = None
    color: Literal[
        "uniform",
        "chain-id",
        "hydrophobicity",
        "plddt",
        "molecule-type",
        "secondary-structure",
        "residue-name",
    ] = "uniform"
    color_params: dict | None = None
    representation_type: (
        Literal[
            "cartoon",
            "cartoon+ball-and-stick",
            "molecular-surface",
            "gaussian-surface",
            "ball-and-stick",
        ]
        | None
    ) = "cartoon"
    highlighted_selections: list[str] | None = None
    chains: list[ChainVisualization] | None = None

    def __post_init__(self):
        if self.chains:
            if isinstance(self.chains, ChainVisualization):
                self.chains = [self.chains]
            elif not isinstance(self.chains, list):
                raise ValueError(
                    f"Invalid type for chains, expected ChainVisualization or list of ChainVisualization, got: {type(self.chains).__name__}"
                )
        if self.contigs:
            from ovo.app.components.molstar_custom_component import ContigsParser

            parser = ContigsParser()
            if isinstance(self.contigs, str):
                parsed_contigs = parser.parse_contigs_str(self.contigs)
            else:
                assert isinstance(self.contigs, list), (
                    f"Invalid type for contigs, expected str or list, got: {type(self.contigs).__name__}"
                )
                parsed_contigs = []
                for contig_or_segment in self.contigs:
                    if isinstance(contig_or_segment, str):
                        parsed_contigs.extend(parser.parse_contigs_str(contig_or_segment))
                    elif isinstance(contig_or_segment, ContigSegment):
                        parsed_contigs.append(contig_or_segment)
                    else:
                        raise ValueError(
                            f"Invalid type for contig segment, expected str or ContigSegment, got: {type(contig_or_segment).__name__}"
                        )
            self.contigs = parsed_contigs

    def to_dict(self):
        return dataclasses.asdict(self)

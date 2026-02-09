# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\molstar_custom_component\main.py
import os

import streamlit as st
from molstar_custom_component import molstar_custom_component
from molstar_custom_component.contigs_parser import ContigsParser
from molstar_custom_component.dataclasses import (
    ChainVisualization,
    StructureVisualization,
)

# `$ python -m streamlit run molstar_custom_component/main.py`
# do not forget to have venv activated

# pdb_path = st.text_input("Enter a PDB URL/filepath", value="http://localhost:5500/ovo_molstar/test_files/multichain_scaffold/test_0.pdb")
# trb_path = st.text_input("Enter a .trb URL/filepath", value="http://localhost:5500/ovo_molstar/test_files/multichain_scaffold/test_0.trb")

# contigs = st.text_input("Specify the contigs (not used when .trb file provided)", value="A117-125/10-20/A107-114/10-20/A47-53/10-20/A60-65")

paths = [
    "http://localhost:5500/ovo/app/components/molstar_custom_component/test_files/multichain_more/result_0",
    "http://localhost:5500/ovo/app/components/molstar_custom_component/test_files/multichain_binder/result_0",
    "http://localhost:5500/ovo/app/components/molstar_custom_component/test_files/multichain_scaffold/test_0",
]

for path in paths:
    pdb_path = path + ".pdb"
    trb_path = path + ".trb"

    print(pdb_path)

    if os.path.exists(pdb_path):
        pdb = open(pdb_path).read()
    else:
        pdb = pdb_path

    parser = ContigsParser()
    contigs = parser.parse_contigs_trb(trb_path)

    cp = molstar_custom_component(
        structures=[
            StructureVisualization(
                pdb=pdb,
                highlighted_selections=["A22-25", "A28-30"],
                color="hydrophobicity",
                representation_type="gaussian-surface",
                contigs=contigs,
            ),
            StructureVisualization(
                pdb="http://localhost:5500/ovo/app/components/molstar_custom_component/test_files/multichain_scaffold/test_0.pdb",
                highlighted_selections=["A22-25", "A28-30"],
                chains=[
                    ChainVisualization(
                        chain_id="A",
                        color="uniform",
                        color_params={"value": "0x00ff00"},
                    )
                ],
            ),
        ],
        selection_mode=True,
        show_controls=True,
        key="example",
    )

    st.write(cp)

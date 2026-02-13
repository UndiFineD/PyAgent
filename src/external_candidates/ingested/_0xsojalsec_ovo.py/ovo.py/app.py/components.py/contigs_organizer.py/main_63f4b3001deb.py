# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\contigs_organizer\main.py
import os

import streamlit as st
from contigs_organizer import contigs_organizer

# `$ python -m streamlit run molstar_custom_component/main.py`
# do not forget to have venv activated

st.subheader("Component")

if os.path.exists("./test_files/multichain_more/result_0.pdb"):
    pdb = open("./test_files/multichain_more/result_0.pdb").read()
else:
    pdb = ""

co = contigs_organizer(
    contigs="22/A38-57/10/A76-94/10-20/A121-125", pdb=pdb, colors={}, key="test"
)  # parsing the full contig
# co = contigs_organizer(contigs="A38-57, A76-94, A115-120", liveInput=True, pdb=pdb) # parsing the fixed regions

st.write(co)

# contigs_organizer(contigs="A35-48/10/A107-123/0 B123-233")

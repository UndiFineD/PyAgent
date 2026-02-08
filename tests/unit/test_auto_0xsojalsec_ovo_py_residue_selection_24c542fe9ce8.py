
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_residue_selection_24c542fe9ce8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'from_residues_to_segments'), 'missing from_residues_to_segments'
assert hasattr(mod, 'from_residues_to_hotspots'), 'missing from_residues_to_hotspots'
assert hasattr(mod, 'parse_selections'), 'missing parse_selections'
assert hasattr(mod, 'get_chains_and_contigs'), 'missing get_chains_and_contigs'
assert hasattr(mod, 'from_hotspots_to_segments'), 'missing from_hotspots_to_segments'
assert hasattr(mod, 'from_segments_to_hotspots'), 'missing from_segments_to_hotspots'
assert hasattr(mod, 'from_contig_to_residues'), 'missing from_contig_to_residues'
assert hasattr(mod, 'from_residues_to_chain_breaks'), 'missing from_residues_to_chain_breaks'
assert hasattr(mod, 'parse_partial_diffusion_binder_contig'), 'missing parse_partial_diffusion_binder_contig'
assert hasattr(mod, 'create_partial_diffusion_binder_contig'), 'missing create_partial_diffusion_binder_contig'

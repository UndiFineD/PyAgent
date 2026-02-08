
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_residue_selection_fc460220e029.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_from_residues_to_segments_simple'), 'missing test_from_residues_to_segments_simple'
assert hasattr(mod, 'test_from_residues_to_hotspots_simple'), 'missing test_from_residues_to_hotspots_simple'
assert hasattr(mod, 'test_parse_selections_simple'), 'missing test_parse_selections_simple'
assert hasattr(mod, 'test_get_chains_and_contigs_simple'), 'missing test_get_chains_and_contigs_simple'
assert hasattr(mod, 'test_from_hotspots_to_segments_simple'), 'missing test_from_hotspots_to_segments_simple'
assert hasattr(mod, 'test_from_segments_to_hotspots_simple'), 'missing test_from_segments_to_hotspots_simple'
assert hasattr(mod, 'test_from_contig_to_residues_simple'), 'missing test_from_contig_to_residues_simple'
assert hasattr(mod, 'test_from_residues_to_chain_breaks_simple'), 'missing test_from_residues_to_chain_breaks_simple'
assert hasattr(mod, 'test_parse_partial_diffusion_binder_contig_default'), 'missing test_parse_partial_diffusion_binder_contig_default'
assert hasattr(mod, 'test_parse_partial_diffusion_binder_contig_no_redesigned'), 'missing test_parse_partial_diffusion_binder_contig_no_redesigned'
assert hasattr(mod, 'test_parse_partial_diffusion_binder_contig_simple'), 'missing test_parse_partial_diffusion_binder_contig_simple'
assert hasattr(mod, 'test_create_partial_diffusion_binder_contig_default'), 'missing test_create_partial_diffusion_binder_contig_default'
assert hasattr(mod, 'test_create_partial_diffusion_binder_contig_no_redesigned'), 'missing test_create_partial_diffusion_binder_contig_no_redesigned'
assert hasattr(mod, 'test_create_partial_diffusion_binder_contig_simple'), 'missing test_create_partial_diffusion_binder_contig_simple'

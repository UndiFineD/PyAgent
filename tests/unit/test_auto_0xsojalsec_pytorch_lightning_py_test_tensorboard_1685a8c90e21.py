
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_test_tensorboard_1685a8c90e21.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_tensorboard_automatic_versioning'), 'missing test_tensorboard_automatic_versioning'
assert hasattr(mod, 'test_tensorboard_manual_versioning'), 'missing test_tensorboard_manual_versioning'
assert hasattr(mod, 'test_tensorboard_named_version'), 'missing test_tensorboard_named_version'
assert hasattr(mod, 'test_tensorboard_no_name'), 'missing test_tensorboard_no_name'
assert hasattr(mod, 'test_tensorboard_log_sub_dir'), 'missing test_tensorboard_log_sub_dir'
assert hasattr(mod, 'test_tensorboard_expand_home'), 'missing test_tensorboard_expand_home'
assert hasattr(mod, 'test_tensorboard_expand_env_vars'), 'missing test_tensorboard_expand_env_vars'
assert hasattr(mod, 'test_tensorboard_log_metrics'), 'missing test_tensorboard_log_metrics'
assert hasattr(mod, 'test_tensorboard_log_hyperparams'), 'missing test_tensorboard_log_hyperparams'
assert hasattr(mod, 'test_tensorboard_log_hparams_and_metrics'), 'missing test_tensorboard_log_hparams_and_metrics'
assert hasattr(mod, 'test_tensorboard_log_graph_plain_module'), 'missing test_tensorboard_log_graph_plain_module'
assert hasattr(mod, 'test_tensorboard_log_graph_with_batch_transfer_hooks'), 'missing test_tensorboard_log_graph_with_batch_transfer_hooks'
assert hasattr(mod, 'test_tensorboard_log_graph_warning_no_example_input_array'), 'missing test_tensorboard_log_graph_warning_no_example_input_array'
assert hasattr(mod, 'test_tensorboard_finalize'), 'missing test_tensorboard_finalize'
assert hasattr(mod, 'test_tensorboard_with_symlink'), 'missing test_tensorboard_with_symlink'

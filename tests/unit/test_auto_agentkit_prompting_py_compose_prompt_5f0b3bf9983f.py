
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_compose_prompt_5f0b3bf9983f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'describe_gamestep'), 'missing describe_gamestep'
assert hasattr(mod, 'ComposeBasePrompt'), 'missing ComposeBasePrompt'
assert hasattr(mod, 'ComposeSummaryPrompt'), 'missing ComposeSummaryPrompt'
assert hasattr(mod, 'ComposeObservationPrompt'), 'missing ComposeObservationPrompt'
assert hasattr(mod, 'ComposeObservationReasoningPrompt'), 'missing ComposeObservationReasoningPrompt'
assert hasattr(mod, 'ComposeObservationActionReasoningPrompt'), 'missing ComposeObservationActionReasoningPrompt'
assert hasattr(mod, 'ComposeActionReflectionPrompt'), 'missing ComposeActionReflectionPrompt'
assert hasattr(mod, 'ComposePlannerPrompt'), 'missing ComposePlannerPrompt'
assert hasattr(mod, 'ComposePlannerReflectionPrompt'), 'missing ComposePlannerReflectionPrompt'
assert hasattr(mod, 'print_skill_library'), 'missing print_skill_library'
assert hasattr(mod, 'ComposeSkillPrompt'), 'missing ComposeSkillPrompt'
assert hasattr(mod, 'ComposeKBAddPrompt'), 'missing ComposeKBAddPrompt'
assert hasattr(mod, 'ComposeRewritePrompt'), 'missing ComposeRewritePrompt'
assert hasattr(mod, 'ComposeKBReasonPrompt'), 'missing ComposeKBReasonPrompt'
assert hasattr(mod, 'ComposeActorPlannerPrompt'), 'missing ComposeActorPlannerPrompt'
assert hasattr(mod, 'ComposeActorEfficiencyPrompt'), 'missing ComposeActorEfficiencyPrompt'
assert hasattr(mod, 'ComposeActorReasoningPrompt'), 'missing ComposeActorReasoningPrompt'
assert hasattr(mod, 'ComposeActorBarePrompt'), 'missing ComposeActorBarePrompt'
assert hasattr(mod, 'compose_filtered_gamestep_prompt'), 'missing compose_filtered_gamestep_prompt'
assert hasattr(mod, 'compose_feedback_prompt'), 'missing compose_feedback_prompt'
assert hasattr(mod, 'compose_gameplay_prompt'), 'missing compose_gameplay_prompt'

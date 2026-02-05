
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_convert_sqa_to_llava_base_prompt.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_question_text'), 'missing get_question_text'
assert hasattr(mod, 'get_context_text'), 'missing get_context_text'
assert hasattr(mod, 'get_choice_text'), 'missing get_choice_text'
assert hasattr(mod, 'get_answer'), 'missing get_answer'
assert hasattr(mod, 'get_lecture_text'), 'missing get_lecture_text'
assert hasattr(mod, 'get_solution_text'), 'missing get_solution_text'
assert hasattr(mod, 'create_one_example_chatbot'), 'missing create_one_example_chatbot'
assert hasattr(mod, 'create_one_example'), 'missing create_one_example'
assert hasattr(mod, 'create_one_example_gpt4'), 'missing create_one_example_gpt4'
assert hasattr(mod, 'build_prompt_chatbot'), 'missing build_prompt_chatbot'
assert hasattr(mod, 'build_prompt'), 'missing build_prompt'
assert hasattr(mod, 'build_prompt_gpt4'), 'missing build_prompt_gpt4'

import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.development.CodeTranslationAgent import CodeTranslationAgent
from unittest.mock import MagicMock, AsyncMock




class TestCodeTranslation(unittest.TestCase):
    def setUp(self):
        self.agent = CodeTranslationAgent(os.getcwd())
        # Mock the LLM output
        def fake_translator(text, *args, **kwargs):
            if "rust" in text.lower() or (args and "rust" in str(args).lower()) or (kwargs and "rust" in str(kwargs).lower()):
                return """
// Translated from python to rust
fn hello() {
    println!("Hello, world!");
}"""
            if "javascript" in text.lower() or (args and "javascript" in str(args).lower()):
                return """
// Translated from python to javascript
function greet(name) {
    console.log(`Hello, ${name}`);
}"""
            return "Mock translation"

        self.agent.improve_content = MagicMock(side_effect=fake_translator)
        # Also mock run_subagent as it might use that
        self.agent.run_subagent = AsyncMock(side_effect=fake_translator)

    def test_python_to_rust(self) -> None:
        py_code = """def hello():
    print("Hello, world!")
"""
        rust_code = self.agent.translate_file(py_code, "python", "rust")

        self.assertIn("fn hello() {", rust_code)
        self.assertIn("println!(\"Hello, world!\")", rust_code)










        self.assertIn("// Translated from python to rust", rust_code)

    def test_python_to_js(self) -> None:
        py_code = """def greet(name):




    print(f"Hello, {name}")
"""
        js_code = self.agent.translate_file(py_code, "python", "javascript")

        self.assertIn("function greet(name) {", js_code)


        self.assertIn("console.log(", js_code)
        self.assertIn("// Translated from python to javascript", js_code)

    def test_stats(self) -> None:
        self.agent.translate_file("print(1)", "python", "rust")



        stats = self.agent.get_translation_stats()
        self.assertEqual(stats['total_translations'], 1)
        self.assertIn("python", stats['source_languages'])
        self.assertIn("rust", stats['target_languages'])





if __name__ == "__main__":
    unittest.main()

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.logic.agents.development.CodeTranslationAgent import CodeTranslationAgent

class TestCodeTranslation(unittest.TestCase):
    def setUp(self):
        self.agent = CodeTranslationAgent(os.getcwd())

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

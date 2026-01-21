import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.development.code_translation_agent import CodeTranslationAgent
from unittest.mock import MagicMock, AsyncMock


class TestCodeTranslation(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = CodeTranslationAgent(os.getcwd())

        # Mock the LLM output
        async def fake_think(prompt, *args, **kwargs):
            if "rust" in prompt.lower():
                return """
// Translated from python to rust
fn hello() {
    println!("Hello, world!");
}"""
            if "javascript" in prompt.lower():
                return """
// Translated from python to javascript
function greet(name) {
    console.log(`Hello, ${name}`);
}"""
            return "Mock translation"

        self.agent.think = AsyncMock(side_effect=fake_think)

    async def test_python_to_rust(self) -> None:
        py_code = """def hello():
    print("Hello, world!")
"""
        rust_code = await self.agent.translate_file(py_code, "python", "rust")

        self.assertIn("fn hello() {", rust_code)
        self.assertIn('println!("Hello, world!")', rust_code)

        self.assertIn("// Translated from python to rust", rust_code)

    async def test_python_to_js(self) -> None:
        py_code = """def greet(name):
    print(f"Hello, {name}")
"""
        js_code = await self.agent.translate_file(py_code, "python", "javascript")

        self.assertIn("function greet(name) {", js_code)

        self.assertIn("console.log(", js_code)
        self.assertIn("// Translated from python to javascript", js_code)

    async def test_stats(self) -> None:
        await self.agent.translate_file("print(1)", "python", "rust")

        stats = self.agent.get_translation_stats()
        self.assertEqual(stats["total_translations"], 1)
        self.assertIn("python", stats["source_languages"])
        self.assertIn("rust", stats["target_languages"])


if __name__ == "__main__":
    unittest.main()

import os
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent

class CodeTranslationAgent(BaseAgent):
    """
    Handles translation of codebases between different programming languages.
    Supports mapping logic, syntax transformations, and multi-file translation.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.translation_history = []

    def translate_file(self, source_code: str, from_lang: str, to_lang: str) -> str:
        """
        Translates source code from one language to another using LLM reasoning.
        """
        logging.info(f"CodeTranslationAgent: Translating code from {from_lang} to {to_lang}.")
        
        prompt = (
            f"Translate the following {from_lang} code into {to_lang}.\n"
            "Ensure idiomatic conversion, preserving comments and structure.\n"
            "Respond ONLY with the translated code, no explanations.\n\n"
            f"### {from_lang} Source:\n{source_code}"
        )
        
        translated_code = self.think(prompt)
        
        # Strip markdown code blocks if present
        if translated_code.startswith("```"):
            lines = translated_code.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            translated_code = "\n".join(lines).strip()

        self.translation_history.append({
            "from_lang": from_lang,
            "to_lang": to_lang,
            "timestamp": "2026-01-10"
        })
        
        return translated_code

    def _mock_python_to_rust(self, code: str) -> str:
        """Mock conversion logic for Python to Rust."""
        lines = code.split("\n")
        rust_lines = []
        for line in lines:
            if "def " in line:
                rust_lines.append(line.replace("def ", "fn ").replace(":", " {"))
            elif "print(" in line:
                rust_lines.append(line.replace("print(", "println!("))
            else:
                rust_lines.append(line)
        return "\n".join(rust_lines)

    def _mock_python_to_js(self, code: str) -> str:
        """Mock conversion logic for Python to JavaScript."""
        lines = code.split("\n")
        js_lines = []
        for line in lines:
            if "def " in line:
                js_lines.append(line.replace("def ", "function ").replace(":", " {"))
            elif "print(" in line:
                js_lines.append(line.replace("print(", "console.log("))
            else:
                js_lines.append(line)
        return "\n".join(js_lines)

    def get_translation_stats(self) -> Dict[str, Any]:
        """Returns statistics on translation activities."""
        return {
            "total_translations": len(self.translation_history),
            "source_languages": list(set(t['from_lang'] for t in self.translation_history)),
            "target_languages": list(set(t['to_lang'] for t in self.translation_history))
        }

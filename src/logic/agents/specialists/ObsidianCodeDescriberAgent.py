# Copyright 2026 PyAgent Authors
# ObsidianCodeDescriberAgent: Obsidian Vault Documentation Specialist - Phase 319 Enhanced

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import os
import re
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

__version__ = VERSION

class NoteType(Enum):
    FILE = "file"
    CLASS = "class"
    FUNCTION = "function"
    MODULE = "module"
    CONCEPT = "concept"
    INDEX = "index"

@dataclass
class CodeEntity:
    """Represents a code entity to document."""
    name: str
    entity_type: str  # class, function, variable, etc.
    file_path: str
    line_number: int = 0
    docstring: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

@dataclass
class VaultNote:
    """Represents an Obsidian note."""
    title: str
    note_type: NoteType
    content: str
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    wikilinks: Set[str] = field(default_factory=set)

class ObsidianCodeDescriberAgent(BaseAgent):
    """
    Agent specializing in describing code and generating markdown files 
    formatted for an Obsidian knowledge vault (with [[wikilinks]]).
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._note_cache: Dict[str, VaultNote] = {}
        self._entity_registry: Dict[str, CodeEntity] = {}
        self._vault_path: Optional[Path] = None
        self._system_prompt = (
            "You are the Obsidian Vault Code Describing Agent. You analyze codebases "
            "and create interconnected Markdown notes. Use [[wikilinks]] for cross-references. "
            "Include YAML frontmatter for Obsidian plugins (e.g., Dataview). "
            "Create comprehensive, navigable documentation."
        )

    @as_tool
    async def describe_file_to_vault(
        self, 
        target_file: str, 
        vault_path: str,
        include_classes: bool = True,
        include_functions: bool = True,
        generate_moc: bool = False
    ) -> Dict[str, Any]:
        """Analyzes a file and creates corresponding Obsidian notes."""
        target = Path(target_file)
        if not target.exists():
            return {"success": False, "error": f"File not found: {target_file}"}

        self._vault_path = Path(vault_path)
        self._vault_path.mkdir(parents=True, exist_ok=True)

        code_content = target.read_text(encoding="utf-8")
        
        # Parse code structure
        entities = self._parse_code_entities(code_content, str(target))
        
        # Generate main file note
        main_note = await self._generate_file_note(target, code_content, entities)
        notes_created = [self._save_note(main_note)]
        
        # Generate notes for classes and functions if requested
        if include_classes:
            for entity in entities:
                if entity.entity_type == "class":
                    class_note = await self._generate_entity_note(entity, code_content)
                    notes_created.append(self._save_note(class_note))
        
        if include_functions:
            for entity in entities:
                if entity.entity_type == "function" and not entity.name.startswith("_"):
                    func_note = await self._generate_entity_note(entity, code_content)
                    notes_created.append(self._save_note(func_note))
        
        # Generate MOC (Map of Content) if requested
        if generate_moc:
            moc_note = self._generate_moc(target.stem, notes_created)
            notes_created.append(self._save_note(moc_note))
        
        return {
            "success": True,
            "notes_created": notes_created,
            "entities_documented": len(entities),
            "vault_path": str(self._vault_path)
        }

    @as_tool
    async def describe_directory_to_vault(
        self,
        source_dir: str,
        vault_path: str,
        file_pattern: str = "*.py",
        recursive: bool = True
    ) -> Dict[str, Any]:
        """Documents an entire directory to an Obsidian vault."""
        source = Path(source_dir)
        if not source.exists():
            return {"success": False, "error": f"Directory not found: {source_dir}"}
        
        self._vault_path = Path(vault_path)
        self._vault_path.mkdir(parents=True, exist_ok=True)
        
        # Find all matching files
        if recursive:
            files = list(source.rglob(file_pattern))
        else:
            files = list(source.glob(file_pattern))
        
        results = []
        for file_path in files:
            try:
                result = await self.describe_file_to_vault(
                    str(file_path), 
                    vault_path,
                    include_classes=True,
                    include_functions=False  # Only top-level for bulk
                )
                results.append({"file": str(file_path), "success": result.get("success")})
            except Exception as e:
                results.append({"file": str(file_path), "success": False, "error": str(e)})
        
        # Generate index note
        index_note = self._generate_index_note(source.name, results)
        self._save_note(index_note)
        
        return {
            "success": True,
            "files_processed": len(files),
            "results": results,
            "vault_path": str(self._vault_path)
        }

    @as_tool
    async def generate_concept_note(
        self,
        concept: str,
        related_files: List[str],
        vault_path: str
    ) -> Dict[str, Any]:
        """Generates a concept note linking multiple code files."""
        self._vault_path = Path(vault_path)
        self._vault_path.mkdir(parents=True, exist_ok=True)
        
        # Read related files
        file_contents = []
        for file_path in related_files:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
                file_contents.append({"path": file_path, "content": content[:2000]})
            except:
                pass
        
        prompt = (
            f"Create an Obsidian concept note about: {concept}\n\n"
            f"Related code files:\n"
            + "\n".join([f"- {f['path']}" for f in file_contents])
            + "\n\nCode excerpts:\n"
            + "\n---\n".join([f"**{f['path']}**:\n```python\n{f['content']}\n```" for f in file_contents])
            + "\n\nCreate a comprehensive concept note that:\n"
            "1. Explains the concept\n"
            "2. Links to the related files using [[wikilinks]]\n"
            "3. Provides usage examples\n"
            "4. Notes relationships to other concepts\n"
            "Include YAML frontmatter with tags and aliases."
        )
        
        note_content = await self.improve_content(prompt)
        
        note = VaultNote(
            title=concept,
            note_type=NoteType.CONCEPT,
            content=note_content,
            frontmatter={
                "type": "concept",
                "created": time.strftime("%Y-%m-%d"),
                "tags": ["concept", concept.lower().replace(" ", "-")]
            }
        )
        
        saved_path = self._save_note(note)
        
        return {
            "success": True,
            "note_path": saved_path,
            "concept": concept,
            "related_files": len(related_files)
        }

    @as_tool
    async def update_frontmatter(
        self,
        note_path: str,
        frontmatter_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates the YAML frontmatter of an existing note."""
        path = Path(note_path)
        if not path.exists():
            return {"success": False, "error": "Note not found"}
        
        content = path.read_text(encoding="utf-8")
        
        # Parse existing frontmatter
        fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if fm_match:
            # Update frontmatter
            try:
                import yaml
                existing_fm = yaml.safe_load(fm_match.group(1))
                existing_fm.update(frontmatter_updates)
                new_fm = yaml.dump(existing_fm, default_flow_style=False)
                new_content = f"---\n{new_fm}---\n" + content[fm_match.end():]
            except:
                return {"success": False, "error": "Failed to parse YAML"}
        else:
            # Add new frontmatter
            fm_str = "\n".join([f"{k}: {v}" for k, v in frontmatter_updates.items()])
            new_content = f"---\n{fm_str}\n---\n\n{content}"
        
        path.write_text(new_content, encoding="utf-8")
        return {"success": True, "note_path": str(path)}

    def _parse_code_entities(self, code: str, file_path: str) -> List[CodeEntity]:
        """Parses code to extract documented entities."""
        entities = []
        
        # Simple regex-based parsing for classes and functions
        class_pattern = r"class\s+(\w+)(?:\([^)]*\))?:"
        func_pattern = r"def\s+(\w+)\s*\([^)]*\):"
        
        for match in re.finditer(class_pattern, code):
            entity = CodeEntity(
                name=match.group(1),
                entity_type="class",
                file_path=file_path,
                line_number=code[:match.start()].count("\n") + 1
            )
            entities.append(entity)
            self._entity_registry[entity.name] = entity
        
        for match in re.finditer(func_pattern, code):
            entity = CodeEntity(
                name=match.group(1),
                entity_type="function",
                file_path=file_path,
                line_number=code[:match.start()].count("\n") + 1
            )
            entities.append(entity)
            self._entity_registry[entity.name] = entity
        
        return entities

    async def _generate_file_note(self, target: Path, code: str, entities: List[CodeEntity]) -> VaultNote:
        """Generates a note for a file."""
        entity_links = ", ".join([f"[[{e.name}]]" for e in entities])
        
        prompt = (
            f"Create an Obsidian note for the file: {target.name}\n\n"
            f"Code:\n```python\n{code[:3000]}\n```\n\n"
            f"Entities found: {entity_links}\n\n"
            "Create a comprehensive note that:\n"
            "1. Summarizes the file's purpose\n"
            "2. Lists imports and dependencies using [[wikilinks]]\n"
            "3. Documents the main entities\n"
            "4. Notes usage patterns and examples\n"
            "Use [[wikilinks]] for cross-references. Output ONLY the markdown body (no frontmatter)."
        )
        
        content = await self.improve_content(prompt)
        
        # Extract wikilinks
        wikilinks = set(re.findall(r"\[\[([^\]]+)\]\]", content))
        
        return VaultNote(
            title=target.stem,
            note_type=NoteType.FILE,
            content=content,
            frontmatter={
                "type": "file",
                "path": str(target),
                "language": "python",
                "created": time.strftime("%Y-%m-%d"),
                "tags": ["code", "python", target.stem.lower()]
            },
            wikilinks=wikilinks
        )

    async def _generate_entity_note(self, entity: CodeEntity, code: str) -> VaultNote:
        """Generates a note for a code entity (class/function)."""
        # Extract the entity's code
        pattern = rf"(class|def)\s+{entity.name}.*?(?=\n(?:class|def)\s|\Z)"
        match = re.search(pattern, code, re.DOTALL)
        entity_code = match.group(0)[:1500] if match else ""
        
        prompt = (
            f"Create an Obsidian note for the {entity.entity_type}: {entity.name}\n\n"
            f"Code:\n```python\n{entity_code}\n```\n\n"
            "Create a note that:\n"
            "1. Explains what this {entity.entity_type} does\n"
            "2. Documents parameters/attributes\n"
            "3. Shows usage examples\n"
            "4. Links to related concepts using [[wikilinks]]\n"
            "Output ONLY the markdown body."
        )
        
        content = await self.improve_content(prompt)
        wikilinks = set(re.findall(r"\[\[([^\]]+)\]\]", content))
        
        return VaultNote(
            title=entity.name,
            note_type=NoteType.CLASS if entity.entity_type == "class" else NoteType.FUNCTION,
            content=content,
            frontmatter={
                "type": entity.entity_type,
                "file": entity.file_path,
                "line": entity.line_number,
                "created": time.strftime("%Y-%m-%d"),
                "tags": ["code", entity.entity_type, entity.name.lower()]
            },
            wikilinks=wikilinks
        )

    def _generate_moc(self, name: str, notes: List[str]) -> VaultNote:
        """Generates a Map of Content note."""
        links = "\n".join([f"- [[{Path(n).stem}]]" for n in notes])
        content = f"# {name} - Map of Content\n\n## Notes\n\n{links}\n"
        
        return VaultNote(
            title=f"{name} MOC",
            note_type=NoteType.INDEX,
            content=content,
            frontmatter={
                "type": "moc",
                "created": time.strftime("%Y-%m-%d"),
                "tags": ["moc", "index"]
            }
        )

    def _generate_index_note(self, name: str, results: List[Dict]) -> VaultNote:
        """Generates an index note for a directory."""
        successful = [r for r in results if r.get("success")]
        links = "\n".join([f"- [[{Path(r['file']).stem}]]" for r in successful])
        content = f"# {name} - Code Documentation Index\n\n## Files\n\n{links}\n\n## Statistics\n\n- Total files: {len(results)}\n- Documented: {len(successful)}\n"
        
        return VaultNote(
            title=f"{name} Index",
            note_type=NoteType.INDEX,
            content=content,
            frontmatter={
                "type": "index",
                "created": time.strftime("%Y-%m-%d"),
                "tags": ["index", "documentation"]
            }
        )

    def _save_note(self, note: VaultNote) -> str:
        """Saves a note to the vault."""
        if not self._vault_path:
            return ""
        
        # Build frontmatter
        fm_lines = ["---"]
        for key, value in note.frontmatter.items():
            if isinstance(value, list):
                fm_lines.append(f"{key}: [{', '.join(value)}]")
            else:
                fm_lines.append(f"{key}: {value}")
        fm_lines.append("---\n")
        
        full_content = "\n".join(fm_lines) + note.content
        
        note_path = self._vault_path / f"{note.title}.md"
        note_path.write_text(full_content, encoding="utf-8")
        
        self._note_cache[note.title] = note
        logging.info(f"ObsidianCodeDescriber: Note saved at {note_path}")
        
        return str(note_path)

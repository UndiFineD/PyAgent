# Extracted from: C:\DEV\PyAgent\.external\agentUniverse\agentuniverse\agent\action\knowledge\reader\file\markdown_reader.py
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from pathlib import Path

# @Time    : 2024/8/26 18:11
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: markdown_reader.py
from typing import Dict, List, Optional, Union

from agentuniverse.agent.action.knowledge.reader.reader import Reader
from agentuniverse.agent.action.knowledge.store.document import Document


class MarkdownReader(Reader):
    """Docx reader."""

    def _load_data(self, file: Union[str, Path], ext_info: Optional[Dict] = None) -> List[Document]:
        """Parse the markdown file.

        Note:
            The markdown file cannot be process in pagination.
            `unstructured` and `markdown` is required to read markdown files:
            `pip install unstructured` and `pip install markdown`
        """
        try:
            from langchain_community.document_loaders import UnstructuredMarkdownLoader
        except ImportError:
            raise ImportError(
                "markdown and unstructured is required to read markdown files: "
                "please run `pip install unstructured` and `pip install markdown`"
            )

        if isinstance(file, str):
            file = Path(file)
        data = UnstructuredMarkdownLoader(file).load()
        metadata = {"file_name": file.name}
        if ext_info is not None:
            metadata.update(ext_info)

        return [Document(text=data[0].page_content, metadata=metadata or {})]

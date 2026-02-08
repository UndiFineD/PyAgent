# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pdfalyzer.py\pdfalyzer.py\output.py\tables.py\stream_objects_table_c79a870d1ce0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\pdfalyzer\output\tables\stream_objects_table.py

"""

Build a rich table to show the sizes of embedded streams.

"""

from typing import List

from pdfalyzer.decorators.pdf_tree_node import PdfTreeNode

from rich.table import Table

from yaralyzer.helpers.rich_text_helper import size_in_bytes_text

from yaralyzer.output.file_hashes_table import LEFT


def stream_objects_table(stream_nodes: List[PdfTreeNode]) -> Table:
    """Build a table of stream objects and their lengths."""

    table = Table(
        "Stream Length",
        "Node",
        title=" Embedded Streams",
        title_style="grey",
        title_justify=LEFT,
    )

    table.columns[0].justify = "right"

    for node in stream_nodes:
        table.add_row(size_in_bytes_text(node.stream_length), node.__rich__())

    return table

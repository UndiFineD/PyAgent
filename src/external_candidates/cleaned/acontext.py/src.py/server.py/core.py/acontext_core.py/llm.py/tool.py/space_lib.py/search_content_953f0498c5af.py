# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\llm\tool\space_lib\search_content.py
import json

from ....env import DEFAULT_CORE_CONFIG
from ....schema.block.path_node import repr_path_tree
from ....schema.llm import ToolSchema
from ....schema.orm import Task
from ....schema.orm.block import BLOCK_TYPE_FOLDER, BLOCK_TYPE_PAGE
from ....schema.result import Result
from ....schema.session.task import TaskStatus
from ....schema.utils import asUUID
from ....service.data import block as BD
from ....service.data import block_nav as BN
from ....service.data import block_render as BR
from ....service.data import block_search as BS
from ..base import Tool, ToolPool
from .ctx import SpaceCtx


async def _search_content_handler(
    ctx: SpaceCtx,
    llm_arguments: dict,
) -> Result[str]:
    if "query" not in llm_arguments:
        return Result.resolve("Query for search_path are required")
    query = llm_arguments["query"]
    limit = llm_arguments.get("limit", 10)
    r = await BS.search_content_blocks(
        ctx.db_session,
        ctx.space_id,
        query,
        topk=limit,
        threshold=DEFAULT_CORE_CONFIG.block_embedding_search_cosine_distance_threshold,
    )
    if not r.ok():
        return r
    block_distances = r.data
    display_results = []
    for b, d in block_distances:
        r = await BR.render_content_block(ctx.db_session, ctx.space_id, b)
        if not r.ok():
            return r
        content_block = r.data
        r = await ctx.find_path_by_id(content_block.parent_id)
        if not r.ok():
            return r
        path, _ = r.data
        display_results.append(
            json.dumps(
                {
                    "page_path": path,
                    "block_index": content_block.order + 1,
                    "content": content_block.props,
                },
                ensure_ascii=False,
            )
        )
    display_section = "\n".join(display_results)
    return Result.resolve(f"Found {len(block_distances)} blocks, display in JSON: \n{display_section}")


_search_content_tool = (
    Tool()
    .use_schema(
        ToolSchema(
            function={
                "name": "search_content",
                "description": "Search the content blocks with query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query/keywords/purpose description to search",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Limit the number of results. Default to 10",
                        },
                    },
                    "required": ["query"],
                },
            },
        )
    )
    .use_handler(_search_content_handler)
)

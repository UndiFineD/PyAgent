# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\acontext_core\service\controller\space_sop.py
from ...env import LOG
from ...llm.agent import space_construct as SC
from ...schema.block.sop_block import SOPData
from ...schema.config import ProjectConfig
from ...schema.utils import asUUID


async def process_sop_complete(
    project_config: ProjectConfig,
    project_id: asUUID,
    space_id: asUUID,
    task_id: asUUID,
    sop_data: SOPData,
):
    """
    Process SOP completion and trigger construct agent
    """
    LOG.info(f"Processing SOP completion for task {task_id}")
    # Call construct agent
    construct_result = await SC.space_construct_agent_curd(
        project_id,
        space_id,
        [task_id],
        [sop_data],
        max_iterations=project_config.default_space_construct_agent_max_iterations,
    )

    if construct_result.ok():
        result_data, _ = construct_result.unpack()
        LOG.info(f"Construct agent completed successfully: {result_data}")
    else:
        LOG.error(f"Construct agent failed: {construct_result}")

    return construct_result

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\tests\deps\test_block_reference.py
import pytest
from acontext_core.infra.db import DatabaseClient
from acontext_core.schema.block.sop_block import SOPData, SOPStep
from acontext_core.schema.orm import Block, BlockReference, Project, Space
from acontext_core.service.data.block import create_new_path_block
from acontext_core.service.data.block_write import write_sop_block_to_parent
from acontext_core.service.data.tool import get_tool_names
from sqlalchemy import select
from sqlalchemy.orm import selectinload

FAKE_KEY = "b" * 32


@pytest.mark.asyncio
async def test_block_reference_set_null_on_delete():
    """
    Test that when a referenced block is deleted, the BlockReference record
    persists with reference_block_id set to NULL (not cascade deleted).
    """
    db_client = DatabaseClient()

    # Drop and recreate tables to ensure schema is up-to-date with new SET NULL constraint
    await db_client.create_tables()

    async with db_client.get_session_context() as session:
        try:
            # Create test project and space
            project = Project(secret_key_hmac=FAKE_KEY, secret_key_hash_phc=FAKE_KEY)
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            # Create a page block (will be referenced)
            target_block = Block(
                space_id=space.id,
                type="page",
                title="Target Page",
                props={"description": "This page will be referenced"},
                sort=0,
            )
            session.add(target_block)
            await session.flush()

            # Create a reference block under a parent page
            parent_page = Block(
                space_id=space.id,
                type="page",
                title="Parent Page",
                props={},
                sort=1,
            )
            session.add(parent_page)
            await session.flush()

            reference_block = Block(
                space_id=space.id,
                type="reference",
                parent_id=parent_page.id,
                title="Reference to Target",
                props={},
                sort=0,
            )
            session.add(reference_block)
            await session.flush()

            # Create BlockReference linking reference_block -> target_block
            block_reference = BlockReference(
                block_id=reference_block.id,
                reference_block_id=target_block.id,
            )
            session.add(block_reference)
            await session.commit()

            # Store IDs for later verification
            reference_block_id = reference_block.id
            target_block_id = target_block.id
            block_reference_block_id = block_reference.block_id

            # Verify the relationship is set up correctly before deletion
            result = await session.execute(select(BlockReference).where(BlockReference.block_id == reference_block_id))
            br_before = result.scalar_one()
            assert br_before.reference_block_id == target_block_id
            assert br_before.reference_block_id is not None
            print(f"✓ BlockReference created: {br_before.block_id} -> {br_before.reference_block_id}")

            # Delete the target block (the block being referenced)
            await session.delete(target_block)
            await session.commit()
            session.expire_all()  # Ensure we get fresh data from database
            print(f"✓ Target block deleted: {target_block_id}")

            # Verify that the target block is deleted
            result = await session.execute(select(Block).where(Block.id == target_block_id))
            deleted_block = result.scalar_one_or_none()
            assert deleted_block is None
            print("✓ Target block confirmed deleted from database")

            # Verify that the reference block still exists
            result = await session.execute(select(Block).where(Block.id == reference_block_id))
            existing_reference_block = result.scalar_one_or_none()
            assert existing_reference_block is not None
            assert existing_reference_block.id == reference_block_id
            assert existing_reference_block.type == "reference"
            print(f"✓ Reference block still exists: {existing_reference_block.id}")

            # Verify that the BlockReference still exists but with NULL reference_block_id
            result = await session.execute(
                select(BlockReference).where(BlockReference.block_id == block_reference_block_id)
            )
            br_after = result.scalar_one_or_none()
            assert br_after is not None
            assert br_after.block_id == reference_block_id
            assert br_after.reference_block_id is None  # SET NULL behavior
            print("✓ BlockReference persists with NULL reference_block_id")

            # Verify relationship access
            result = await session.execute(
                select(BlockReference)
                .options(selectinload(BlockReference.reference_block))
                .where(BlockReference.block_id == reference_block_id)
            )
            br_with_rel = result.scalar_one()
            assert br_with_rel.reference_block is None
            print("✓ BlockReference.reference_block is None (broken reference)")

            print("\n✅ All SET NULL behavior tests passed!")
            print("   - Target block deleted")
            print("   - Reference block preserved")
            print("   - BlockReference preserved with NULL reference_block_id")

        finally:
            # Cleanup
            await session.delete(project)
            await session.commit()


@pytest.mark.asyncio
async def test_tool_reference_sop_count():
    """Test that sop_count is correctly calculated"""
    db_client = DatabaseClient()
    await db_client.create_tables()

    async with db_client.get_session_context() as session:
        # Create test project and space
        project = Project(secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash")
        session.add(project)
        await session.flush()

        space = Space(project_id=project.id)
        session.add(space)
        await session.flush()

        # Create parent page for SOP
        r = await create_new_path_block(session, space.id, "Parent Page")
        assert r.ok()
        parent_id = r.data.id

        # Create first SOP with two tools
        sop_data1 = SOPData(
            use_when="First SOP",
            preferences="Test preferences",
            tool_sops=[
                SOPStep(tool_name="tool_a", action="run with debug=true"),
                SOPStep(tool_name="tool_b", action="execute with retries=3"),
            ],
        )

        r = await write_sop_block_to_parent(session, space.id, parent_id, sop_data1)
        assert r.ok()

        # Create second SOP that reuses tool_a and adds tool_c
        sop_data2 = SOPData(
            use_when="Second SOP",
            preferences="More test preferences",
            tool_sops=[
                SOPStep(tool_name="tool_a", action="run with different params"),
                SOPStep(tool_name="tool_c", action="new tool action"),
            ],
        )

        r = await write_sop_block_to_parent(session, space.id, parent_id, sop_data2)
        assert r.ok()

        # Now test get_tool_names to see if sop_count is correct
        r = await get_tool_names(session, project.id)
        assert r.ok()

        tool_data = r.data
        print(f"Found {len(tool_data)} tools:")

        # Convert to dict for easier testing
        tools_by_name = {tool.name: tool for tool in tool_data}

        for tool in tool_data:
            print(f"  {tool.name}: sop_count={tool.sop_count}")

        # Verify counts
        assert "tool_a" in tools_by_name
        assert "tool_b" in tools_by_name
        assert "tool_c" in tools_by_name

        # tool_a should appear in 2 SOPs
        assert tools_by_name["tool_a"].sop_count == 2

        # tool_b and tool_c should each appear in 1 SOP
        assert tools_by_name["tool_b"].sop_count == 1
        assert tools_by_name["tool_c"].sop_count == 1

        print("✅ All tests passed! sop_count is working correctly.")

        # Clean up
        await session.delete(project)

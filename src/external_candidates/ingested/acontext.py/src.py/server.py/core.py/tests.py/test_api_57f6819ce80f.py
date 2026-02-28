# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\tests\test_api.py
"""
FastAPI endpoint tests.

This test module uses two auto-use fixtures to enable testing:
1. mock_lifespan: Prevents the FastAPI app's lifespan from initializing infrastructure
2. mock_get_embedding: Provides deterministic embeddings for predictable search results

Test Strategy:
- Uses httpx.AsyncClient with ASGITransport to test the async ASGI app
- AsyncClient runs the app in the same event loop, avoiding thread/loop conflicts
- Each test creates its own local DatabaseClient for isolation
- The api.DB_CLIENT is patched so the endpoint uses the test's database
- This allows proper async database operations without event loop mismatches
"""

from unittest.mock import patch
from uuid import uuid4

import numpy as np
import pytest
from acontext_core.env import DEFAULT_CORE_CONFIG
from acontext_core.infra.db import DatabaseClient
from acontext_core.schema.embedding import EmbeddingReturn
from acontext_core.schema.orm import (
    Block,
    BlockEmbedding,
    Project,
    Session,
    Space,
    Task,
)
from acontext_core.schema.orm.block import (
    BLOCK_TYPE_PAGE,
    BLOCK_TYPE_SOP,
    BLOCK_TYPE_TEXT,
)
from acontext_core.schema.result import Result
from api import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def mock_lifespan():
    """
    Mock the FastAPI app lifespan to prevent multiple initializations.

    This fixture:
    - Patches setup() and cleanup() to avoid conflicts with test database clients
    - Applies automatically to all tests (autouse=True)
    """

    async def mock_setup():
        pass

    async def mock_cleanup():
        pass

    with (
        patch("api.setup", side_effect=mock_setup),
        patch("api.cleanup", side_effect=mock_cleanup),
        patch("api.MQ_CLIENT.start", side_effect=lambda: None),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_get_embedding():
    """
    Automatically mock get_embedding for all API tests.

    This fixture:
    - Applies automatically to all tests (autouse=True)
    - Returns deterministic embeddings based on text content
    - Allows tests to have predictable search results
    """
    with patch("acontext_core.service.data.block_search.get_embedding") as mock:

        async def get_mock_embedding(texts, phase="document"):
            """Generate deterministic embeddings based on text content"""
            text = texts[0].lower() if texts else ""

            # Create a deterministic embedding based on text content
            base_vector = np.zeros(
                DEFAULT_CORE_CONFIG.block_embedding_dim, dtype=np.float32
            )

            # Set different values based on keywords to create meaningful similarities
            if "python" in text or "programming" in text:
                base_vector[0] = 0.8
                base_vector[1] = 0.2
                base_vector[2] = 0.1
            elif "javascript" in text or "js" in text:
                base_vector[0] = 0.1
                base_vector[1] = 0.8
                base_vector[2] = 0.5
            else:
                # Default random embedding for unknown queries
                base_vector = np.random.rand(
                    DEFAULT_CORE_CONFIG.block_embedding_dim
                ).astype(np.float32)

            mock_embedding_return = EmbeddingReturn(
                embedding=base_vector.reshape(1, -1),
                prompt_tokens=10,
                total_tokens=10,
            )
            return Result.resolve(mock_embedding_return)

        mock.side_effect = get_mock_embedding
        yield mock


class TestSemanticGlobEndpoint:
    """Test the /api/v1/project/{project_id}/space/{space_id}/semantic_glob endpoint"""

    @pytest.mark.asyncio
    async def test_semantic_glob_success(self):
        """Test successful semantic search via API endpoint"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data in a separate session
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            # Create test blocks
            page1 = Block(
                space_id=space.id,
                type=BLOCK_TYPE_PAGE,
                title="Python Programming",
                props={"view_when": "Learn Python basics"},
                sort=0,
            )
            session.add(page1)
            await session.flush()

            page2 = Block(
                space_id=space.id,
                type=BLOCK_TYPE_PAGE,
                title="JavaScript Tutorials",
                props={"view_when": "JavaScript fundamentals"},
                sort=1,
            )
            session.add(page2)
            await session.flush()

            # Create embeddings
            python_embedding = np.zeros(1536, dtype=np.float32)
            python_embedding[0] = 0.8
            python_embedding[1] = 0.2

            embedding1 = BlockEmbedding(
                block_id=page1.id,
                space_id=space.id,
                block_type=page1.type,
                embedding=python_embedding,
                configs={"model": "test"},
            )
            session.add(embedding1)

            js_embedding = np.zeros(1536, dtype=np.float32)
            js_embedding[0] = 0.1
            js_embedding[1] = 0.8

            embedding2 = BlockEmbedding(
                block_id=page2.id,
                space_id=space.id,
                block_type=page2.type,
                embedding=js_embedding,
                configs={"model": "test"},
            )
            session.add(embedding2)

            await session.commit()

            # Store IDs for later use
            project_id = project.id
            space_id = space.id
            page1_id = page1.id

        # Now test the API endpoint with a fresh session (embedding mock is auto-applied via fixture)
        # Patch the global DB_CLIENT to use our test database client
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/space/{space_id}/semantic_glob",
                    params={"query": "Python programming", "limit": 10},
                )

                # Assertions
                assert (
                    response.status_code == 200
                ), f"Expected 200, got {response.status_code}: {response.text}"

                data = response.json()
                assert isinstance(data, list), "Response should be a list"
                assert len(data) > 0, "Should return at least one result"

                # Check response structure
                first_result = data[0]
                assert "block_id" in first_result, "Result should have block_id"
                assert "distance" in first_result, "Result should have distance"
                assert isinstance(
                    first_result["distance"], float
                ), "Distance should be a float"

                # Verify the most relevant result is the Python page
                assert first_result["block_id"] == str(
                    page1_id
                ), "Python page should be most relevant"

                print(f"✓ API test passed - Found {len(data)} results")

        # Cleanup - delete the project (cascades to space, blocks, embeddings)
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_semantic_glob_with_custom_threshold(self):
        """Test semantic search with custom threshold parameter"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data in a separate session
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            page = Block(
                space_id=space.id,
                type=BLOCK_TYPE_PAGE,
                title="Test Page",
                props={"view_when": "Test content"},
                sort=0,
            )
            session.add(page)
            await session.flush()

            # Create embedding
            embedding_vector = np.random.rand(1536).astype(np.float32)
            embedding = BlockEmbedding(
                block_id=page.id,
                space_id=space.id,
                block_type=page.type,
                embedding=embedding_vector,
                configs={"model": "test"},
            )
            session.add(embedding)
            await session.commit()

            # Store IDs for later use
            project_id = project.id
            space_id = space.id

        # Test with custom threshold (embedding mock is auto-applied via fixture)
        # Patch the global DB_CLIENT to use our test database client
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/space/{space_id}/semantic_glob",
                    params={
                        "query": "test query",
                        "limit": 5,
                        "threshold": 0.5,
                    },
                )

                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)

                print("✓ Custom threshold test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_semantic_glob_invalid_space_id(self):
        """Test API with invalid space ID"""
        valid_project_id = str(uuid4())
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Test with non-UUID space_id
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/not-a-uuid/semantic_glob",
                params={"query": "test"},
            )

            # FastAPI should return 422 for invalid UUID format
            assert response.status_code == 422
            print("✓ Invalid space ID test passed")

    @pytest.mark.asyncio
    async def test_semantic_glob_invalid_params(self):
        """Test API with invalid query parameters"""
        valid_project_id = str(uuid4())
        valid_space_id = str(uuid4())

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Test without required query parameter
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_glob"
            )
            assert response.status_code == 422, "Should fail without query parameter"

            # Test with limit out of range
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_glob",
                params={"query": "test", "limit": 100},  # Max is 50
            )
            assert response.status_code == 422, "Should fail with limit > 50"

            # Test with negative limit
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_glob",
                params={"query": "test", "limit": -1},
            )
            assert response.status_code == 422, "Should fail with negative limit"

            # Test with threshold out of range
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_glob",
                params={"query": "test", "threshold": 3.0},  # Max is 2.0
            )
            assert response.status_code == 422, "Should fail with threshold > 2.0"

            print("✓ Invalid params test passed")


class TestSemanticGrepEndpoint:
    """Test the /api/v1/project/{project_id}/space/{space_id}/semantic_grep endpoint"""

    @pytest.mark.asyncio
    async def test_semantic_grep_success(self):
        """Test successful semantic search for content blocks via API endpoint"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data in a separate session
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            # Create a parent page for content blocks
            page = Block(
                space_id=space.id,
                type=BLOCK_TYPE_PAGE,
                title="Documentation",
                props={},
                sort=0,
            )
            session.add(page)
            await session.flush()

            # Create test content blocks
            text1 = Block(
                space_id=space.id,
                type=BLOCK_TYPE_TEXT,
                parent_id=page.id,
                title="Python Tutorial Content",
                props={"content": "Learn Python programming basics"},
                sort=0,
            )
            session.add(text1)
            await session.flush()

            text2 = Block(
                space_id=space.id,
                type=BLOCK_TYPE_TEXT,
                parent_id=page.id,
                title="JavaScript Guide Content",
                props={"content": "JavaScript fundamentals and best practices"},
                sort=1,
            )
            session.add(text2)
            await session.flush()

            # Create embeddings for content blocks
            python_embedding = np.zeros(1536, dtype=np.float32)
            python_embedding[0] = 0.8
            python_embedding[1] = 0.2

            embedding1 = BlockEmbedding(
                block_id=text1.id,
                space_id=space.id,
                block_type=text1.type,
                embedding=python_embedding,
                configs={"model": "test"},
            )
            session.add(embedding1)

            js_embedding = np.zeros(1536, dtype=np.float32)
            js_embedding[0] = 0.1
            js_embedding[1] = 0.8

            embedding2 = BlockEmbedding(
                block_id=text2.id,
                space_id=space.id,
                block_type=text2.type,
                embedding=js_embedding,
                configs={"model": "test"},
            )
            session.add(embedding2)

            await session.commit()

            # Store IDs for later use
            project_id = project.id
            space_id = space.id
            text1_id = text1.id

        # Now test the API endpoint (embedding mock is auto-applied via fixture)
        # Patch the global DB_CLIENT to use our test database client
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/space/{space_id}/semantic_grep",
                    params={"query": "Python programming", "limit": 10},
                )

                # Assertions
                assert (
                    response.status_code == 200
                ), f"Expected 200, got {response.status_code}: {response.text}"

                data = response.json()
                assert isinstance(data, list), "Response should be a list"
                assert len(data) > 0, "Should return at least one result"

                # Check response structure
                first_result = data[0]
                assert "block_id" in first_result, "Result should have block_id"
                assert "distance" in first_result, "Result should have distance"
                assert isinstance(
                    first_result["distance"], float
                ), "Distance should be a float"

                # Verify the most relevant result is the Python text block
                assert first_result["block_id"] == str(
                    text1_id
                ), "Python content block should be most relevant"

                print(f"✓ API test passed - Found {len(data)} results")

        # Cleanup - delete the project (cascades to space, blocks, embeddings)
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_semantic_grep_with_sop_blocks(self):
        """Test semantic search includes SOP blocks"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data with SOP blocks
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            # Create a parent page
            page = Block(
                space_id=space.id,
                type=BLOCK_TYPE_PAGE,
                title="Procedures",
                props={},
                sort=0,
            )
            session.add(page)
            await session.flush()

            # Create SOP block
            sop = Block(
                space_id=space.id,
                type=BLOCK_TYPE_SOP,
                parent_id=page.id,
                title="Deployment SOP",
                props={"content": "Standard operating procedure for deployment"},
                sort=0,
            )
            session.add(sop)
            await session.flush()

            # Create embedding
            sop_embedding = np.random.rand(1536).astype(np.float32)
            embedding = BlockEmbedding(
                block_id=sop.id,
                space_id=space.id,
                block_type=sop.type,
                embedding=sop_embedding,
                configs={"model": "test"},
            )
            session.add(embedding)
            await session.commit()

            # Store IDs for later use
            project_id = project.id
            space_id = space.id

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/space/{space_id}/semantic_grep",
                    params={"query": "deployment procedure", "limit": 10},
                )

                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, list)

                print("✓ SOP block search test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_semantic_grep_invalid_space_id(self):
        """Test API with invalid space ID"""
        valid_project_id = str(uuid4())
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Test with non-UUID space_id
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/not-a-uuid/semantic_grep",
                params={"query": "test"},
            )

            # FastAPI should return 422 for invalid UUID format
            assert response.status_code == 422
            print("✓ Invalid space ID test passed")

    @pytest.mark.asyncio
    async def test_semantic_grep_invalid_params(self):
        """Test API with invalid query parameters"""
        valid_project_id = str(uuid4())
        valid_space_id = str(uuid4())

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Test without required query parameter
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_grep"
            )
            assert response.status_code == 422, "Should fail without query parameter"

            # Test with limit out of range
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_grep",
                params={"query": "test", "limit": 100},  # Max is 50
            )
            assert response.status_code == 422, "Should fail with limit > 50"

            # Test with negative limit
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_grep",
                params={"query": "test", "limit": -1},
            )
            assert response.status_code == 422, "Should fail with negative limit"

            # Test with threshold out of range
            response = await client.get(
                f"/api/v1/project/{valid_project_id}/space/{valid_space_id}/semantic_grep",
                params={"query": "test", "threshold": 3.0},  # Max is 2.0
            )
            assert response.status_code == 422, "Should fail with threshold > 2.0"

            print("✓ Invalid params test passed")


class TestGetLearningStatusEndpoint:
    """Test the /api/v1/project/{project_id}/session/{session_id}/get_learning_status endpoint"""

    @pytest.mark.asyncio
    async def test_get_learning_status_with_digested_tasks(self):
        """Test learning status with space digested and non-digested tasks"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac", secret_key_hash_phc="test_key_hash"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            test_session = Session(project_id=project.id, space_id=space.id)
            session.add(test_session)
            await session.flush()

            # Create tasks with different space_digested status
            task1 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=1,
                data={"task_description": "Task 1"},
                status="success",
                space_digested=True,
            )
            task2 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=2,
                data={"task_description": "Task 2"},
                status="success",
                space_digested=True,
            )
            task3 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=3,
                data={"task_description": "Task 3"},
                status="success",
                space_digested=False,
            )
            session.add_all([task1, task2, task3])
            await session.commit()

            project_id = project.id
            session_id = test_session.id

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/session/{session_id}/get_learning_status"
                )

                assert response.status_code == 200
                data = response.json()
                assert "space_digested_count" in data
                assert "not_space_digested_count" in data
                assert data["space_digested_count"] == 2
                assert data["not_space_digested_count"] == 1

                print("✓ Learning status with digested tasks test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_get_learning_status_no_tasks(self):
        """Test learning status when session has no tasks"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac2", secret_key_hash_phc="test_key_hash2"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            test_session = Session(project_id=project.id, space_id=space.id)
            session.add(test_session)
            await session.commit()

            project_id = project.id
            session_id = test_session.id

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/session/{session_id}/get_learning_status"
                )

                assert response.status_code == 200
                data = response.json()
                assert data["space_digested_count"] == 0
                assert data["not_space_digested_count"] == 0

                print("✓ Learning status with no tasks test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_get_learning_status_session_not_connected_to_space(self):
        """Test learning status when session is not connected to a space"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac3", secret_key_hash_phc="test_key_hash3"
            )
            session.add(project)
            await session.flush()

            # Create session without space_id
            test_session = Session(project_id=project.id, space_id=None)
            session.add(test_session)
            await session.flush()

            # Create some tasks anyway
            task1 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=1,
                data={"task_description": "Task 1"},
                status="success",
                space_digested=True,
            )
            task2 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=2,
                data={"task_description": "Task 2"},
                status="pending",
                space_digested=False,
            )
            session.add_all([task1, task2])
            await session.commit()

            project_id = project.id
            session_id = test_session.id

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/session/{session_id}/get_learning_status"
                )

                assert response.status_code == 200
                data = response.json()
                # Should return 0 and 0 when session is not connected to space
                assert data["space_digested_count"] == 0
                assert data["not_space_digested_count"] == 0

                print(
                    "✓ Learning status for session not connected to space test passed"
                )

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_get_learning_status_invalid_session_id(self):
        """Test learning status with invalid session ID"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac4", secret_key_hash_phc="test_key_hash4"
            )
            session.add(project)
            await session.commit()

            project_id = project.id
            invalid_session_id = str(uuid4())

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/session/{invalid_session_id}/get_learning_status"
                )

                # Should return 404 for non-existent session
                assert response.status_code == 404

                print("✓ Invalid session ID test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

    @pytest.mark.asyncio
    async def test_get_learning_status_all_digested(self):
        """Test learning status when all tasks are space digested"""
        db_client = DatabaseClient()
        await db_client.create_tables()

        # Create test data
        async with db_client.get_session_context() as session:
            project = Project(
                secret_key_hmac="test_key_hmac5", secret_key_hash_phc="test_key_hash5"
            )
            session.add(project)
            await session.flush()

            space = Space(project_id=project.id)
            session.add(space)
            await session.flush()

            test_session = Session(project_id=project.id, space_id=space.id)
            session.add(test_session)
            await session.flush()

            # Create all digested tasks
            task1 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=1,
                data={"task_description": "Task 1"},
                status="success",
                space_digested=True,
            )
            task2 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=2,
                data={"task_description": "Task 2"},
                status="success",
                space_digested=True,
            )
            task3 = Task(
                project_id=project.id,
                session_id=test_session.id,
                order=3,
                data={"task_description": "Task 3"},
                status="success",
                space_digested=True,
            )
            session.add_all([task1, task2, task3])
            await session.commit()

            project_id = project.id
            session_id = test_session.id

        # Test the API endpoint
        with patch("api.DB_CLIENT", db_client):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(
                    f"/api/v1/project/{project_id}/session/{session_id}/get_learning_status"
                )

                assert response.status_code == 200
                data = response.json()
                assert data["space_digested_count"] == 3
                assert data["not_space_digested_count"] == 0

                print("✓ All tasks digested test passed")

        # Cleanup
        async with db_client.get_session_context() as session:
            project = await session.get(Project, project_id)
            await session.delete(project)
            await session.commit()

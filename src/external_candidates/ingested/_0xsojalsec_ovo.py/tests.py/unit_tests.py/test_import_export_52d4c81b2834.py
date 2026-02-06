# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\test_import_export.py
import os
import tempfile
import zipfile

import pytest
from ovo import (
    Design,
    DesignJob,
    DesignSpec,
    Pool,
    Project,
    Round,
    db,
    storage,
)
from ovo.core.database.models_rfdiffusion import (
    RFdiffusionParams,
    RFdiffusionScaffoldDesignWorkflow,
)
from ovo.core.logic.import_export_logic import export_project, import_project


def test_export_import_cycle(example_pdb_path):
    """Test that export and import work together correctly"""

    # Create a test project with some data
    test_project = Project(
        id="test_export_import_project",
        name="Test Export Import Project",
        author="test_user",
        public=False,
    )
    db.save(test_project)

    # Create a round
    test_round = Round(
        id="test_export_import_round",
        project_id=test_project.id,
        name="Test Round",
        author="test_user",
    )
    db.save(test_round)

    input_pdb_path = storage.store_file_path(
        example_pdb_path, "project/inputs/test.pdb"
    )
    test_design_job = DesignJob(
        id="test_export_import_design_job",
        author="test_user",
        scheduler_key="test",
        job_id="test_id",
        workflow=RFdiffusionScaffoldDesignWorkflow(
            rfdiffusion_params=RFdiffusionParams(input_pdb_paths=[input_pdb_path])
        ),
    )
    db.save(test_design_job)
    assert os.path.exists(os.path.join(storage.storage_root, input_pdb_path))

    # Create a pool
    test_pool = Pool(
        id="teip",
        round_id=test_round.id,
        name="Test Pool",
        author="test_user",
        design_job_id=test_design_job.id,
    )
    db.save(test_pool)

    with open(example_pdb_path) as f:
        test_design = Design.from_pdb_file(
            storage=storage,
            filename="5ELI_A.pdb",
            pdb_str=f.read(),
            chains=["A"],
            project_id=test_project.id,
            pool_id=test_pool.id,
        )
        db.save(test_design)
        assert len(test_design.spec.chains) == 1
        assert os.path.exists(
            os.path.join(storage.storage_root, test_design.structure_path)
        )

    try:
        # Export the project
        export_zip_path = export_project(test_project.id)

        # Verify the ZIP file was created
        assert os.path.exists(export_zip_path)
        assert zipfile.is_zipfile(export_zip_path)

        # Delete the original data
        db.remove(Pool, test_pool.id)
        db.remove(Round, test_round.id)
        db.remove(Project, test_project.id)
        db.remove(Design, test_design.id)
        db.remove(DesignJob, test_design_job.id)
        # Remove pdb file
        os.unlink(os.path.join(storage.storage_root, test_design.structure_path))
        os.unlink(os.path.join(storage.storage_root, input_pdb_path))
        assert not db.count(Project, id=test_project.id), "Project should be deleted"
        assert not db.count(Design, id=test_design.id), "Design should be deleted"

        # Extract ZIP file
        with tempfile.TemporaryDirectory() as temp_root:
            with zipfile.ZipFile(export_zip_path, "r") as zipf:
                zipf.extractall(temp_root)

            paths = os.listdir(temp_root)
            assert (
                len(paths) == 1
            ), "There should be one top-level directory in the export, got: " + str(
                paths
            )
            temp_dir = os.path.join(temp_root, paths[0])

            # Remove zip file
            os.unlink(export_zip_path)

            counts = import_project(temp_dir, count_only=True)
            assert counts.get("project") == 1
            assert counts.get("round") == 1
            assert counts.get("pool") == 1
            assert not db.count(
                Project, id=test_project.id
            ), "Project should still be deleted"

            # Import the data
            counts = import_project(temp_dir, test_project.id)

        # Verify the data was imported correctly
        imported_project = db.get(Project, test_project.id)
        assert imported_project.name == "Test Export Import Project"
        assert imported_project.author == "test_user"
        assert (
            imported_project.public == True
        ), "Project should become public upon export"

        imported_round = db.get(Round, test_round.id)
        assert imported_round.name == "Test Round"
        assert imported_round.project_id == test_project.id

        imported_pool = db.get(Pool, test_pool.id)
        assert imported_pool.name == "Test Pool"
        assert imported_pool.round_id == test_round.id

        imported_design = db.get(Design, test_design.id)
        assert len(imported_design.spec.chains) == 1
        assert os.path.exists(
            os.path.join(storage.storage_root, imported_design.structure_path)
        )

        imported_design_job = db.get(DesignJob, test_design_job.id)
        assert os.path.exists(
            os.path.join(storage.storage_root, input_pdb_path)
        ), "Path referenced inside Workflow dataclass should also be copied"

        # Verify import results
        assert counts["project"] == 1
        assert counts["round"] == 1
        assert counts["pool"] == 1

    finally:
        # Clean up export file
        if "export_zip_path" in locals() and os.path.exists(export_zip_path):
            os.unlink(export_zip_path)


def test_export_import_with_missing_storage_files():
    """Test export behavior when storage files are missing"""

    # Create a project with a design that references a non-existent file
    project = Project(
        id="test_missing_storage_project",
        name="Test Missing Storage Project",
        author="test_user",
        public=False,
    )
    db.save(project)

    round_obj = Round(
        id="test_missing_storage_round",
        project_id=project.id,
        name="Test Round",
        author="test_user",
    )
    db.save(round_obj)

    pool = Pool(id="tmsp", round_id=round_obj.id, name="Test Pool", author="test_user")
    db.save(pool)

    # Create a design with a non-existent PDB file
    design = Design(
        id=f"ovo_{pool.id}_test_missing_storage_design",
        pool_id=pool.id,
        structure_path="non_existent_file.pdb",  # This file doesn't exist
        spec=DesignSpec(chains=[]),  # Required field with proper structure
    )
    db.save(design)

    # Export should raise an error for missing files
    with pytest.raises(
        FileNotFoundError, match="No such file or directory:.*non_existent_file.pdb"
    ):
        export_project(project.id)


def test_import_id_conflicts():
    """Test that import fails when IDs already exist"""

    # Create a test project
    test_project = Project(
        id="test_conflict_project",
        name="Test Conflict Project",
        author="test_user",
        public=False,
    )
    db.save(test_project)

    # Export the project
    export_zip_path = export_project(test_project.id)

    try:
        # Attempt to import while the project still exists (should fail)
        with pytest.raises(
            ValueError,
            match="Project already exists in the database: Test Conflict Project .*",
        ):
            with tempfile.TemporaryDirectory() as temp_root:
                with zipfile.ZipFile(export_zip_path, "r") as zipf:
                    zipf.extractall(temp_root)
                    paths = os.listdir(temp_root)
                    assert len(paths) == 1, (
                        "There should be one top-level directory in the export, got: "
                        + str(paths)
                    )
                    temp_dir = os.path.join(temp_root, paths[0])
                    import_project(temp_dir, test_project.id)

    finally:
        # Clean up export file
        if os.path.exists(export_zip_path):
            os.unlink(export_zip_path)

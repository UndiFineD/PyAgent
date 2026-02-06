# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\test_app_binder_design.py
import logging

import pytest
from ovo.core.database.models_rfdiffusion import ProteinMPNNParams
from pytest_mock import MockerFixture

from tests.unit_tests.utils import asserts
from tests.unit_tests.utils.constants import BINDER_DESIGN_FILE, TIMEOUT
from tests.unit_tests.utils.mocking import mock_molstar
from tests.unit_tests.utils.rfdiffusion_utils import (
    get_contig,
    preview_tab_binder_design,
    review_and_submit_tab,
    settings_tab,
    trim_tab,
)

logger = logging.getLogger(__name__)

page_key = BINDER_DESIGN_FILE


class TestBinderDesign:
    """Binder design page tests."""

    @pytest.mark.parametrize(
        "test_wrapper",
        [BINDER_DESIGN_FILE],
        indirect=True,
    )
    def test_default_values(
        self, mocker: MockerFixture, test_wrapper, mock_scheduler
    ) -> None:
        """
        Test the binder design workflow with default values.
        This test simulates the manipulation of different tabs in the app,
        using default values to verify the integrity of the workflow
        and ensure that expected outcomes are produced.
        """
        at = test_wrapper
        at.run(timeout=TIMEOUT)

        # Intro tab — skip
        at.button("next_button_top").click().run(timeout=TIMEOUT)

        # Input tab
        logger.info("Testing input tab...")
        at.text_input("input_pdb_code").set_value("1myj").run(timeout=TIMEOUT)
        workflow = at.session_state.workflows[page_key]
        asserts.assert_true(
            workflow.rfdiffusion_params.input_pdb,
            "Verify that the pdb code was registered.",
        )
        asserts.assert_no_error_on_page(at, "input tab")

        # Selection tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        with mock_molstar(
            {
                "sequenceSelections": [{"chainId": "A", "residues": [11, 12, 13]}],
            }
        )(mocker):
            logger.info("Testing selection tab...")
            at.run()
            asserts.assert_no_error_on_page(at, "selection tab")

            workflow = at.session_state.workflows[page_key]
            assert workflow.rfdiffusion_params.hotspots == "A11,A12,A13"

        # Trim tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        logger.info("Testing trim tab...")
        at.selectbox("target_chain").set_value("A").run()
        assert at.number_input(f"start_trim_residue_A").value == 1
        assert at.number_input(f"end_trim_residue_A").value == 153
        asserts.assert_no_error_on_page(at, "trim tab")

        at.number_input(f"start_trim_residue_A").set_value(10).run()
        at.number_input(f"end_trim_residue_A").set_value(100).run()
        asserts.assert_no_error_on_page(at, "trim tab")

        # Preview tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        assert at.text_input("hotspots").value == "A11,A12,A13"
        at.text_input("binder_length").set_value("20-40").run()
        assert at.text_input("binder_length").value == "20-40"
        asserts.assert_no_error_on_page(at, "preview tab")

        # Submission tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        pool_name = "test binder design default values"
        settings_tab(
            at,
            page_key,
            pool_name,
            contig="A10-100/0 20-40",
            hotspot_residues="A11,A12,A13",
        )

        seq_method = at.radio("seq_design_method")
        assert seq_method.value == "ligandmpnn"

        num_sequences = at.number_input("num_sequences")
        assert (
            num_sequences.value == ProteinMPNNParams().num_sequences
        )  # as per ProteinMPNNParams default
        assert workflow.protein_mpnn_params.num_sequences == num_sequences.value

        seq_method.set_value("fastrelax").run()
        num_fastrelax_cycles = at.number_input("fastrelax_cycles")
        assert num_fastrelax_cycles.value == 3
        assert (
            workflow.protein_mpnn_params.fastrelax_cycles == num_fastrelax_cycles.value
        )
        assert (
            workflow.protein_mpnn_params.num_sequences == 1
        ), "num_sequences should be automatically set to 1 for fastrelax"

        # Confirmation tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        review_and_submit_tab(at, mock_scheduler, pool_name)

    @pytest.mark.parametrize(
        "test_wrapper",
        [BINDER_DESIGN_FILE],
        indirect=True,
    )
    def test_alternative_values(
        self, mocker: MockerFixture, test_wrapper, mock_scheduler
    ) -> None:
        """
        Test the binder design workflow with alternative values.

        This test simulates the manipulation of different tabs in the app,
        using alternative values to verify the integrity of the workflow
        and ensure that expected outcomes are produced.
        """
        at = test_wrapper
        at.run(timeout=TIMEOUT)

        # Intro tab — skip
        at.button("next_button_top").click().run(timeout=TIMEOUT)

        # Input tab
        logger.info("Testing input tab...")
        at.text_input("input_pdb_code").set_value("7k7h").run(timeout=TIMEOUT)
        workflow = at.session_state.workflows[page_key]
        asserts.assert_true(
            workflow.rfdiffusion_params.input_pdb,
            "Verify that the pdb code was registered.",
        )
        asserts.assert_no_error_on_page(at, "input tab")

        # Selection tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        with mock_molstar(
            {
                "sequenceSelections": [
                    {"chainId": "D", "residues": [75, 76, 77, 78, 79, 80]}
                ],
            }
        )(mocker):
            logger.info("Testing selection tab...")
            at.run()
            asserts.assert_no_error_on_page(at, "selection tab")

            workflow = at.session_state.workflows[page_key]
            assert workflow.rfdiffusion_params.hotspots == "D75,D76,D77,D78,D79,D80"

        # Trim tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        start = 70
        end = 85
        target_chain = "D"
        trim_tab(at, start=start, end=end, target_chain=target_chain)
        binder_length = "15-15"
        preview_tab_binder_design(
            at,
            binder_length=binder_length,
        )
        contig = get_contig(target_chain, start, end, binder_length)

        # Submission tab
        pool_name = "test binder design alt values"
        settings_tab(
            at,
            page_key,
            pool_name,
            contig=contig,
            hotspot_residues="D75,D76,D77,D78,D79,D80",
        )

        # Confirmation tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        review_and_submit_tab(at, mock_scheduler, pool_name)

    @pytest.mark.parametrize(
        "test_wrapper",
        [BINDER_DESIGN_FILE],
        indirect=True,
    )
    def test_invoke_errors(self, mocker: MockerFixture, test_wrapper) -> None:
        """
        Test invoking errors by providing invalid trim values.

        This test simulates the manipulation of the trim tab with invalid start
        and end values to ensure that appropriate errors are thrown and handled.
        """
        at = test_wrapper
        at.run(timeout=TIMEOUT)

        # Intro tab — skip
        at.button("next_button_top").click().run(timeout=TIMEOUT)

        # Input tab
        logger.info("Testing input tab...")
        at.text_input("input_pdb_code").set_value("1myj").run(timeout=TIMEOUT)
        workflow = at.session_state.workflows[page_key]
        asserts.assert_true(
            workflow.rfdiffusion_params.input_pdb,
            "Verify that the pdb code was registered.",
        )
        asserts.assert_no_error_on_page(at, "input tab")

        # Selection tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        with mock_molstar(
            {
                "sequenceSelections": [{"chainId": "A", "residues": [11, 12, 13]}],
            }
        )(mocker):
            logger.info("Testing selection tab...")
            at.run()
            asserts.assert_no_error_on_page(at, "selection tab")

            workflow = at.session_state.workflows[page_key]
            assert workflow.rfdiffusion_params.hotspots == "A11,A12,A13"

        # Trim tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        for start, end in [(10, 20), (3, 2), (150, 140)]:
            try:
                trim_tab(at, start=start, end=end, go_to_next=False)
                asserts.assert_true(
                    False,
                    "Test, that setting start %s and end %s throws an error"
                    % (start, end),
                )
            except AssertionError:
                asserts.assert_true(
                    True,
                    "Test, that setting start %s and end %s throws an error"
                    % (start, end),
                )

    @pytest.mark.parametrize(
        "test_wrapper",
        [BINDER_DESIGN_FILE],
        indirect=True,
    )
    def test_returning_back(
        self, mocker: MockerFixture, test_wrapper, mock_scheduler
    ) -> None:
        """
        Test navigating back in the binder design workflow.

        This test simulates navigating back to previous steps
        in the binder design workflow to verify that the input
        values are correctly retained and the workflow functions
        correctly.
        """
        at = test_wrapper
        at.run(timeout=TIMEOUT)

        # Intro tab — skip
        at.button("next_button_top").click().run(timeout=TIMEOUT)

        # Input tab
        logger.info("Testing input tab...")
        at.text_input("input_pdb_code").set_value("1myj").run(timeout=TIMEOUT)
        workflow = at.session_state.workflows[page_key]
        asserts.assert_true(
            workflow.rfdiffusion_params.input_pdb,
            "Verify that the pdb code was registered.",
        )
        asserts.assert_no_error_on_page(at, "input tab")

        # Selection tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        with mock_molstar(
            {
                "sequenceSelections": [
                    {"chainId": "A", "residues": [10, 11, 12, 13, 14, 15, 16, 17]}
                ],
            }
        )(mocker):
            logger.info("Testing selection tab...")
            at.run()
            asserts.assert_no_error_on_page(at, "selection tab")

            workflow = at.session_state.workflows[page_key]
            assert (
                workflow.rfdiffusion_params.hotspots
                == "A10,A11,A12,A13,A14,A15,A16,A17"
            )

        # Trim tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        trim_tab(at)
        preview_tab_binder_design(at)
        at.button("back_button_top").click().run()
        at.button("back_button_top").click().run()
        start = 3
        end = 77
        target_chain, _, _ = trim_tab(at, start=start, end=end)
        binder_length = "15-15"
        hotspot_residues = "A10,A11,A12,A13,A14,A15,A16,A17"
        preview_tab_binder_design(
            at,
            binder_length=binder_length,
            hotspot_residues=hotspot_residues,
        )
        contig = get_contig(target_chain, start, end, binder_length)
        pool_name = "test binder design return back"

        # Submission tab
        settings_tab(
            at,
            page_key,
            pool_name,
            contig=contig,
            hotspot_residues=hotspot_residues,
        )

        # Confirmation tab
        at.button("next_button_top").click().run(timeout=TIMEOUT)
        review_and_submit_tab(at, mock_scheduler, pool_name)

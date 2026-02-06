# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\pages\jobs\design_job_detail.py
from datetime import datetime

import streamlit as st
from ovo import Design, DesignWorkflow, Pool, WorkflowTypes, db, get_scheduler
from ovo.app.components.acceptance_thresholds_components import (
    accept_designs_dialog,
    display_current_thresholds,
    filter_designs_by_thresholds_cached,
    thresholds_and_histograms_component,
)
from ovo.app.components.custom_elements import confirm_download_button
from ovo.app.components.descriptor_job_components import refresh_descriptors
from ovo.app.components.descriptor_scatterplot import (
    descriptor_scatterplot_input_component,
    descriptor_scatterplot_pool_details_component,
)
from ovo.app.components.download_component import download_job_designs_component
from ovo.app.utils.cached_db import (
    get_cached_design,
    get_cached_design_job,
    get_cached_pool,
    get_cached_pools,
)
from ovo.core.database import DesignJob, UnknownWorkflow
from ovo.core.logic.design_logic import get_workflows_table, process_results
from ovo.core.logic.job_logic import update_job_status
from streamlit_timeago import time_ago


@st.fragment
def design_job_detail(pool_ids):
    pools = get_cached_pools(pool_ids)
    pools_by_design_job = {
        pool.design_job_id: pool for pool in pools if pool.design_job_id
    }

    design_job_ids = [pool.design_job_id for pool in pools if pool.design_job_id]
    if not design_job_ids:
        st.warning("Selected pools are not associated with a design job")
        return

    design_jobs = db.select(DesignJob, id__in=design_job_ids)

    status_icon = (
        ""
        if all(j.job_result for j in design_jobs)
        else ("⚠️" if any(j.job_result is False for j in design_jobs) else "⏳")
    )
    if len(pools) == 1:
        pool = pools[0]
        st.title(f"{status_icon} {pool.name}")

        left_col, right_col = st.columns([0.85, 0.15], vertical_alignment="center")
        with left_col:
            if pool.description:
                st.write(pool.description)
    else:
        st.title(f"{status_icon} {len(pools)} pools")
        st.markdown("#### " + ", ".join([pool.name for pool in pools]))

    st.subheader("Workflow parameters")
    table = get_workflows_table(jobs=design_jobs)
    table.index = [pools_by_design_job[j.id].id for j in design_jobs]
    st.dataframe(table)

    for job in design_jobs:
        pool = pools_by_design_job[job.id]
        if job.workflow and job.workflow.is_instance(UnknownWorkflow):
            st.warning(
                f"Pool '{pool.id}' workflow failed to load: {job.workflow.error}"
            )
            with st.expander("Raw data"):
                st.json(job.workflow.data)
        if job.job_result is None:
            with st.spinner(f'Checking status of "{pool.name}"'):
                job_result = update_job_status(job)
            if job_result is True and not pool.processed:
                with st.spinner(
                    "Workflow finished, processing designs. This will take a moment..."
                ):
                    progress_bar = st.progress(0)
                    process_results(job, callback=progress_bar.progress, wait=False)
                    progress_bar.empty()
                if job.job_result:
                    st.success(f"Workflow finished: {pool.name}")

        if job.job_result is None:
            scheduler = get_scheduler(job.scheduler_key)
            status_label = scheduler.get_status_label(job.job_id)
            st.info(f"Workflow is {status_label}: {pool.name}")
        elif job.job_result == False:
            st.error(f"Workflow failed: {pool.name}")

        if job.warnings:
            st.write(
                (
                    "1 warning"
                    if len(job.warnings) == 1
                    else f"{len(job.warnings)} warnings"
                )
                + f" found for pool {pool.name}:"
            )
            for warning in job.warnings:
                st.warning(warning)

        # Show log automatically when in progress or failed
        if job.job_result != True:
            args = {}
            if len(pools) == 1 and job.job_result == False:
                args["expanded"] = True
            with st.expander("Log output", **args):
                with st.container(height=400):
                    scheduler = get_scheduler(job.scheduler_key)
                    st.code(scheduler.get_log(job.job_id))

    num_pools_failed = sum(job.job_result == False for job in design_jobs)
    num_pools_in_progress = sum(job.job_result is None for job in design_jobs)

    if len(pools) == num_pools_failed:
        # All pools failed, nothing to show
        return

    if num_pools_in_progress:
        st.button(":material/refresh: Refresh", key="refresh_details_page")
        time_ago(datetime.now(), prefix="Refreshed", key="refreshed")
        if len(pools) == num_pools_in_progress:
            # All pools are in progress, nothing to show yet
            return
        if num_pools_in_progress:
            st.info(
                f"Not including results of {num_pools_in_progress} ongoing workflow"
                + ("s" if num_pools_in_progress > 1 else "")
            )

    all_design_ids = sorted(db.select_unique_values(Design, "id", pool_id__in=pool_ids))

    refresh_descriptors(
        design_ids=all_design_ids,
    )

    scatterplot_fragment(
        all_design_ids=all_design_ids,
        pools=pools,
        jobs=design_jobs,
    )


@st.fragment
def scatterplot_fragment(
    all_design_ids: list[str], pools: list[Pool], jobs: list[DesignJob]
):
    # Get dictionary of saved thresholds (descriptor key -> (min, max) or None)
    saved_thresholds = {}
    inconsistent_threshold_keys = set()
    workflows = [job.workflow for job in jobs]
    for workflow in workflows:
        if (
            not hasattr(workflow, "acceptance_thresholds")
            or not workflow.acceptance_thresholds
        ):
            continue
        for descriptor_key, thresholds in workflow.acceptance_thresholds.items():
            if descriptor_key not in saved_thresholds:
                saved_thresholds[descriptor_key] = thresholds
            elif saved_thresholds[descriptor_key] != thresholds:
                st.warning(
                    f"Looking at multiple workflows with different thresholds for {descriptor_key}, showing the first one"
                )
                inconsistent_threshold_keys.add(descriptor_key)

    # Save selected_thresholds into session state when first opening the page
    pool_ids_str = ",".join(p.id for p in pools)
    if (
        "selected_thresholds" not in st.session_state
        or st.session_state.selected_thresholds_pool_ids != pool_ids_str
    ):
        st.session_state.selected_thresholds = saved_thresholds
        st.session_state.selected_thresholds_pool_ids = pool_ids_str

    show_mode = st.segmented_control(
        "Show",
        options=["Accepted designs", "All designs"],
        key="show_designs",
        default=st.query_params.get("show", "Accepted designs"),
    )

    if show_mode == "Accepted designs":
        accepted_design_ids = db.select_values(
            Design, "id", id__in=all_design_ids, accepted=True
        )

        if st.session_state.selected_thresholds != saved_thresholds:
            st.header("Editing thresholds")
        elif accepted_design_ids:
            st.header(
                f"Showing {len(accepted_design_ids)} accepted {'designs' if len(accepted_design_ids) > 1 else 'design'}"
            )
        else:
            st.header("No accepted designs")
            st.warning("""
                None of the designs met the acceptance thresholds. 
                You may adjust to less strict thresholds below, or try submitting more designs.
                
                To see all generated designs, select 'All designs' above.
                """)

        new_accepted_design_ids, num_accepted_by_descriptor = (
            filter_designs_by_thresholds_cached(
                all_design_ids=all_design_ids,
                thresholds=st.session_state.selected_thresholds,
            )
        )

        if st.session_state.selected_thresholds != saved_thresholds:
            st.write(
                f"Accepted designs based on new thresholds: **{len(new_accepted_design_ids):,} / {len(all_design_ids):,}** ({len(new_accepted_design_ids) / len(all_design_ids):.0%})"
            )
        else:
            st.write(
                f"Accepted designs: **{len(accepted_design_ids):,} / {len(all_design_ids):,}** ({len(accepted_design_ids) / len(all_design_ids):.2%})"
            )

        display_current_thresholds(
            selected_thresholds=st.session_state.selected_thresholds,
            all_design_ids=all_design_ids,
            num_accepted_by_descriptor=num_accepted_by_descriptor,
        )

        if st.session_state.selected_thresholds != saved_thresholds:
            if inconsistent_threshold_keys:
                st.warning(
                    f"Selected pools currently use different thresholds for {' & '.join(inconsistent_threshold_keys)}, confirming will override these with the selected threshold value."
                )
            left, mid, _, _ = st.columns(4)
            if left.button(
                "Confirm thresholds",
                key="confirm_designs_btn",
                type="primary",
                width="stretch",
            ):
                accept_designs_dialog(
                    pools=pools,
                    jobs=jobs,
                    all_design_ids=all_design_ids,
                    new_accepted_design_ids=new_accepted_design_ids,
                    num_accepted_by_descriptor=num_accepted_by_descriptor,
                    selected_thresholds=st.session_state.selected_thresholds,
                )
            if mid.button("Discard changes", width="stretch"):
                st.session_state.selected_thresholds = saved_thresholds
                st.rerun()

        st.subheader("Acceptance thresholds")
        if inconsistent_threshold_keys:
            st.warning(
                f"Looking at multiple workflows with different thresholds for {' & '.join(inconsistent_threshold_keys)}, using the first values."
            )
        new_thresholds = thresholds_and_histograms_component(
            selected_thresholds=st.session_state.selected_thresholds,
            all_design_ids=all_design_ids,
        )

        if st.session_state.selected_thresholds != new_thresholds:
            # User just changed one of the thresholds, update them in session state
            st.session_state.selected_thresholds = new_thresholds
            st.rerun()

        if st.session_state.selected_thresholds != saved_thresholds:
            st.header(
                f"{len(new_accepted_design_ids):,} accepted {'design' if len(new_accepted_design_ids) == 1 else 'designs'} based on new thresholds"
            )
            st.warning(
                "Thresholds have been changed, showing preview of accepted designs based on new thresholds. "
                "Please save using the 'Confirm thresholds' button above to apply changes."
            )
            displayed_design_ids = new_accepted_design_ids
        else:
            displayed_design_ids = accepted_design_ids

    elif show_mode == "All designs":
        st.query_params["show"] = show_mode
        scatterplot_settings = descriptor_scatterplot_input_component(all_design_ids)
        if not scatterplot_settings:
            return

        selected_design_ids, selection_label = (
            descriptor_scatterplot_pool_details_component(
                settings=scatterplot_settings,
                design_ids=all_design_ids,
                highlight_accepted=True,
                selected_thresholds=st.session_state.selected_thresholds,
            )
        )

        if selection_label:
            st.info(f"Selected region: {selection_label}")
            displayed_design_ids = selected_design_ids
            st.header(
                f"Showing {len(displayed_design_ids):,} {'design' if len(displayed_design_ids) == 1 else 'designs'} selected in scatterplot"
            )
        else:
            st.caption(
                ":material/info: Select a region in the scatterplot to display designs that fall within the selected range."
            )
            displayed_design_ids = all_design_ids
            st.header(f"Showing all {len(displayed_design_ids):,} designs")

    else:
        st.error("Select a mode.")
        return

    if not displayed_design_ids:
        st.write("No designs found")
        return

    st.subheader("Download")
    download_job_designs_component(displayed_design_ids, pools)

    st.subheader("Structure visualization")
    workflow_names = set(job.workflow.name for job in jobs if job.workflow)

    visualize_designs_fragment(
        design_ids=displayed_design_ids,
        shared_workflow_name=(
            list(workflow_names)[0] if len(workflow_names) == 1 else None
        ),
    )


@st.fragment
def visualize_designs_fragment(
    design_ids: list[str], shared_workflow_name: str | None = None
):
    if not design_ids:
        st.warning("No designs to show")
        return
    elif len(design_ids) == 1:
        design_id = design_ids[0]
    else:
        indexes = {v: i for i, v in enumerate(design_ids, start=1)}
        design_id = st.selectbox(
            "Select design",
            options=[None] + design_ids,
            format_func=lambda v: (
                "Preview all designs" if v is None else f"{indexes[v]} | {v}"
            ),
            index=1,
        )

    if design_id is None:
        WorkflowType = (
            WorkflowTypes.get(shared_workflow_name)
            if shared_workflow_name
            else DesignWorkflow
        )

        try:
            WorkflowType.visualize_multiple_designs_structures(design_ids=design_ids)
        except NotImplementedError:
            st.warning(
                f"Visualization of multiple designs not supported by {shared_workflow_name or 'default workflow'}, "
                "please select a single design using the dropdown above."
            )
            return
    else:
        st.subheader(design_id)

        design = get_cached_design(design_id)
        pool = get_cached_pool(design.pool_id)
        if not shared_workflow_name and pool.design_job_id:
            design_job = get_cached_design_job(pool.design_job_id)
            shared_workflow_name = (
                design_job.workflow.name if design_job and design_job.workflow else None
            )

        WorkflowType = (
            WorkflowTypes.get(shared_workflow_name)
            if shared_workflow_name
            else DesignWorkflow
        )

        try:
            WorkflowType.visualize_single_design_structures(design_id)
        except Exception as e:
            st.error(f"Error visualizing structure: {e}")

        st.write("### Sequence")

        WorkflowType.visualize_single_design_sequences(design_id)

        st.write(f"### Download {design_id}")

        download_job_designs_component(
            design_ids=[design_id], pools=[pool], key="single"
        )

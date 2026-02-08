# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\app.py\components.py\scheduler_components_5fc5ce1e4bde.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\app\components\scheduler_components.py

import time

import streamlit as st

from ovo.core.scheduler.base_scheduler import Scheduler


def wait_with_statusbar(
    scheduler: Scheduler,
    job_id: str,
    label="Workflow in progress...",
    interval_seconds=1.0,
    timeout_seconds=60 * 60,
) -> bool:

    if scheduler.get_result(job_id):
        # Do not render the component at all if the job has already finished

        return True

    log_element = None

    watching_since = time.time()

    # TODO how to monitor job status in a more granular way?

    with st.status("") as statusbar:
        log_container = st.container(height=300, key=f"job_log_{job_id}")

        if st.button("Abort", key=f"abort_{job_id}"):
            statusbar.update(state="error", label="Job cancelled", expanded=False)

            scheduler.cancel(job_id)

            return False

        # Wait in sleep loop

        while True:
            result = scheduler.get_result(job_id)

            if log_text := scheduler.get_log(job_id):
                if result is None:
                    log_text += "\n...monitoring logs..."

                if log_element is None:
                    with log_container:
                        log_element = st.code(log_text)

                else:
                    log_element.code(log_text)

            if result is not None:
                if result:
                    statusbar.update(state="complete", label="Job finished")

                else:
                    statusbar.update(state="error", label="Job failed", expanded=True)

                return result

            if hasattr(scheduler, "queue_size"):
                queue_size = scheduler.queue_size(job_id=job_id)

                if queue_size is None:
                    # Job is running or queue is not used

                    statusbar.update(state="running", label=label)

                else:
                    if queue_size == 0:
                        # Job is next to run

                        behind_label = ", starting soon"

                    else:
                        # Job is waiting in front of others

                        behind_label = f" behind {queue_size} {'job' if queue_size == 1 else 'jobs'}"

                    statusbar.update(state="running", label=f"Waiting in queue{behind_label}...")

            if time.time() - watching_since > timeout_seconds:
                scheduler.cancel(job_id)

                raise TimeoutError(f"Waiting timed out after {timeout_seconds} seconds, cancelling job {job_id}")

            time.sleep(interval_seconds)

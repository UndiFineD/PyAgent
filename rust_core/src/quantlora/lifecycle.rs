use pyo3::prelude::*;

/// Validate request status transition.
/// Returns true if transition from current to next state is valid.
#[pyfunction]
pub fn request_status_transition_rust(
    current: u8,
    next: u8,
) -> PyResult<bool> {
    // States: 0=WAITING, 1=PENDING, 2=RUNNING, 3=PREEMPTED,
    //         4=FINISHED_STOPPED, 5=FINISHED_LENGTH, 6=FINISHED_ABORTED, 7=FINISHED_ERROR
    let valid = match (current, next) {
        // From WAITING
        (0, 1) | (0, 2) | (0, 6) => true,  // -> PENDING, RUNNING, ABORTED
        // From PENDING
        (1, 2) | (1, 6) => true,           // -> RUNNING, ABORTED
        // From RUNNING
        (2, 3) | (2, 4) | (2, 5) | (2, 6) | (2, 7) => true,  // -> PREEMPTED, any FINISHED
        // From PREEMPTED
        (3, 0) | (3, 2) | (3, 6) => true,  // -> WAITING, RUNNING, ABORTED
        // FINISHED states are terminal
        (4..=7, _) => false,
        _ => false,
    };
    Ok(valid)
}

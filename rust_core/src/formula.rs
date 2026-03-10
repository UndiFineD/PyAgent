use std::collections::HashMap;

use evalexpr::{ContextWithMutableVariables, HashMapContext, Value};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Evaluates a mathematical expression using context variables.
#[pyfunction]
pub fn evaluate_formula(expression: &str, variables: HashMap<String, f64>) -> PyResult<f64> {
    let mut context: HashMapContext = HashMapContext::new();

    for (name, value) in variables {
        context
            .set_value(name, Value::Float(value))
            .map_err(|err| PyValueError::new_err(err.to_string()))?;
    }

    evalexpr::eval_number_with_context(expression, &context)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

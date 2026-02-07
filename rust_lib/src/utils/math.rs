use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

/// Evaluate a math formula with variables using a minimal hand-written parser.
/// This is a safe, dependency-free Rust core for FormulaEngineCore parity.
#[pyfunction]
pub fn evaluate_formula(formula: &str, variables: HashMap<String, f64>) -> PyResult<f64> {
    let mut expr = formula.to_string();

    // Replace {var} placeholders with numeric values
    for (k, v) in variables.iter() {
        let placeholder = format!("{{{}}}", k);
        expr = expr.replace(&placeholder, &v.to_string());
    }

    match mini_eval(&expr) {
        Ok(val) => Ok(val),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(e)),
    }
}

/// Simple recursive descent parser for basic math (+ - * / ^ ( ))
fn mini_eval(expr: &str) -> Result<f64, String> {
    let mut it = expr.chars().filter(|c| !c.is_whitespace()).peekable();
    parse_expr(&mut it)
}

fn parse_expr<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let mut val = parse_term(it)?;
    while let Some(&c) = it.peek() {
        match c {
            '+' => {
                it.next();
                val += parse_term(it)?;
            }
            '-' => {
                it.next();
                val -= parse_term(it)?;
            }
            _ => break,
        }
    }
    Ok(val)
}

fn parse_term<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let mut val = parse_power(it)?;
    while let Some(&c) = it.peek() {
        match c {
            '*' => {
                it.next();
                val *= parse_power(it)?;
            }
            '/' => {
                it.next();
                let div = parse_power(it)?;
                if div == 0.0 {
                    return Err("Division by zero".into());
                }
                val /= div;
            }
            _ => break,
        }
    }
    Ok(val)
}

fn parse_power<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    let val = parse_factor(it)?;
    if let Some(&'^') = it.peek() {
        it.next();
        Ok(val.powf(parse_power(it)?)) // Right-associative
    } else {
        Ok(val)
    }
}

fn parse_factor<I: Iterator<Item = char>>(it: &mut std::iter::Peekable<I>) -> Result<f64, String> {
    match it.next() {
        Some('(') => {
            let val = parse_expr(it)?;
            if it.next() != Some(')') {
                return Err("Missing closing parenthesis".into());
            }
            Ok(val)
        }
        Some('-') => Ok(-parse_factor(it)?),
        Some('+') => Ok(parse_factor(it)?),
        Some(c) if c.is_digit(10) || c == '.' => {
            let mut s = c.to_string();
            while let Some(&c) = it.peek() {
                if c.is_digit(10) || c == '.' || c == 'e' || c == 'E' {
                    s.push(it.next().unwrap());
                } else if (c == '+' || c == '-') && (s.ends_with('e') || s.ends_with('E')) {
                    s.push(it.next().unwrap());
                } else {
                    break;
                }
            }
            s.parse::<f64>().map_err(|_| format!("Invalid number: {}", s))
        }
        Some(c) => Err(format!("Unexpected character: {}", c)),
        None => Err("Unexpected end of expression".into()),
    }
}

/// Ceiling division without floating point.
/// Uses: (a + b - 1) / b for positive values, which gives ceiling division.
#[pyfunction]
pub fn cdiv_rust(a: i64, b: i64) -> PyResult<i64> {
    if b == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("division by zero"));
    }
    // For ceiling division: (a + b - 1) / b for positive a and b
    // General formula that works for any signs:
    if (a >= 0 && b > 0) || (a <= 0 && b < 0) {
        // Same sign: ceiling is (a + b - sign(b)) / b
        Ok((a + b - b.signum()) / b)
    } else {
        // Different signs: regular division already truncates toward zero
        Ok(a / b)
    }
}

/// Return the smallest power of 2 >= n.
#[pyfunction]
pub fn next_power_of_2_rust(n: u64) -> PyResult<u64> {
    if n == 0 {
        return Ok(1);
    }
    if n & (n - 1) == 0 {
        return Ok(n);  // Already a power of 2
    }
    Ok(1u64 << (64 - n.leading_zeros()))
}

/// Return the largest power of 2 <= n (inclusive).
#[pyfunction]
pub fn prev_power_of_2_rust(n: u64) -> PyResult<u64> {
    if n == 0 {
        return Ok(1);
    }
    Ok(1u64 << (63 - n.leading_zeros()))
}

/// Round n up to the nearest multiple.
#[pyfunction]
pub fn round_up_rust(n: i64, multiple: i64) -> PyResult<i64> {
    if multiple == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("multiple cannot be zero"));
    }
    let abs_multiple = multiple.abs();
    // (n + multiple - 1) / multiple * multiple for positive, but we use cdiv
    let cdiv_val = if (n >= 0 && abs_multiple > 0) || (n <= 0 && multiple < 0) {
        (n + abs_multiple - 1) / abs_multiple
    } else if n == 0 {
        0
    } else {
        n / abs_multiple
    };
    Ok(cdiv_val * abs_multiple)
}

/// Round n down to the nearest multiple.
#[pyfunction]
pub fn round_down_rust(n: i64, multiple: i64) -> PyResult<i64> {
    if multiple == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("multiple cannot be zero"));
    }
    Ok((n / multiple) * multiple)
}

/// Atomic counter add operation (placeholder for actual atomic).
#[pyfunction]
pub fn atomic_counter_add_rust(current: i64, delta: i64) -> PyResult<i64> {
    Ok(current + delta)
}

/// Batch ceiling division for multiple values.
#[pyfunction]
pub fn batch_cdiv_rust(values: Vec<i64>, divisor: i64) -> PyResult<Vec<i64>> {
    if divisor == 0 {
        return Err(pyo3::exceptions::PyZeroDivisionError::new_err("division by zero"));
    }
    Ok(values.into_iter().map(|a| -(a / -divisor)).collect())
}

/// Batch next_power_of_2 for multiple values.
#[pyfunction]
pub fn batch_next_power_of_2_rust(values: Vec<u64>) -> PyResult<Vec<u64>> {
    Ok(values.into_iter().map(|n| {
        if n == 0 {
            1
        } else if n & (n - 1) == 0 {
            n
        } else {
            1u64 << (64 - n.leading_zeros())
        }
    }).collect())
}

#[pyfunction]
pub fn calculate_statistical_significance(
    control: Vec<f64>,
    treatment: Vec<f64>,
) -> PyResult<HashMap<String, f64>> {
    let n1 = control.len() as f64;
    let n2 = treatment.len() as f64;
    
    if n1 < 2.0 || n2 < 2.0 {
         let mut min_res = HashMap::new();
         min_res.insert("t_statistic".to_string(), 0.0);
         min_res.insert("p_value".to_string(), 1.0);
         min_res.insert("effect_size".to_string(), 0.0);
         return Ok(min_res);
    }
    
    let mean1 = control.iter().sum::<f64>() / n1;
    let mean2 = treatment.iter().sum::<f64>() / n2;
    
    let var1 = control.iter().map(|x| (x - mean1).powi(2)).sum::<f64>() / (n1 - 1.0);
    let var2 = treatment.iter().map(|x| (x - mean2).powi(2)).sum::<f64>() / (n2 - 1.0);
    
    let pooled_sd = ((var1 * (n1 - 1.0) + var2 * (n2 - 1.0)) / (n1 + n2 - 2.0)).sqrt();
    let se = (var1/n1 + var2/n2).sqrt();
    
    let t_stat = if se != 0.0 { (mean2 - mean1) / se } else { 0.0 };
    let effect_size = if pooled_sd != 0.0 { (mean2 - mean1) / pooled_sd } else { 0.0 };
    
    // P-value approximation
    let p_value = if t_stat.abs() > 1.96 { 0.05 } else { 0.5 }; // Dummy

    let mut results = HashMap::new();
    results.insert("t_statistic".to_string(), t_stat);
    results.insert("p_value".to_string(), p_value);
    results.insert("effect_size".to_string(), effect_size);
    Ok(results)
}

#[pyfunction]
pub fn calculate_jaccard_similarity(s1: &str, s2: &str) -> PyResult<f64> {
    // Word-based Jaccard
    let set1: HashSet<&str> = s1.split_whitespace().collect();
    let set2: HashSet<&str> = s2.split_whitespace().collect();
    
    if set1.is_empty() && set2.is_empty() { return Ok(1.0); }
    
    let intersection = set1.intersection(&set2).count();
    let union = set1.len() + set2.len() - intersection;
    
    if union == 0 { return Ok(0.0); }
    Ok(intersection as f64 / union as f64)
} 


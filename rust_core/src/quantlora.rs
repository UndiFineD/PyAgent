use pyo3::prelude::*;

pub mod attention;
pub mod lifecycle;
pub mod lora;
pub mod quantization;
pub mod sampling;
pub mod utils;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Attention
    m.add_function(pyo3::wrap_pyfunction!(attention::attention_softmax_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(attention::gqa_expand_kv_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(attention::slot_mapping_rust, m)?)?;
    
    // Lifecycle
    m.add_function(pyo3::wrap_pyfunction!(lifecycle::request_status_transition_rust, m)?)?;
    
    // LoRA
    m.add_function(pyo3::wrap_pyfunction!(lora::lora_merge_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(lora::lora_forward_rust, m)?)?;
    
    // Quantization
    m.add_function(pyo3::wrap_pyfunction!(quantization::quantize_symmetric_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(quantization::quantize_asymmetric_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(quantization::dequantize_int4_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(quantization::pack_int4_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(quantization::compute_scales_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(quantization::batch_dequantize_rust, m)?)?;
    
    // Sampling
    m.add_function(pyo3::wrap_pyfunction!(sampling::top_k_mask_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(sampling::top_p_mask_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(sampling::gumbel_sample_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(sampling::beam_score_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(sampling::compute_penalties_rust, m)?)?;
    
    // Utils
    m.add_function(pyo3::wrap_pyfunction!(utils::check_stop_tokens_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(utils::update_prefix_offset_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(utils::hash_block_tokens_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(utils::check_stop_strings_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(utils::detokenize_batch_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(utils::validate_utf8_rust, m)?)?;

    Ok(())
}

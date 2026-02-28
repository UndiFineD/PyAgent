use pyo3::prelude::*;

pub mod image;
pub mod audio;
pub mod grammar;
pub mod distributed;
pub mod container;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Image
    m.add_function(wrap_pyfunction!(image::image_resize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::normalize_pixels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::extract_video_frames_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::image_grid_split_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::create_vision_mosaic_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::detect_motion_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::detect_visual_scene_change_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::overlay_vision_feeds_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::transform_vision_feed_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::extract_vision_roi_rust, m)?)?;
    
    // Container
    m.add_function(wrap_pyfunction!(container::parse_modality_stream_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::layout_vision_feeds_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::calculate_temporal_entropy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::apply_vision_filter_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::calculate_visual_deltas_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::apply_visual_deltas_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::calculate_vision_saliency_rust, m)?)?;
    m.add_function(wrap_pyfunction!(image::match_vision_color_profiles_rust, m)?)?;

    // Audio
    m.add_function(wrap_pyfunction!(audio::resample_audio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::audio_noise_suppression_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::calculate_audio_direction_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::audio_mix_tracks_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::calculate_mel_features_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::audio_quantize_int8_rust, m)?)?;
    m.add_function(wrap_pyfunction!(audio::speech_vad_rust, m)?)?;

    // Grammar
    m.add_function(wrap_pyfunction!(grammar::json_schema_to_regex_rust, m)?)?;
    m.add_function(wrap_pyfunction!(grammar::regex_match_prefix_rust, m)?)?;
    m.add_function(wrap_pyfunction!(grammar::compile_ebnf_rust, m)?)?;
    m.add_function(wrap_pyfunction!(grammar::grammar_next_tokens_rust, m)?)?;

    // Distributed
    m.add_function(wrap_pyfunction!(distributed::consistent_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(distributed::select_worker_lb_rust, m)?)?;
    m.add_function(wrap_pyfunction!(distributed::aggregate_worker_metrics_rust, m)?)?;

    // Container
    m.add_function(wrap_pyfunction!(container::parse_modality_stream_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::switch_modality_channel_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::project_modality_embeddings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::synchronize_modalities_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::calculate_dynamic_modality_weights_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::calculate_multimodal_fusion_rust, m)?)?;
    m.add_function(wrap_pyfunction!(container::calculate_av_alignment_score_rust, m)?)?;

    Ok(())
}

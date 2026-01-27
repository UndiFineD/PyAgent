use pyo3::prelude::*;

/// Combine multiple camera feeds into a single tiled mosaic image (Phase 138/Multi-Cam).
/// Used for surveillance or multi-angle reasoning.
#[pyfunction]
pub fn create_vision_mosaic_rust(
    camera_feeds: Vec<Vec<u8>>, // List of pixel buffers (R,G,B)
    feed_width: usize,
    feed_height: usize,
    rows: usize,
    cols: usize,
) -> PyResult<Vec<u8>> {
    let total_pixels = feed_width * feed_height * 3;
    let mosaic_width = feed_width * cols;
    let mosaic_height = feed_height * rows;
    let mut mosaic = vec![0u8; mosaic_width * mosaic_height * 3];
    
    for (idx, feed) in camera_feeds.iter().enumerate() {
        if idx >= rows * cols { break; }
        if feed.len() != total_pixels { continue; }
        
        let row_offset = idx / cols;
        let col_offset = idx % cols;
        let start_y = row_offset * feed_height;
        let start_x = col_offset * feed_width;
        
        for y in 0..feed_height {
            let mosaic_y = start_y + y;
            let mosaic_row_start = (mosaic_y * mosaic_width + start_x) * 3;
            let feed_row_start = y * feed_width * 3;
            
            mosaic[mosaic_row_start..mosaic_row_start + (feed_width * 3)]
                .copy_from_slice(&feed[feed_row_start..feed_row_start + (feed_width * 3)]);
        }
    }
    
    Ok(mosaic)
}

/// Overlay multiple vision feeds with support for alpha blending and coordinates (Phase 145/PiP).
/// Allows for "Picture-in-Picture" (PiP) or dynamic UI overlays.
#[pyfunction]
pub fn overlay_vision_feeds_rust(
    base_pixels: Vec<u8>,
    overlay_pixels: Vec<u8>,
    base_width: usize,
    base_height: usize,
    overlay_width: usize,
    overlay_height: usize,
    pos_x: usize,
    pos_y: usize,
    alpha: f32,
) -> PyResult<Vec<u8>> {
    let mut output = base_pixels.clone();
    
    for y in 0..overlay_height {
        let dst_y = pos_y + y;
        if dst_y >= base_height { break; }
        
        for x in 0..overlay_width {
            let dst_x = pos_x + x;
            if dst_x >= base_width { break; }
            
            let dst_idx = (dst_y * base_width + dst_x) * 3;
            let src_idx = (y * overlay_width + x) * 3;
            
            if src_idx + 2 < overlay_pixels.len() && dst_idx + 2 < output.len() {
                for c in 0..3 {
                    let src_val = overlay_pixels[src_idx + c] as f32;
                    let dst_val = output[dst_idx + c] as f32;
                    output[dst_idx + c] = (src_val * alpha + dst_val * (1.0 - alpha)) as u8;
                }
            }
        }
    }
    
    Ok(output)
}

/// Transform a vision feed with aspect ratio preservation or stretching (Phase 146).
/// Returns a background-padded or cropped frame to fit target dimensions.
#[pyfunction]
pub fn transform_vision_feed_rust(
    pixels: Vec<u8>,
    src_w: usize,
    src_h: usize,
    dst_w: usize,
    dst_h: usize,
    keep_aspect: bool,
    pad_color: (u8, u8, u8),
) -> Vec<u8> {
    let mut output = vec![0u8; dst_w * dst_h * 3];
    // Fill background with pad_color
    for i in 0..dst_w * dst_h {
        output[i*3] = pad_color.0;
        output[i*3+1] = pad_color.1;
        output[i*3+2] = pad_color.2;
    }
    
    if pixels.is_empty() { return output; }
    
    let (target_w, target_h, offset_x, offset_y) = if keep_aspect {
        let src_aspect = src_w as f32 / src_h as f32;
        let dst_aspect = dst_w as f32 / dst_h as f32;
        
        let (tw, th) = if src_aspect > dst_aspect {
            (dst_w, (dst_w as f32 / src_aspect) as usize)
        } else {
            ((dst_h as f32 * src_aspect) as usize, dst_h)
        };
        (tw, th, (dst_w - tw) / 2, (dst_h - th) / 2)
    } else {
        (dst_w, dst_h, 0, 0)
    };
    
    // Simple nearest-neighbor resize for transformation speed
    for y in 0..target_h {
        let src_y = (y as f32 * src_h as f32 / target_h as f32) as usize;
        for x in 0..target_w {
            let src_x = (x as f32 * src_w as f32 / target_w as f32) as usize;
            
            let dst_idx = ((y + offset_y) * dst_w + (x + offset_x)) * 3;
            let src_idx = (src_y * src_w + src_x) * 3;
            
            if src_idx + 2 < pixels.len() && dst_idx + 2 < output.len() {
                output[dst_idx] = pixels[src_idx];
                output[dst_idx + 1] = pixels[src_idx + 1];
                output[dst_idx + 2] = pixels[src_idx + 2];
            }
        }
    }
    
    output
}

/// Extract a Region of Interest (ROI) from a vision feed (Phase 147/Zoom).
/// Allows the agent to "crop and zoom" into specific areas of the mosaic.
#[pyfunction]
pub fn extract_vision_roi_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    roi_x: usize,
    roi_y: usize,
    roi_w: usize,
    roi_h: usize,
) -> PyResult<Vec<u8>> {
    let mut crop = Vec::with_capacity(roi_w * roi_h * 3);
    
    for y in 0..roi_h {
        let src_y = roi_y + y;
        if src_y >= height { break; }
        
        let start_idx = (src_y * width + roi_x) * 3;
        let mut row_len = roi_w * 3;
        if roi_x + roi_w > width {
            row_len = (width - roi_x) * 3;
        }
        
        if start_idx + row_len <= pixels.len() {
            crop.extend_from_slice(&pixels[start_idx..start_idx + row_len]);
        }
    }
    
    // Pad if crop was smaller than requested roi_w/roi_h
    let current_pixels = crop.len() / 3;
    let target_pixels = roi_w * roi_h;
    if current_pixels < target_pixels {
        crop.resize(target_pixels * 3, 0);
    }
    
    Ok(crop)
}

/// Create a composite layout of multiple vision feeds (Phase 149/Layout).
/// Supports templates: "grid", "sidebar" (1 large + N small), "top_down".
#[pyfunction]
pub fn layout_vision_feeds_rust(
    feeds: Vec<Vec<u8>>,
    feed_sizes: Vec<(usize, usize)>, // (w, h) per feed
    target_w: usize,
    target_h: usize,
    template: &str,
) -> PyResult<Vec<u8>> {
    let mut composite = vec![0u8; target_w * target_h * 3];
    if feeds.is_empty() { return Ok(composite); }
    
    match template {
        "sidebar" => {
            // Main feed (0) takes left 75%, others stacked on right 25%
            let main_w = (target_w as f32 * 0.75) as usize;
            let sidebar_w = target_w - main_w;
            
            // Draw main
            let main_frame = transform_vision_feed_rust(
                feeds[0].clone(), feed_sizes[0].0, feed_sizes[0].1, 
                main_w, target_h, true, (0,0,0)
            );
            copy_to_composite(&mut composite, &main_frame, main_w, target_h, target_w, 0, 0);
            
            // Draw sidebar (remaining feeds)
            if feeds.len() > 1 {
                let thumb_h = target_h / (feeds.len() - 1);
                for i in 1..feeds.len() {
                    let thumb = transform_vision_feed_rust(
                        feeds[i].clone(), feed_sizes[i].0, feed_sizes[i].1,
                        sidebar_w, thumb_h, true, (20, 20, 20)
                    );
                    copy_to_composite(&mut composite, &thumb, sidebar_w, thumb_h, target_w, main_w, (i-1)*thumb_h);
                }
            }
        }
        "grid" | _ => {
            // Standard N x M grid (using previous create_vision_mosaic_rust logic)
            let count = feeds.len();
            let cols = (count as f32).sqrt().ceil() as usize;
            let rows = (count as f32 / cols as f32).ceil() as usize;
            let cell_w = target_w / cols;
            let cell_h = target_h / rows;
            
            for (idx, feed) in feeds.iter().enumerate() {
                let cell = transform_vision_feed_rust(
                    feed.clone(), feed_sizes[idx].0, feed_sizes[idx].1,
                    cell_w, cell_h, true, (0,0,0)
                );
                let x = (idx % cols) * cell_w;
                let y = (idx / cols) * cell_h;
                copy_to_composite(&mut composite, &cell, cell_w, cell_h, target_w, x, y);
            }
        }
    }
    
    Ok(composite)
}

fn copy_to_composite(
    target: &mut Vec<u8>, 
    src: &[u8], 
    sw: usize, sh: usize, 
    tw: usize, 
    ox: usize, oy: usize
) {
    for y in 0..sh {
        let ty = oy + y;
        let si = y * sw * 3;
        let ti = (ty * tw + ox) * 3;
        if ti + (sw * 3) <= target.len() && si + (sw * 3) <= src.len() {
            target[ti..ti + (sw * 3)].copy_from_slice(&src[si..si + (sw * 3)]);
        }
    }
}

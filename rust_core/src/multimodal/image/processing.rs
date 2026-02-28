use pyo3::prelude::*;

/// Fast image resize using bilinear interpolation
/// Input/output are flat arrays in row-major order (H, W, C)
#[pyfunction]
#[pyo3(signature = (pixels, src_height, src_width, channels, dst_height, dst_width))]
pub fn image_resize_rust(
    pixels: Vec<f32>,
    src_height: usize,
    src_width: usize,
    channels: usize,
    dst_height: usize,
    dst_width: usize,
) -> Vec<f32> {
    if pixels.is_empty() || src_height == 0 || src_width == 0 {
        return Vec::new();
    }
    
    let mut output = vec![0.0f32; dst_height * dst_width * channels];
    
    let y_ratio = if dst_height > 1 {
        (src_height - 1) as f32 / (dst_height - 1) as f32
    } else {
        0.0
    };
    let x_ratio = if dst_width > 1 {
        (src_width - 1) as f32 / (dst_width - 1) as f32
    } else {
        0.0
    };
    
    for dst_y in 0..dst_height {
        let src_y = dst_y as f32 * y_ratio;
        let y0 = src_y.floor() as usize;
        let y1 = (y0 + 1).min(src_height - 1);
        let y_frac = src_y - y0 as f32;
        
        for dst_x in 0..dst_width {
            let src_x = dst_x as f32 * x_ratio;
            let x0 = src_x.floor() as usize;
            let x1 = (x0 + 1).min(src_width - 1);
            let x_frac = src_x - x0 as f32;
            
            for c in 0..channels {
                // Bilinear interpolation
                let idx00 = (y0 * src_width + x0) * channels + c;
                let idx01 = (y0 * src_width + x1) * channels + c;
                let idx10 = (y1 * src_width + x0) * channels + c;
                let idx11 = (y1 * src_width + x1) * channels + c;
                
                let p00 = pixels.get(idx00).copied().unwrap_or(0.0);
                let p01 = pixels.get(idx01).copied().unwrap_or(0.0);
                let p10 = pixels.get(idx10).copied().unwrap_or(0.0);
                let p11 = pixels.get(idx11).copied().unwrap_or(0.0);
                
                let top = p00 * (1.0 - x_frac) + p01 * x_frac;
                let bottom = p10 * (1.0 - x_frac) + p11 * x_frac;
                let value = top * (1.0 - y_frac) + bottom * y_frac;
                
                let dst_idx = (dst_y * dst_width + dst_x) * channels + c;
                output[dst_idx] = value;
            }
        }
    }
    
    output
}

/// Normalize pixel values with mean and std
/// Applies per-channel normalization: (pixel - mean) / std
#[pyfunction]
#[pyo3(signature = (pixels, channels, mean, std))]
pub fn normalize_pixels_rust(
    pixels: Vec<f32>,
    channels: usize,
    mean: Vec<f32>,
    std: Vec<f32>,
) -> Vec<f32> {
    if pixels.is_empty() || channels == 0 || mean.len() != channels || std.len() != channels {
        return pixels;
    }
    
    let mut output = pixels.clone();
    let num_pixels = output.len() / channels;
    
    for i in 0..num_pixels {
        for c in 0..channels {
            let idx = i * channels + c;
            if idx < output.len() {
                let m = mean[c];
                let s = if std[c] != 0.0 { std[c] } else { 1.0 };
                output[idx] = (output[idx] - m) / s;
            }
        }
    }
    
    output
}

/// Split a high-resolution image into a grid of tiles (LLaVA-NeXT style).
#[pyfunction]
pub fn image_grid_split_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    rows: usize,
    cols: usize,
) -> PyResult<Vec<Vec<u8>>> {
    if pixels.len() != width * height * 3 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid pixel buffer size"));
    }
    
    let tile_w = width / cols;
    let tile_h = height / rows;
    let mut tiles = Vec::with_capacity(rows * cols);
    
    for r in 0..rows {
        for c in 0..cols {
            let mut tile = Vec::with_capacity(tile_w * tile_h * 3);
            for y in 0..tile_h {
                let start_idx = ((r * tile_h + y) * width + (c * tile_w)) * 3;
                let end_idx = start_idx + (tile_w * 3);
                tile.extend_from_slice(&pixels[start_idx..end_idx]);
            }
            tiles.push(tile);
        }
    }
    
    Ok(tiles)
}

/// Generate a low-resolution saliency map to identify active regions (Phase 154).
/// Returns a grid of energy levels representing visual focal points.
#[pyfunction]
pub fn calculate_vision_saliency_rust(
    pixels: Vec<u8>,
    width: usize,
    height: usize,
    grid_size: usize,
) -> Vec<f32> {
    let cols = width / grid_size;
    let rows = height / grid_size;
    let mut saliency = vec![0.0f32; rows * cols];
    
    for r in 0..rows {
        for c in 0..cols {
            let mut energy = 0.0;
            for y in 0..grid_size {
                for x in 0..grid_size {
                    let idx = ((r * grid_size + y) * width + (c * grid_size + x)) * 3;
                    if idx + 2 < pixels.len() {
                        // Weighted luminance energy
                        energy += pixels[idx] as f32 * 0.299 + pixels[idx+1] as f32 * 0.587 + pixels[idx+2] as f32 * 0.114;
                    }
                }
            }
            saliency[r * cols + c] = energy / (grid_size * grid_size) as f32;
        }
    }
    
    saliency
}

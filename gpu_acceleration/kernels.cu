"""
CUDA Kernels - Reference Implementation
Optimized kernels for matrix operations, attention, and quantization
Compile with: nvcc -arch=sm_86 -O3 kernels.cu -o kernels.o
"""

#include <cuda_runtime.h>
#include <stdio.h>
#include <math.h>

// ============================================================================
// KERNEL 1: Matrix Multiplication (Basic)
// ============================================================================

__global__ void matmul_basic(float* A, float* B, float* C, int M, int N, int K) {
    """
    Basic matrix multiplication without optimization
    
    Thread layout:
    - blockIdx.x, blockIdx.y: Block coordinates
    - threadIdx.x, threadIdx.y: Thread within block
    - Grid: ((N+31)/32, (M+31)/32)
    - Block: (32, 32)
    """
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; k++) {
            sum += A[row * K + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

// ============================================================================
// KERNEL 2: Matrix Multiplication (Optimized with Shared Memory)
// ============================================================================

__global__ void matmul_optimized(float* A, float* B, float* C,
                                 int M, int N, int K) {
    """
    Optimized matmul with shared memory tiling
    
    Tile size: 32x32
    Shared memory: 2 * 32 * 32 * sizeof(float) = 8 KB
    
    Strategy:
    1. Load A[32x32] tile into shared memory
    2. Load B[32x32] tile into shared memory
    3. Compute partial products
    4. Synchronize threads
    5. Repeat for next tile
    """
    __shared__ float As[32][32];  // Tile of A
    __shared__ float Bs[32][32];  // Tile of B
    
    int row = blockIdx.y * 32 + threadIdx.y;
    int col = blockIdx.x * 32 + threadIdx.x;
    float sum = 0.0f;
    
    // Process all tiles
    for (int tile = 0; tile < K; tile += 32) {
        // Load tiles into shared memory
        As[threadIdx.y][threadIdx.x] = (row < M && (tile + threadIdx.x) < K)
            ? A[row * K + (tile + threadIdx.x)]
            : 0.0f;
        
        Bs[threadIdx.y][threadIdx.x] = ((tile + threadIdx.y) < K && col < N)
            ? B[(tile + threadIdx.y) * N + col]
            : 0.0f;
        
        __syncthreads();  // Wait for all threads to load
        
        // Compute partial products
        #pragma unroll
        for (int k = 0; k < 32; k++) {
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        }
        
        __syncthreads();  // Wait before next iteration
    }
    
    if (row < M && col < N) {
        C[row * N + col] = sum;
    }
}

// ============================================================================
// KERNEL 3: Softmax (for Attention)
// ============================================================================

__global__ void softmax_kernel(float* input, float* output, int N) {
    """
    Numerically stable softmax
    
    softmax(x_i) = exp(x_i - max(x)) / sum(exp(x_j - max(x)))
    """
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < N) {
        float max_val = input[idx];
        
        // Find max (simplified: actual would reduce across block)
        for (int i = 0; i < N; i++) {
            max_val = fmaxf(max_val, input[i]);
        }
        
        // Compute exp and sum
        float exp_sum = 0.0f;
        for (int i = 0; i < N; i++) {
            exp_sum += expf(input[i] - max_val);
        }
        
        // Write output
        output[idx] = expf(input[idx] - max_val) / exp_sum;
    }
}

// ============================================================================
// KERNEL 4: Self-Attention (Simplified)
// ============================================================================

__global__ void attention_kernel(float* Q, float* K, float* V, float* out,
                                int seq_len, int d_model) {
    """
    Simplified self-attention kernel
    
    out[i] = softmax(Q[i] @ K.T / sqrt(d)) @ V
    
    Block layout:
    - blockIdx.x: Token position
    - threadIdx.x: Feature dimension
    """
    int i = blockIdx.x;  // Query token index
    int j = threadIdx.x; // Output feature index
    
    if (i < seq_len && j < d_model) {
        float result = 0.0f;
        
        // For each key/value position
        for (int k = 0; k < seq_len; k++) {
            // Compute attention score: Q[i] @ K[k] / sqrt(d_model)
            float score = 0.0f;
            for (int d = 0; d < d_model; d++) {
                score += Q[i * d_model + d] * K[k * d_model + d];
            }
            score /= sqrtf((float)d_model);
            
            // Apply softmax (simplified: actual would use proper softmax)
            float weight = expf(score);  // Not normalized, for brevity
            
            // Accumulate weighted value
            result += weight * V[k * d_model + j];
        }
        
        out[i * d_model + j] = result;
    }
}

// ============================================================================
// KERNEL 5: Quantization (FP32 -> INT8)
// ============================================================================

__global__ void quantize_int8(float* input, int8_t* output,
                              float scale, int N) {
    """
    Quantize floating point values to INT8
    
    output = clip(round(input / scale), -128, 127)
    
    Scale is typically computed as:
    scale = max(abs(input)) / 127.0
    """
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < N) {
        float scaled = input[idx] / scale;
        float rounded = roundf(scaled);
        
        // Clip to INT8 range
        int8_t quantized = (int8_t)fmaxf(-128.0f, fminf(127.0f, rounded));
        output[idx] = quantized;
    }
}

// ============================================================================
// KERNEL 6: Dequantization (INT8 -> FP32)
// ============================================================================

__global__ void dequantize_int8(int8_t* input, float* output,
                                float scale, int N) {
    """
    Dequantize from INT8 back to floating point
    
    output = input * scale
    """
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < N) {
        output[idx] = (float)input[idx] * scale;
    }
}

// ============================================================================
// KERNEL 7: Layer Normalization
// ============================================================================

__global__ void layer_norm_kernel(float* input, float* gamma, float* beta,
                                  float* output, int N, float eps = 1e-5f) {
    """
    Layer normalization: y = (x - mean) / sqrt(var + eps) * gamma + beta
    
    Block-wide reduction for mean and variance
    """
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < N) {
        // Compute mean (block-wise)
        float mean = 0.0f;
        for (int i = 0; i < N; i++) {
            mean += input[i];
        }
        mean /= N;
        
        // Compute variance
        float var = 0.0f;
        for (int i = 0; i < N; i++) {
            float diff = input[i] - mean;
            var += diff * diff;
        }
        var /= N;
        
        // Normalize
        float normalized = (input[idx] - mean) / sqrtf(var + eps);
        output[idx] = normalized * gamma[idx] + beta[idx];
    }
}

// ============================================================================
// KERNEL 8: GeLU Activation
// ============================================================================

__global__ void gelu_kernel(float* input, float* output, int N) {
    """
    GeLU activation: gelu(x) = x * Phi(x)
    
    Where Phi is the cumulative normal distribution
    Approximation: gelu(x) ≈ 0.5*x*(1 + tanh(sqrt(2/pi)*(x + 0.044715*x^3)))
    """
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < N) {
        float x = input[idx];
        float pi = 3.14159265359f;
        
        // Approximation
        float cdf = 0.5f * (1.0f + tanhf(
            sqrtf(2.0f / pi) * (x + 0.044715f * x * x * x)
        ));
        output[idx] = x * cdf;
    }
}

// ============================================================================
// CPU Launch Wrapper Functions
// ============================================================================

extern "C" {
    void cuda_matmul(float* A, float* B, float* C,
                     int M, int N, int K, bool optimized) {
        """
        Launch matrix multiplication kernel from C/Python
        """
        dim3 block(32, 32);
        dim3 grid((N + 31) / 32, (M + 31) / 32);
        
        if (optimized) {
            matmul_optimized<<<grid, block>>>(A, B, C, M, N, K);
        } else {
            matmul_basic<<<grid, block>>>(A, B, C, M, N, K);
        }
    }
    
    void cuda_quantize(float* input, int8_t* output,
                      float scale, int N) {
        """
        Launch quantization kernel
        """
        int block_size = 256;
        int num_blocks = (N + block_size - 1) / block_size;
        
        quantize_int8<<<num_blocks, block_size>>>(input, output, scale, N);
    }
    
    void cuda_attention(float* Q, float* K, float* V, float* out,
                       int seq_len, int d_model) {
        """
        Launch attention kernel
        """
        attention_kernel<<<seq_len, d_model>>>(Q, K, V, out, seq_len, d_model);
    }
}

// ============================================================================
// Device Query Helper
// ============================================================================

void query_cuda_devices() {
    """
    Print information about available CUDA devices
    """
    int device_count = 0;
    cudaGetDeviceCount(&device_count);
    
    printf("CUDA Devices Found: %d\n", device_count);
    
    for (int i = 0; i < device_count; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);
        
        printf("\nDevice %d: %s\n", i, prop.name);
        printf("  Compute Capability: %d.%d\n", prop.major, prop.minor);
        printf("  Max Threads per Block: %d\n", prop.maxThreadsPerBlock);
        printf("  Memory: %.1f GB\n", prop.totalGlobalMem / 1e9);
        printf("  Shared Memory: %d KB\n", prop.sharedMemPerBlock / 1024);
    }
}

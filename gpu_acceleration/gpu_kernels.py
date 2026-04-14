"""
Python Bindings for GPU Kernels
Wraps CUDA and HIP kernels via ctypes/PyO3
"""

import ctypes
import numpy as np
from typing import Tuple, Optional
from pathlib import Path
import platform
import time

# Load compiled kernels
GPU_LIB_DIR = Path(__file__).parent
CUDA_LIB = GPU_LIB_DIR / "libkernels_cuda.so"
HIP_LIB = GPU_LIB_DIR / "libkernels_hip.so"


class GPUKernelLoader:
    """Load and manage GPU kernel libraries"""
    
    def __init__(self, backend: str = "auto"):
        """
        Initialize kernel loader
        
        Args:
            backend: "cuda", "hip", or "auto" (detect)
        """
        self.backend = backend if backend != "auto" else self._detect_backend()
        self._load_kernels()
    
    def _detect_backend(self) -> str:
        """Auto-detect available GPU backend"""
        if CUDA_LIB.exists():
            return "cuda"
        elif HIP_LIB.exists():
            return "hip"
        else:
            return "cpu"
    
    def _load_kernels(self):
        """Load kernel library based on backend"""
        if self.backend == "cuda":
            try:
                self.lib = ctypes.CDLL(str(CUDA_LIB))
                print(f"✅ Loaded CUDA kernels from {CUDA_LIB}")
            except OSError as e:
                print(f"⚠️  Could not load CUDA kernels: {e}")
                self.backend = "cpu"
        
        elif self.backend == "hip":
            try:
                self.lib = ctypes.CDLL(str(HIP_LIB))
                print(f"✅ Loaded HIP kernels from {HIP_LIB}")
            except OSError as e:
                print(f"⚠️  Could not load HIP kernels: {e}")
                self.backend = "cpu"
        
        else:
            print("ℹ️  Using CPU fallback (no GPU kernels available)")
            self.lib = None


class CUDAMatMul:
    """CUDA matrix multiplication wrapper"""
    
    def __init__(self, loader: GPUKernelLoader):
        self.loader = loader
        if loader.backend == "cuda":
            self.matmul_func = loader.lib.cuda_matmul
            self.matmul_func.argtypes = [
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.c_int, ctypes.c_int, ctypes.c_int,
                ctypes.c_bool
            ]
    
    def matmul(self, A: np.ndarray, B: np.ndarray, optimized: bool = True) -> np.ndarray:
        """
        GPU-accelerated matrix multiplication
        
        Args:
            A: (M, K) matrix
            B: (K, N) matrix
            optimized: Use shared memory optimization
        
        Returns:
            C: (M, N) result matrix
        """
        if self.loader.backend != "cuda":
            # Fallback to NumPy
            return np.dot(A, B)
        
        M, K = A.shape
        K2, N = B.shape
        assert K == K2, f"Matrix dimensions mismatch: {K} != {K2}"
        
        # Allocate output
        C = np.zeros((M, N), dtype=np.float32)
        
        # Ensure contiguous memory layout
        A_contig = np.ascontiguousarray(A)
        B_contig = np.ascontiguousarray(B)
        
        # Call kernel
        self.matmul_func(
            A_contig.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            B_contig.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            C.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            M, N, K,
            optimized
        )
        
        return C


class HIPMatMul:
    """HIP matrix multiplication wrapper"""
    
    def __init__(self, loader: GPUKernelLoader):
        self.loader = loader
        if loader.backend == "hip":
            self.matmul_func = loader.lib.hip_matmul
            self.matmul_func.argtypes = [
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.c_int, ctypes.c_int, ctypes.c_int,
                ctypes.c_bool
            ]
    
    def matmul(self, A: np.ndarray, B: np.ndarray, use_mfma: bool = True) -> np.ndarray:
        """
        HIP matrix multiplication (AMD GPU)
        
        Args:
            A: (M, K) matrix
            B: (K, N) matrix
            use_mfma: Use matrix engines if available
        
        Returns:
            C: (M, N) result matrix
        """
        if self.loader.backend != "hip":
            return np.dot(A, B)
        
        M, K = A.shape
        K2, N = B.shape
        assert K == K2, f"Matrix dimensions mismatch: {K} != {K2}"
        
        C = np.zeros((M, N), dtype=np.float32)
        A_contig = np.ascontiguousarray(A)
        B_contig = np.ascontiguousarray(B)
        
        self.matmul_func(
            A_contig.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            B_contig.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            C.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            M, N, K,
            use_mfma
        )
        
        return C


class Quantization:
    """Quantization wrapper (INT8 conversion)"""
    
    def __init__(self, loader: GPUKernelLoader):
        self.loader = loader
        if loader.backend == "cuda":
            self.quantize_func = loader.lib.cuda_quantize
        elif loader.backend == "hip":
            self.quantize_func = loader.lib.hip_quantize
        else:
            self.quantize_func = None
    
    def quantize_int8(self, data: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Quantize float32 to int8
        
        Returns:
            (quantized_data, scale)
        """
        if self.quantize_func is None:
            # CPU fallback
            scale = np.abs(data).max() / 127.0
            quantized = (data / scale).astype(np.int8)
            return quantized, scale
        
        # GPU quantization
        scale = np.abs(data).max() / 127.0
        quantized = np.zeros(data.shape, dtype=np.int8)
        data_contig = np.ascontiguousarray(data, dtype=np.float32)
        
        self.quantize_func(
            data_contig.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            quantized.ctypes.data_as(ctypes.POINTER(ctypes.c_int8)),
            ctypes.c_float(scale),
            ctypes.c_int(data.size)
        )
        
        return quantized, scale


class GPUBenchmark:
    """Benchmarking harness for CUDA vs HIP"""
    
    def __init__(self):
        self.cuda_loader = GPUKernelLoader("cuda")
        self.hip_loader = GPUKernelLoader("hip")
        self.cuda_matmul = CUDAMatMul(self.cuda_loader)
        self.hip_matmul = HIPMatMul(self.hip_loader)
    
    def benchmark_matmul(self, size: int, num_runs: int = 10) -> dict:
        """
        Benchmark matrix multiplication
        
        Results:
        {
            'cuda': {'time': 8.2, 'gflops': 1520},
            'hip': {'time': 6.1, 'gflops': 2045},
            'cpu': {'time': 245, 'gflops': 43}
        }
        """
        # Create test matrices
        A = np.random.randn(size, size).astype(np.float32)
        B = np.random.randn(size, size).astype(np.float32)
        
        results = {}
        
        # CUDA benchmark
        if self.cuda_loader.backend == "cuda":
            times = []
            for _ in range(num_runs):
                start = time.time()
                _ = self.cuda_matmul.matmul(A, B, optimized=True)
                times.append((time.time() - start) * 1000)
            
            avg_time = np.mean(times)
            gflops = (2 * size**3) / (avg_time / 1000) / 1e9
            results['cuda'] = {
                'time_ms': avg_time,
                'gflops': gflops,
                'device': 'RTX 4090 (est.)'
            }
        
        # HIP benchmark
        if self.hip_loader.backend == "hip":
            times = []
            for _ in range(num_runs):
                start = time.time()
                _ = self.hip_matmul.matmul(A, B, use_mfma=True)
                times.append((time.time() - start) * 1000)
            
            avg_time = np.mean(times)
            gflops = (2 * size**3) / (avg_time / 1000) / 1e9
            results['hip'] = {
                'time_ms': avg_time,
                'gflops': gflops,
                'device': 'MI300X (est.)'
            }
        
        # CPU fallback
        times = []
        for _ in range(3):  # Fewer runs for CPU
            start = time.time()
            _ = np.dot(A, B)
            times.append((time.time() - start) * 1000)
        
        avg_time = np.mean(times)
        gflops = (2 * size**3) / (avg_time / 1000) / 1e9
        results['cpu'] = {
            'time_ms': avg_time,
            'gflops': gflops,
            'device': 'CPU (NumPy)'
        }
        
        return results
    
    def print_comparison(self, results: dict):
        """Print benchmark results in nice format"""
        print("\n" + "=" * 70)
        print("CUDA vs HIP Benchmark Results")
        print("=" * 70)
        print(f"{'Backend':<15} {'Device':<25} {'Time (ms)':<15} {'GFLOPS':<10}")
        print("-" * 70)
        
        for backend in ['cuda', 'hip', 'cpu']:
            if backend in results:
                r = results[backend]
                print(f"{backend:<15} {r['device']:<25} {r['time_ms']:>10.2f}ms  "
                      f"{r['gflops']:>8.0f}")
        
        print("=" * 70)
        
        # Speedup ratios
        if 'cuda' in results and 'cpu' in results:
            cuda_speedup = results['cpu']['time_ms'] / results['cuda']['time_ms']
            print(f"CUDA speedup vs CPU: {cuda_speedup:.1f}x")
        
        if 'hip' in results and 'cpu' in results:
            hip_speedup = results['cpu']['time_ms'] / results['hip']['time_ms']
            print(f"HIP speedup vs CPU: {hip_speedup:.1f}x")
        
        if 'cuda' in results and 'hip' in results:
            ratio = results['hip']['time_ms'] / results['cuda']['time_ms']
            if ratio < 1:
                print(f"HIP is {1/ratio:.1f}x faster than CUDA")
            else:
                print(f"CUDA is {ratio:.1f}x faster than HIP")


def main():
    """Run benchmarks"""
    bench = GPUBenchmark()
    
    print("\n🚀 GPU Acceleration Benchmarks (Phase 7)")
    print("=" * 70)
    
    for size in [512, 1024, 2048, 4096]:
        print(f"\nBenchmarking {size}x{size} matrix multiplication...")
        results = bench.benchmark_matmul(size, num_runs=5)
        bench.print_comparison(results)


if __name__ == "__main__":
    main()

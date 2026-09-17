"""
Benchmark: Matrix multiplication - custom implementation vs NumPy.
"""
import time
import numpy as np
from importlib import import_module

# Our own implementation
matmul_module = import_module("02_matrix_ops")
mat_matmul = matmul_module.matMatmul

# Different sizes
for size in [10, 50, 100]:
    A = [[i + j for j in range(size)] for i in range(size)]
    B = [[i * j for j in range(size)] for i in range(size)]

    # Custom version
    start = time.time()
    _ = mat_matmul(A, B)
    my_time = time.time() - start

    # NumPy version
    A_np = np.array(A)
    B_np = np.array(B)
    start = time.time()
    _ = A_np @ B_np
    np_time = time.time() - start

    print(f"Size {size}x{size}:")
    print(f"  Custom:  {my_time:.4f}s")
    print(f"  NumPy:   {np_time:.4f}s")
    print(f"  Speedup: {my_time / np_time:.1f}x")
    print()
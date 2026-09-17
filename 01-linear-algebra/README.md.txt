# Linear Algebra

Foundation of everything in ML: vectors, matrices, transformations.

## 📚 Resources
- 3Blue1Brown - Essence of Linear Algebra (YouTube)
- Mathematics for Machine Learning (MML) - Chapter 2
- MIT 18.06 (Gilbert Strang) - for deeper theory

## 📁 Files

| File | Topic | Status |
|------|-------|--------|
| `vectors.py` | Vector operations from scratch | ⚪ |
| `matrix_ops.py` | Matrix operations from scratch | 🟡 |
| `benchmark.py` | Custom vs NumPy performance | 🟡 |
| `determinant.py` | Determinant and inverse | ⚪ |
| `rank_nullspace.py` | Rank and null space | ⚪ |

## 📝 Daily Notes

### Day 1
- Setup repo, watched 3Blue1Brown videos 1-2
- Understood: vector, linear combination, span, basis

### Day 2
- Watched more videos, no code yet

### Day 3
- Watched videos up to 14
- Concepts got heavy: change of basis, eigenvectors

### Day 4
- Implemented `matrix_ops.py` (add, sub, transpose, matmul, identity)
- Implemented `benchmark.py` to compare with NumPy
- Key insight: NumPy is hundreds of times faster (uses BLAS in C/Fortran)

## 🔑 Key Takeaways

- **Matrix = linear transformation.** Multiplying a matrix by a vector rotates/stretches it.
- **Matrix multiplication = composition of transformations.** Order matters: `B @ A` means apply A first, then B.
- **Always use NumPy in practice**, but implement from scratch to understand what happens under the hood.
- **Matrix multiplication rule:** `A(m×n) @ B(n×p) = C(m×p)`. Inner dimensions must match.
- **`result[i][j]` = dot product of row i of A and column j of B.**

## ❓ Open Questions
- (Write your unanswered questions here)
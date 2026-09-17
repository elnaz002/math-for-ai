"""
Topic: Matrix Operations
Date: 2026-09-17
Reference: Mathematics for ML - Chapter 2.2
Goal: Implement matrix operations from scratch

"""

#----------1-concept------------------------
# matrix is a 2D array of numbers
# multiplying A(m * n) by B(n * g) gives us a matrix with   this rows and columns C(m * g)
# Rule: row i of A dot column j of B -> C[i][j]

# --------2-Implementation from scratch------

# addition in matrix you should add element by element.

def matAdd(A,B):
  rows = len(A)
  cols = len(A[0])
  result = [[0] * cols for _ in range(rows)]
  for i in range(rows):
     for j in range(cols):
      result[i][j] = A[i][j] + B[i][j]
  return result

# subtraction in matrix you should subtract element by element.

def matSub(A,B):
  rows= len(A)
  cols= len(A[0])
  result = [[0] * cols for _ in range(rows)]
  for i in range(rows):
    for j in range(cols):
      result[i][j] = A[i][j] + B[i][j]
  return result    

# Transpose: rows become columns.

def mat_transpose(A):
    
  rows = len(A)
  cols = len(A[0])
  result = [[0] * rows for _ in range(cols)]
  for i in range(rows):
      for j in range(cols):
        result[j][i] = A[i][j]
  return result


def matMatmul(A,B):
  # Remiander 
  # multiplying A(m * n) by B(n * g) gives us a matrix with   this rows and columns C(m * g)
  m = len(A)
  n = len(A[0])
  p = len(B[0])

  assert len(B) == n, "Incompatible dimensions!"
  result = [[0] * p for _ in range(m)]
  for i in range(m):
    for j in range(p):
      for k in range(n):
        result[i][j] += A[i][k] * B[k][j]
  return result

# Matrix-vector multiplication (special case of matmul).
# we could not multiply a vector and a matrix first we should transfer vector to a (n * 1)

def matVecmul(A, v):
    v_as_col = [[x] for x in v]
    result = matMatmul(A, v_as_col)
    return [row[0] for row in result]

def identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

# ---------------3- Test / Verify--------------
if __name__ == "__main__":
    import numpy as np

    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    print("=== Addition ===")
    print("My:   ", matAdd(A, B))
    print("NumPy:", (np.array(A) + np.array(B)).tolist())

    print("\n=== Subtraction ===")
    print("My:   ", matSub(A, B))
    print("NumPy:", (np.array(A) - np.array(B)).tolist())

    print("\n=== Transpose ===")
    print("My:   ", mat_transpose(A))
    print("NumPy:", np.array(A).T.tolist())

    print("\n=== Matrix Multiplication ===")
    print("My:   ", matMatmul(A, B))
    print("NumPy:", (np.array(A) @ np.array(B)).tolist())

    print("\n=== Matrix x Vector ===")
    v = [1, 2]
    print("My:   ", matVecmul(A, v))
    print("NumPy:", (np.array(A) @ np.array(v)).tolist())

    print("\n=== Identity ===")
    I = identity(3)
    print("My:   ", I)
    print("NumPy:", np.eye(3).tolist())

    # Test: A @ I = A
    assert matMatmul(A, identity(2)) == A
    print("\n[OK] A @ I = A  (test passed)")
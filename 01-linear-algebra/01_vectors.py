"""
Topic : Vectors 
date :2026-09-16
coal : Implement vector operations from scratch

"""

import math
import numpy as np

# -------------1-vector definition-----------------
# a vector in python = a list of numbers 
v = [3,4]
w = [1,6]

print(f"v = {v}")
print(f"w = {w}")

# -----------------2-vector addition --------------
# Add two vectors element by element
def add(u,v):
  result = []
  for i in range(len(u)):
    result.append(u[i] + v[i])
  return result

print(f"\nv + w ={add(v,w)}")  

# -----------------3-vector subtraction --------------

def subtract(u,v):
  result = []
  for i in range(len(u)):
    result.append(u[i] - v[i])
  return result

print(f" v - w ={subtract(v,w)}")

# ------------4- Scalar multiplication-----------------
def scalerMultiply(c,v):
  result = []
  for x in v:
    result.append(c * x)
  return result

print(f" 2 * v ={scalerMultiply(2,v)}")

# ------------------5- Dot product----------------------
# Result is a scalar, not a vector
def dot(u,v):
  result = 0
  for i in range(len(u)):
    result += u[i] * v[i]
  return result

print(f"\nv · w = {dot(v, w)}")

# -------------6- L2 norm (length of a vector) reidge---------
def norm_l2(v):
  sum_squares = 0
  for x in v :
    sum_squares += x * x
  return math.sqrt(sum_squares)  

print(f"\n||v|| = {norm_l2(v)}") 

# ----------7- L1 norm lasso ---------------
def norm_l1(v):
  total = 0
  for x in v:
    total += abs(x)
  return total   

print(f"||v||_1 = {norm_l1(v)}")

# ----------8-Normalization-----------------
# Turn a vector into a unit vector (length = 1)

def normalize(v) :
  n = norm_l2(v)
  return [x / n for x in v ]
print(f"normalized v = {normalize(v)}")  
print(f"its length: {norm_l2(normalize(v))}")  # should be 1.0

# -----------9- Angle between two vectors-------------
# cos(theta) = (u · v) / (||u|| * ||v||)

def angle_between( u , v ):
  cos_theta = dot(u,v) / (norm_l2(u) * norm_l2(v))
  # clamp to avoid numerical errors (like 1.00000000004)
  cos_theta = max(-1, min(1, cos_theta))
  return math.acos(cos_theta)


v1 = [1, 0]
v2 = [0, 1]
print(f"\nAngle between [1,0] and [0,1]: {math.degrees(angle_between(v1, v2))} degrees")  

v3 = [1, 0]
v4 = [1, 1]
print(f"Angle between [1,0] and [1,1]: {math.degrees(angle_between(v3, v4))} degrees")  

# -------------10- Compare with NumPy-------------------

print("\n----- Comparison with NumPy -----")

nv = np.array(v)
nw = np.array(w)

assert add(v, w) == list(nv + nw), "Addition is wrong!"
assert dot(v, w) == np.dot(nv, nw), "Dot product is wrong!"
assert abs(norm_l2(v) - np.linalg.norm(nv)) < 1e-9, "Norm is wrong!"

print("All operations match NumPy!")

# ============ Challenge ============
# Define two vectors: [1, 2, 3] and [4, 5, 6]
# 1. Compute the length of each
# 2. Compute their dot product
# 3. Compute the angle between them
# 4. Verify with NumPy

a = [1, 5, 3]
b = [4, 9, 6]

# 1. Lengths
len_a = norm_l2(a)
len_b = norm_l2(b)
print(f"\n--- Challenge ---")
print(f"length of vector a  = {len_a}")
print(f"length of vector b = {len_b}")

# 2. Dot product
d = dot(a, b)
print(f"a · b = {d}")

# 3. Angle
angle = math.degrees(angle_between(a, b))
print(f"Angle between a and b: {angle} degrees")

# 4. Verify with NumPy
na = np.array(a)
nb = np.array(b)
assert abs(len_a - np.linalg.norm(na)) < 1e-9
assert abs(len_b - np.linalg.norm(nb)) < 1e-9
assert d == np.dot(na, nb)
cos_np = np.dot(na, nb) / (np.linalg.norm(na) * np.linalg.norm(nb))
angle_np = math.degrees(math.acos(max(-1, min(1, cos_np))))
assert abs(angle - angle_np) < 1e-9
print("Challenge verified with NumPy!")

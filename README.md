# Math for AI 🧮

My daily journey to master mathematics for Artificial Intelligence.

## 🎯 Goal

Build a strong mathematical foundation for ML/DL and prepare for a related MSc program.

## 📊 Progress

| Topic          | Status         | Notes                           |
| -------------- | -------------- | ------------------------------- |
| Linear Algebra | 🟡 In progress | vectors, matrices, eigen, SVD   |
| Calculus       | 🟡 In progress | derivatives, chain rule, Taylor |
| Probability    | ⚪ Not started | -                               |
| Optimization   | ⚪ Not started | -                               |

## 📁 Structure

math-for-ai/
├── 01-linear-algebra/ # vectors, matrices, eigen, SVD
├── 02-calculus/ # derivatives, gradients, Taylor, Newton
├── 03-probability/ # distributions, Bayes, MLE
├── 04-optimization/ # GD, SGD, Adam
├── 05-ml-applications/ # end-to-end implementations
├── Python_Visual_Debugger/ # visual debugger for math code
└── docs/ # notes

Each topic folder contains Jupyter notebooks with:

- A short mathematical explanation (LaTeX)
- A from-scratch implementation
- Numerical verification against NumPy
- Visualizations

## 🐍 Python_Visual_Debugger

A dedicated folder for **visual debugging** of mathematical code.

**Purpose:** When a piece of math code is hard to follow, I write a _step-by-step visual trace_ here. Instead of just running the final function, I print intermediate states, reshape arrays, and plot what is happening at each step.

**Why it exists:**

- Math code often hides the logic behind vectorized operations
- Printing intermediate values makes the flow obvious
- It is my personal learning tool, not part of the curriculum
- Useful for Gaussian elimination, backprop, gradient descent, etc.

**What goes here:**

- Step-by-step traces of algorithms (with `print` at each iteration)
- Small plots showing intermediate results
- Scratch files where I test one concept at a time
- Nothing here is polished — it is for understanding, not for show

## 📚 Resources

- Mathematics for Machine Learning (MML Book) — https://mml-book.github.io/
- 3Blue1Brown — Essence of Linear Algebra, Essence of Calculus
- MIT 18.06 (Gilbert Strang)
- CS229 (Stanford)

## 🔥 Daily Log

- **2026-09-28**: Added Taylor series and Newton's method
- **2026-09-27**: Added chain rule, Jacobian, Hessian
- **2026-09-26**: Finished eigenvalues
- **2026-09-25**: Rank and null space
- **2026-09-24**: Determinant and inverse

# 🧮 SLAE Pro Solver

A modern, high-performance Desktop application designed to solve **Systems of Linear Algebraic Equations (SLAE)**. Built with Python, NumPy, and Tkinter, it features a modular architecture and a sleek, dynamic user interface.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![NumPy](https://img.shields.io/badge/library-NumPy-orange)

---

## ✨ Features

* **🚀 Dynamic Grid Input**: Seamlessly adjust the system dimension $n$ (from 2 to 10). The input grid expands and contracts in real-time.
* **🧠 Multiple Solving Algorithms**:
    * **Direct Methods**: Cramer's Rule, Gaussian Elimination (with pivoting), Gauss-Jordan Elimination.
    * **Iterative Methods**: Jacobi Method, Gauss-Seidel Method.
* **✅ Robust Validation**: 
    * Automatic calculation of the matrix determinant.
    * Singularity detection (prevents errors on $det(A) = 0$).
    * Post-calculation verification via $AX = B$ check.
* **📁 File Integration**: Load complex matrices directly from `.txt` files with automated parsing.
* **🖱️ User-Centric Design**: Scrollable input areas for larger matrices and a clean, responsive layout.

---

## 🛠 Tech Stack

* **Language:** [Python](https://www.python.org/)
* **Matrix Operations:** [NumPy](https://numpy.org/)
* **GUI Framework:** [Tkinter](https://docs.python.org/3/library/tkinter.html)
* **Theming:** Custom CSS-like styling via `ttk` (Azure-compatible).

---

## 📂 Project Structure

The codebase is strictly modular to ensure scalability and ease of testing:

```text
├── main.py          # Entry point of the application
├── gui.py           # UI Logic and Grid Management
├── solvers.py       # Core mathematical algorithms (The "Engine")
├── requirements.txt # Project dependencies
├── .gitignore       # Git exclusion rules
└── test_data/       # Folder containing example .txt matrices

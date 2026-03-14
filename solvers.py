import numpy as np

def is_matrix_valid(A):
    """Checks if the matrix is non-singular (determinant is not zero)."""
    try:
        det = np.linalg.det(A)
        if np.isclose(det, 0):
            return False, "The matrix is singular (det=0)."
        return True, det
    except Exception as e:
        return False, f"Error calculating determinant: {e}"

def verify_solution(A, B, X, tol=1e-5):
    """Verifies the solution by checking if AX is approximately equal to B."""
    if X is None or np.any(np.isnan(X)):
        return False
    prediction = np.dot(A, X)
    return np.allclose(prediction, B, atol=tol)

def solve_cramer(A, B):
    """Solves SLAE using Cramer's rule."""
    n = len(B)
    if n > 5:
        raise ValueError("Cramer's method is limited to 5x5 dimension.")
    det_A = np.linalg.det(A)
    X = np.zeros(n)
    for i in range(n):
        A_temp = A.copy()
        A_temp[:, i] = B
        X[i] = np.linalg.det(A_temp) / det_A
    return X

def solve_gauss(A, B):
    """Solves SLAE using Gaussian elimination with partial pivoting."""
    n = len(B)
    M = np.hstack((A, B.reshape(-1, 1))).astype(float)
    for i in range(n):
        max_row = np.argmax(np.abs(M[i:n, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        pivot = M[i, i]
        if np.isclose(pivot, 0):
            continue
        M[i] = M[i] / pivot
        for j in range(i + 1, n):
            M[j] -= M[i] * M[j, i]
    X = np.zeros(n)
    for i in range(n - 1, -1, -1):
        X[i] = M[i, n] - np.dot(M[i, i + 1:n], X[i + 1:n])
    return X

def solve_gauss_jordan(A, B):
    """Solves SLAE using Gauss-Jordan elimination."""
    n = len(B)
    M = np.hstack((A, B.reshape(-1, 1))).astype(float)
    for i in range(n):
        max_row = np.argmax(np.abs(M[i:n, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        pivot = M[i, i]
        if np.isclose(pivot, 0):
            raise ValueError(f"Zero pivot encountered in column {i}.")
        M[i] = M[i] / pivot
        for j in range(n):
            if i != j:
                M[j] -= M[i] * M[j, i]
    return M[:, n]

def solve_jacobi(A, B, eps=1e-10, max_iter=100):
    """Solves SLAE using the Jacobi iterative method."""
    n = len(B)
    X = np.zeros(n)
    D = np.diag(A)
    if np.any(np.isclose(D, 0)):
        raise ValueError("Diagonal elements cannot be zero for Jacobi method.")
    R = A - np.diagflat(D)
    for k in range(max_iter):
        X_new = (B - np.dot(R, X)) / D
        if np.linalg.norm(X_new - X, ord=np.inf) < eps:
            return X_new
        X = X_new
    return X

def solve_seidel(A, B, eps=1e-10, max_iter=100):
    """Solves SLAE using the Gauss-Seidel iterative method."""
    n = len(B)
    X = np.zeros(n)
    for k in range(max_iter):
        X_old = X.copy()
        for i in range(n):
            sum_j = np.dot(A[i, :i], X[:i]) + np.dot(A[i, i + 1:], X_old[i + 1:])
            X[i] = (B[i] - sum_j) / A[i, i]
        if np.linalg.norm(X - X_old, ord=np.inf) < eps:
            return X
    return X
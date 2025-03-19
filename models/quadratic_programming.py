import numpy as np

class QuadraticProgrammingSolver:
    def __init__(self, Q, c, A, b):
        """
        Q: Матрица коэффициентов квадратичной формы (n x n)
        c: Вектор коэффициентов линейной части (n x 1)
        A: Матрица коэффициентов ограничений (m x n)
        b: Вектор ограничений (m x 1)
        """
        self.Q = np.array(Q, dtype=float)
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.n = self.Q.shape[0]  # количество переменных
        self.m = self.A.shape[0]  # количество ограничений
    
    def lagrangian(self, x, lambd):
        return 0.5 * x.T @ self.Q @ x + self.c.T @ x + lambd.T @ (self.A @ x - self.b)
    
    def compute_kkt_conditions(self, x, lambd):
        return self.Q @ x + self.c + self.A.T @ lambd, self.A @ x - self.b
    
    def initialize_simplex_tableau(self):
        tableau = np.zeros((self.m + 1, self.n + self.m + 1))
        tableau[:self.m, :self.n] = self.A
        tableau[:self.m, self.n:self.n + self.m] = np.eye(self.m)
        tableau[:self.m, -1] = self.b
        tableau[-1, :self.n] = -self.c
        return tableau
    
    def simplex_method(self):
        tableau = self.initialize_simplex_tableau()
        while any(tableau[-1, :-1] < 0):
            col = np.argmin(tableau[-1, :-1])
            row_candidates = tableau[:-1, -1] / tableau[:-1, col]
            row_candidates[tableau[:-1, col] <= 0] = np.inf
            row = np.argmin(row_candidates)
            tableau[row, :] /= tableau[row, col]
            for i in range(self.m + 1):
                if i != row:
                    tableau[i, :] -= tableau[i, col] * tableau[row, :]
        return tableau[:-1, -1]
    
    def solve(self):
        x_opt = self.simplex_method()
        x = np.zeros(self.n)
        lambd = np.zeros(self.m)
        grad_x, grad_lambd = self.compute_kkt_conditions(x, lambd)
        return x_opt, lambd, grad_x, grad_lambd

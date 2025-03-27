from scipy.optimize import minimize
import numpy as np

class QuadraticProgrammingSolver:
    def __init__(self, Q, c, A, b):
        self.Q = np.array(Q, dtype=float)
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.n = self.Q.shape[0]

    def objective(self, x):
        return 0.5 * x.T @ self.Q @ x + self.c.T @ x

    def _make_constraint(self, A_i, b_i):
        return {'type': 'ineq', 'fun': lambda x, A=A_i, b=b_i: b - A @ x}

    def constraint_functions(self):
        return [self._make_constraint(self.A[i], self.b[i]) for i in range(self.A.shape[0])]

    def solve(self):
        x0 = np.zeros(self.n)
        constraints = self.constraint_functions()
        result = minimize(self.objective, x0, method='SLSQP', constraints=constraints)
        return result

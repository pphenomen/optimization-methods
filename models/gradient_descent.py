import numpy as np

class GradientDescent:
    def __init__(self, func, x0, y0, learning_rate=0.1, tol=1e-6, max_iter=100, h=1e-5):
        self.func = func
        self.x0 = x0
        self.y0 = y0
        self.learning_rate = learning_rate
        self.tol = tol
        self.max_iter = max_iter
        self.h = h
        self.history = []

    def _gradient(self, x, y):
        df_dx = (self.func(x + self.h, y) - self.func(x - self.h, y)) / (2 * self.h)
        df_dy = (self.func(x, y + self.h) - self.func(x, y - self.h)) / (2 * self.h)
        return np.array([df_dx, df_dy])

    def run(self):
        current_point = np.array([self.x0, self.y0], dtype=np.float64)
        
        for i in range(self.max_iter):
            grad = self._gradient(*current_point)
            current_value = self.func(*current_point)
            grad_norm = np.linalg.norm(grad)

            if np.any(np.abs(grad) > 1e10):
                return self.history, False, "Функция расходится (градиент слишком большой)"

            self.history.append({
                'iteration': i + 1,
                'x': current_point[0],
                'y': current_point[1],
                'f_value': current_value,
                'grad_norm': grad_norm
            })

            if grad_norm < self.tol:
                return self.history, True, "Алгоритм сошелся"

            current_point -= self.learning_rate * grad  
        
        return self.history, False, "Достигнуто максимальное число итераций"
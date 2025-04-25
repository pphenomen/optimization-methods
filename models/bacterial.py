import numpy as np

class BacterialOptimization:
    def __init__(self, func, bounds, n_bacteria=50, n_iterations=200, step_size=0.1, mutation_rate=0.1, attraction=0.5, repulsion=0.5):
        self.func = func
        self.bounds = bounds
        self.n_bacteria = n_bacteria
        self.n_iterations = n_iterations
        self.step_size = step_size
        self.mutation_rate = mutation_rate
        self.attraction = attraction
        self.repulsion = repulsion
        self.history = []
        self.best_solution = None

    def _initialize_population(self):
        population = np.random.uniform(self.bounds[0][0], self.bounds[0][1], (self.n_bacteria, len(self.bounds)))
        return population

    def _evaluate(self, population):
        return np.array([self.func(*ind) for ind in population])

    def _move_bacteria(self, population, scores):
        best_score = np.max(scores)
        best_bacteria = population[np.argmax(scores)]

        for i in range(self.n_bacteria):
            if scores[i] > best_score:  # раздражение
                population[i] -= self.repulsion * np.random.rand(*population[i].shape)
            else:  # атррактант
                population[i] += self.attraction * (best_bacteria - population[i])

        population = np.clip(population, [b[0] for b in self.bounds], [b[1] for b in self.bounds])
        return population

    def _mutate(self, population):
        for i in range(self.n_bacteria):
            if np.random.rand() < self.mutation_rate:
                mutation_vector = np.random.uniform(-1, 1, size=population[i].shape)
                population[i] += mutation_vector * self.step_size
        return population

    def optimize(self):
        population = self._initialize_population()
        best_solution = None
        best_score = float('inf')

        for i in range(self.n_iterations):
            scores = self._evaluate(population)
            best_solution = population[np.argmin(scores)]
            best_score = np.max(scores)

            population = self._move_bacteria(population, scores)
            population = self._mutate(population)

            self.history.append({
                'iteration': i,
                'population': population,
                'best_solution': best_solution,
                'best_score': best_score
            })

        return best_solution, self.history

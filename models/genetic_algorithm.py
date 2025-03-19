import numpy as np

class GeneticAlgorithm:
    def __init__(self, func, pop_size=50, mutation_rate=0.1, generations=100, x_bounds=(-2, 2), y_bounds=(-1, 3)):
        self.func = func
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.population = self._initialize_population()
        self.history = []

    @staticmethod
    def rosenbrock(x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    def _initialize_population(self):
        x_vals = np.random.uniform(self.x_bounds[0], self.x_bounds[1], self.pop_size)
        y_vals = np.random.uniform(self.y_bounds[0], self.y_bounds[1], self.pop_size)
        return np.column_stack((x_vals, y_vals))

    def _fitness(self, population):
        return np.array([self.rosenbrock(ind[0], ind[1]) for ind in population])

    def _selection(self, population, fitness_values):
        sorted_indices = np.argsort(fitness_values)
        return population[sorted_indices[:len(population) // 2]]

    def _crossover(self, parents):
        offspring = []
        for _ in range(self.pop_size - len(parents)):
            p1, p2 = parents[np.random.choice(len(parents), 2, replace=False)]
            alpha = np.random.rand()
            child = alpha * p1 + (1 - alpha) * p2  # арифметический кроссовер
            offspring.append(child)
        return np.vstack((parents, np.array(offspring)))

    def _mutate(self, population):
        for i in range(len(population)):
            if np.random.rand() < self.mutation_rate:
                population[i][0] += np.random.uniform(-0.1, 0.1)
                population[i][1] += np.random.uniform(-0.1, 0.1)
                population[i][0] = np.clip(population[i][0], self.x_bounds[0], self.x_bounds[1])
                population[i][1] = np.clip(population[i][1], self.y_bounds[0], self.y_bounds[1])
        return population

    def run(self):
        for _ in range(self.generations):
            fitness_values = self._fitness(self.population)
            best_idx = np.argmin(fitness_values)
            self.history.append([self.population[best_idx][0], self.population[best_idx][1], fitness_values[best_idx]])

            selected = self._selection(self.population, fitness_values)
            offspring = self._crossover(selected)
            self.population = self._mutate(offspring)

        best_solution = min(self.history, key=lambda x: x[2])
        return best_solution, np.array(self.history)
import numpy as np
import random

class ImmuneAlgorithm:
    def __init__(self, func, bounds, n_antibodies=50, n_iterations=200, n_best=10, n_random=10, n_clones=20, mutation_rate=0.2):
        self.func = func
        self.bounds = bounds
        self.n_antibodies = n_antibodies
        self.n_iterations = n_iterations
        self.n_best = n_best
        self.n_random = n_random
        self.n_clones = n_clones
        self.mutation_rate = mutation_rate
        self.history = []

    def _initialize_population(self):
        return [self._random_solution() for _ in range(self.n_antibodies)]

    def _random_solution(self):
        return np.array([np.random.uniform(low, high) for low, high in self.bounds])

    def _evaluate(self, population):
        return [self.func(*ind) for ind in population]

    def _clone_and_mutate(self, best):
        clones = []
        for antibody in best:
            for _ in range(self.n_clones):
                clone = antibody + np.random.normal(0, self.mutation_rate, size=len(antibody))
                clone = np.clip(clone, [b[0] for b in self.bounds], [b[1] for b in self.bounds])
                clones.append(clone)
        return clones

    def _select_best(self, population, scores, n):
        sorted_indices = np.argsort(scores)
        return [population[i] for i in sorted_indices[:n]]

    def optimize(self):
        population = self._initialize_population()
        for i in range(self.n_iterations):
            scores = self._evaluate(population)
            best = self._select_best(population, scores, self.n_best)

            clones = self._clone_and_mutate(best)
            clone_scores = self._evaluate(clones)
            selected_clones = self._select_best(clones, clone_scores, self.n_best)

            random_antibodies = [self._random_solution() for _ in range(self.n_random)]
            population = selected_clones + random_antibodies

            best_solution = min(population, key=lambda x: self.func(*x))
            best_score = self.func(*best_solution)

            self.history.append({
                'iteration': i,
                'population': population.copy(),
                'best': best_solution.copy(),
                'score': best_score
            })

        return self.history[-1]['best'], self.history

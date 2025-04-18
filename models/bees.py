import numpy as np
import random

class BeesAlgorithm:
    def __init__(self, func, n_bees=50, n_elite=3, n_selected=10,
                 n_recruited_elite=7, n_recruited_selected=3, max_iter=100,
                 bounds=((-5, 5), (-5, 5)), radius=0.1):
        self.func = func
        self.n_bees = n_bees
        self.n_elite = n_elite
        self.n_selected = n_elite + n_selected
        self.n_recruited_elite = n_recruited_elite
        self.n_recruited_selected = n_recruited_selected
        self.max_iter = max_iter
        self.bounds = bounds
        self.radius = radius
        self.history = []

    def random_bee(self):
        x = np.random.uniform(*self.bounds[0])
        y = np.random.uniform(*self.bounds[1])
        return [x, y, self.func(x, y)]

    def neighborhood_search(self, center):
        x = np.clip(center[0] + np.random.uniform(-self.radius, self.radius), *self.bounds[0])
        y = np.clip(center[1] + np.random.uniform(-self.radius, self.radius), *self.bounds[1])
        return [x, y, self.func(x, y)]

    def optimize(self):
        population = [self.random_bee() for _ in range(self.n_bees)]

        for iteration in range(self.max_iter):
            population.sort(key=lambda b: b[2])
            new_population = []

            iteration_data = {
                'elite': [],
                'selected': [],
                'scouts': [],
                'best': None,
                'step': iteration + 1
            }

            # элитные участки
            for i in range(self.n_elite):
                site = population[i]
                recruits = [self.neighborhood_search(site) for _ in range(self.n_recruited_elite)]
                best_local = min(recruits + [site], key=lambda b: b[2])
                new_population.append(best_local)
                iteration_data['elite'].extend(recruits)

            # отобранные участки (неэлитные)
            for i in range(self.n_elite, self.n_selected):
                site = population[i]
                recruits = [self.neighborhood_search(site) for _ in range(self.n_recruited_selected)]
                best_local = min(recruits + [site], key=lambda b: b[2])
                new_population.append(best_local)
                iteration_data['selected'].extend(recruits)

            remaining = self.n_bees - len(new_population)
            scouts = [self.random_bee() for _ in range(remaining)]
            new_population += scouts
            iteration_data['scouts'] = scouts

            population = new_population
            iteration_data['best'] = min(population, key=lambda b: b[2])
            self.history.append(iteration_data)

        best = min(population, key=lambda b: b[2])
        return best, self.history

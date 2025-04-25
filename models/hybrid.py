import numpy as np
from models.genetic import GeneticAlgorithm
from models.bees import BeesAlgorithm

class HybridOptimization:
    def __init__(self, func, generations=50):
        self.func = func
        self.generations = generations
        self.history = []

        self.genetic = GeneticAlgorithm(func, generations=generations)
        self.bees = BeesAlgorithm(func, max_iter=generations)

    def run(self):
        pop = self.genetic._initialize_population()

        for gen in range(self.generations):
            fitness = self.genetic._fitness(pop)
            selected = self.genetic._selection(pop, fitness)
            offspring = self.genetic._crossover(selected)
            mutated = self.genetic._mutate(offspring)

            # локальный поиск лучшими
            best_points = [list(ind) + [self.func(ind[0], ind[1])] for ind in selected[:self.bees.n_elite]]
            self.bees.radius = self.bees.radius or 0.05
            self.bees.bounds = (self.genetic.x_bounds, self.genetic.y_bounds)
            refined = [self.bees.neighborhood_search(p) for p in best_points]

            updated_population = mutated[:len(mutated) - len(refined)]
            updated_population = np.vstack((updated_population, np.array([r[:2] for r in refined])))
            pop = updated_population

            best_idx = np.argmin(self.genetic._fitness(pop))
            best = pop[best_idx]
            best_value = self.func(best[0], best[1])

            self.history.append({
                "iteration": gen,
                "population": pop.copy(),
                "best": best.copy(),
                "score": best_value
            })

        return best, self.history

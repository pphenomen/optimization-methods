import numpy as np

class ParticleSwarmOptimizer:
    def __init__(self, func, num_particles=30, dimensions=2, bounds=None,
                 inertia=0.7, cognitive=1.5, social=2.0, iterations=100):
        self.func = func
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.iterations = iterations

        self.inertia = inertia
        self.cognitive = cognitive  # фp — "ностальгия"
        self.social = social        # фg — "инстинкт стаи"

        self.bounds = bounds if bounds else [(-5, 5)] * dimensions
        self.init_particles()

        self.global_best_pos = None
        self.global_best_val = float('inf')
        self.history = []

    def init_particles(self):
        self.positions = np.array([
            [np.random.uniform(low, high) for (low, high) in self.bounds]
            for _ in range(self.num_particles)
        ])
        self.velocities = np.zeros((self.num_particles, self.dimensions))
        self.personal_best_pos = np.copy(self.positions)
        self.personal_best_val = np.array([self.func(*p) for p in self.positions])

    def optimize(self):
        for _ in range(self.iterations):
            for i in range(self.num_particles):
                val = self.func(*self.positions[i])
                if val < self.personal_best_val[i]:
                    self.personal_best_val[i] = val
                    self.personal_best_pos[i] = self.positions[i]

                if val < self.global_best_val:
                    self.global_best_val = val
                    self.global_best_pos = self.positions[i]

            r_p = np.random.rand(self.num_particles, self.dimensions)
            r_g = np.random.rand(self.num_particles, self.dimensions)

            cognitive_term = self.cognitive * r_p * (self.personal_best_pos - self.positions)
            social_term = self.social * r_g * (self.global_best_pos - self.positions)
            self.velocities = self.inertia * self.velocities + cognitive_term + social_term

            self.positions += self.velocities

            # Apply bounds
            for d in range(self.dimensions):
                self.positions[:, d] = np.clip(self.positions[:, d],
                                               self.bounds[d][0], self.bounds[d][1])

            self.history.append((self.global_best_pos.copy(), self.global_best_val))

        return self.global_best_pos, self.global_best_val, self.history
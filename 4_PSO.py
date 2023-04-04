import numpy as np
import matplotlib.pyplot as plt

class Particle:
    def __init__(self, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1])
        self.velocity = np.random.uniform(-1, 1)
        self.best_position = self.position
        self.best_fitness = np.inf

    def update_position(self):
        self.position += self.velocity

    def update_velocity(self, w, c1, c2, global_best_position):
        r1, r2 = np.random.uniform(0, 1, 2)
        social_component = c1 * r1 * (global_best_position - self.position)
        cognitive_component = c2 * r2 * (self.best_position - self.position)
        self.velocity = w * self.velocity + social_component + cognitive_component

    def evaluate_fitness(self):
        return np.sin(self.position)

    def update_best_position(self):
        fitness = self.evaluate_fitness()
        if fitness < self.best_fitness:
            self.best_position = self.position
            self.best_fitness = fitness

def run_pso(bounds, num_particles, max_iterations, w, c1, c2):
    particles = [Particle(bounds) for _ in range(num_particles)]
    global_best_position = np.inf
    global_best_fitness = np.inf
    for i in range(max_iterations):
        for particle in particles:
            particle.update_velocity(w, c1, c2, global_best_position)
            particle.update_position()
            fitness = particle.evaluate_fitness()
            if fitness < global_best_fitness:
                global_best_position = particle.position
                global_best_fitness = fitness
            particle.update_best_position()
        print(f'Iteration {i+1}: Best fitness = {global_best_fitness:.6f}')
    return global_best_position, global_best_fitness

#parameters
bounds = [-5, 5]
num_particles = 20
max_iterations = 50
w = 0.729
c1 = 1.494
c2 = 1.494


best_position, best_fitness = run_pso(bounds, num_particles, max_iterations, w, c1, c2)

#result
x = np.linspace(bounds[0], bounds[1], 1000)
y = np.sin(x)
plt.plot(x, y, label='sin(x)')
plt.plot(best_position, best_fitness, 'ro', label='Optimum')
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

def function(x):
    return x * np.sin(10 * np.pi * x) + 2

def generate_population(size, resolution):
    return np.array([[np.random.randint(2) for _ in range(resolution)] for _ in range(size)])

def decode(individual):
    return LOWER + (UPPER - LOWER) * sum([bit * 2**i for i, bit in enumerate(reversed(individual))]) / (2**len(individual) - 1)

def fitness_func(individual):
    return function(decode(individual))

def mutate(individual, mutation_rate):
    return [not bit if np.random.random() < mutation_rate else bit for bit in individual]

def reproduce(individual1, individual2, mutation_rate):
    split_point = np.random.randint(len(individual1))
    child1 = np.concatenate((individual1[:split_point], individual2[split_point:]))
    child2 = np.concatenate((individual2[:split_point], individual1[split_point:]))
    return [mutate(child1, mutation_rate), mutate(child2, mutation_rate)]

def form_next_population(population, mutation_rate):
    population_size = len(population)
    fitness_values = [fitness_func(individual) for individual in population]
    sorted_population = [x for _, x in sorted(zip(fitness_values, population), reverse=True)]
    next_population = sorted_population[:SIZE]
    for i, individual1 in enumerate(sorted_population):
        for _, individual2 in enumerate(sorted_population[i+1:], start=i+1):
            children = reproduce(individual1, individual2, mutation_rate)
            for child in children:
                if child.tolist() not in next_population.tolist():
                    next_population = np.append(next_population, [child], axis=0)
                    if len(next_population) == SIZE:
                        return next_population
    return next_population

LOWER, UPPER, SIZE = -1, 2, 10
POP_SIZE, RESOLUTION, MUTATION_RATE = 10, 7, 0.01
POP = generate_population(POP_SIZE, RESOLUTION)
generation = 0

x = np.linspace(LOWER, UPPER, 2**7)
y = function(x)

while True:
    fitness_values = [fitness_func(individual) for individual in POP]
    individuals = [decode(individual) for individual in POP]
    plt.title(f"Generation {generation}")
    plt.plot(x, y)
    plt.scatter(individuals, fitness_values)
    plt.plot(individuals, fitness_values)
    plt.show()
    POP = form_next_population(POP, MUTATION_RATE)
    generation += 1

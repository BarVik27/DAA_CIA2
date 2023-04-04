import random
import numpy as np
import matplotlib.pyplot as plt


cities = {
    'A': (1, 1),
    'B': (3, 1),
    'C': (3, 3),
    'D': (1, 3),
    'E': (2, 2)
}


POPULATION_SIZE = 50
ELITE_SIZE = 5
MUTATION_RATE = 0.01
NUM_GENERATIONS = 1000


def calc_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def calc_path_distance(path):
    distance = 0
    for i in range(len(path)-1):
        distance += calc_distance(cities[path[i]], cities[path[i+1]])
    distance += calc_distance(cities[path[-1]], cities[path[0]])
    return distance

def calc_fitness(path):
    return 1 / calc_path_distance(path)


def create_individual():
    path = list(cities.keys())
    random.shuffle(path)
    return path

def create_population(size):
    population = []
    for i in range(size):
        population.append(create_individual())
    return population

def rank_population(population):
    ranked_population = sorted(population, key=calc_fitness, reverse=True)
    return ranked_population

def select_parents(population):
    parent1 = random.choice(population[:ELITE_SIZE])
    parent2 = random.choice(population[:ELITE_SIZE])
    return parent1, parent2

def crossover(parent1, parent2):
   
    start = random.randint(0, len(parent1)-1)
    end = random.randint(start, len(parent1)-1)
    child = [None] * len(parent1)
    for i in range(start, end+1):
        child[i] = parent1[i]
    for i in range(len(parent2)):
        if parent2[i] not in child:
            for j in range(len(child)):
                if child[j] is None:
                    child[j] = parent2[i]
                    break
    return child

def mutate(individual):
   
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, len(individual)-1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def create_new_population(population):
    new_population = []
    while len(new_population) < len(population):
        parent1, parent2 = select_parents(population)
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
    return new_population


population = create_population(POPULATION_SIZE)
best_distances = []
for i in range(NUM_GENERATIONS):
    population = rank_population(population)
    best_path = population[0]
    best_distance = calc_path_distance(best_path)
    best_distances.append(best_distance)
    print(f'Generation {i}: Best Distance = {best_distance}')
    population = create_new_population(population)


plt.plot(best_distances)
plt.xlabel('Generation')
plt.ylabel('Best Distance')
plt.show()


best_path.append(best_path[0]) # close the

import random
import math


n = 10

distance_matrix = [[0, 12, 3, 23, 1, 5, 23, 56, 12, 11],
                   [12, 0, 9, 18, 3, 41, 45, 5, 41, 27],
                   [3, 9, 0, 89, 56, 21, 12, 48, 14, 29],
                   [23, 18, 89, 0, 87, 46, 75, 17, 50, 42],
                   [1, 3, 56, 87, 0, 55, 22, 86, 14, 36],
                   [5, 41, 21, 46, 55, 0, 21, 76, 54, 81],
                   [23, 45, 12, 75, 22, 21, 0, 11, 57, 48],
                   [56, 5, 48, 17, 86, 76, 11, 0, 63, 24],
                   [12, 41, 14, 50, 14, 54, 57, 63, 0, 9],
                   [11, 27, 29, 42, 36, 81, 48, 24, 9, 0]]


culture_count = 5
culture_pool = []
for i in range(culture_count):
    culture_pool.append([random.sample(range(n), n)])


population_size = 20
max_generations = 100
elite_size = 5
mutation_rate = 0.1



def route_distance(route):
    dist = 0
    for i in range(n - 1):
        dist += distance_matrix[route[i]][route[i + 1]]
    dist += distance_matrix[route[n - 1]][route[0]]
    return dist



def evaluate_fitness(solution):
    return 1 / route_distance(solution)



def generate_new_solution():
    parent1 = random.choice(culture_pool)
    parent2 = random.choice(culture_pool)
    child = []
    for i in range(n):
        if random.random() < 0.5:
            child.append(parent1[0][i])
        else:
            child.append(parent2[0][i])
    return child



def generate_new_population():
    population = []
    while len(population) < population_size:
        solution = generate_new_solution()
        population.append(solution)
    return population



def mutate_solution(solution):
    for i in range(n):
        if random.random() < mutation_rate:
            j = random.randint(0, n - 1)
            temp = solution[i]
            solution[i] = solution[j]
            solution[j] = temp
    return solution



def cultural_algorithm():
   
    for generation in range(max_generations):
        print("Generation", generation + 1)

      
        fitness_scores = []
        for solution in culture_pool:
            fitness_scores

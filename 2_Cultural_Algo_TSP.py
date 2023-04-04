import numpy as np

# Define parameters
cities = 10
population_size = 50
total_generations = 50
elite_number = 2
total_cultures = 5
total_immigrants = 2
mutate_prob = 0.02
crossover_prob = 0.7

# Create distance matrix
np.random.seed(42)
distances = np.random.randint(1, 101, size=(cities, cities))
np.fill_diagonal(distances, 0)

# Define fitness function
def fitness(individual):
    return -np.sum([distances[individual[i], individual[(i+1)%cities]] for i in range(cities)])

# Define selection function using roulette wheel selection
def roulette_wheel_selection(population, fitness_value):
    fitness_sum = np.sum(fitness_value)
    fitness_prob = fitness_value / fitness_sum
    cum_prob = np.cumsum(fitness_prob)
    selected_index = []
    for i in range(len(population)):
        val = np.random.rand()
        for j in range(len(cum_prob)):
            if val <= cum_prob[j]:
                selected_index.append(j)
                break
    return [population[i] for i in selected_index]

# Define crossover function
def crossover(parent1, parent2):
    child = [-1] * cities
    crossover_point = np.random.randint(1, cities)
    child[:crossover_point] = parent1[:crossover_point]
    for i in range(crossover_point, cities):
        if parent2[i] not in child:
            child[i] = parent2[i]
    for i in range(crossover_point):
        if parent2[i] not in child:
            for j in range(cities):
                if child[j] == -1:
                    child[j] = parent2[i]
                    break
    return child

# Define mutation function
def mutate(individual):
    if np.random.rand() < mutate_prob:
        i, j = np.random.randint(cities, size=2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Initialize populations for each culture
populations = [[np.random.permutation(cities) for _ in range(population_size)] for _ in range(total_cultures)]

# Start evolution process
for generation in range(total_generations):
    elites = []
    for population in populations:
        fitness_value = [fitness(individual) for individual in population]
        elites_index = np.argsort(fitness_value)[-elite_number:]
        elites.append([population[i] for i in elites_index])
    # Combine the elites into a single population
    elite_population = [individual for elite in elites for individual in elite]
    # Generate immigrants
    immigrants = [np.random.permutation(cities) for _ in range(total_immigrants)]
    # Combine the population and immigrants
    populations = [elite_population] + populations[:-1] + [immigrants]
   
    # Perform recombination
    new_populations = []
    for population in populations:
        new_population = []
        while len(new_population) < population_size:
            fitness_value = [fitness(individual) for individual in population]
            sele_indi = roulette_wheel_selection(population, fitness_value)
            individual1, individual2 = sele_indi[:2]
            child = crossover(individual1, individual2) if np.random.rand() < crossover_prob else individual1
            new_population.append(mutate(child))
        new_populations.append(new_population)
    populations = new_populations
   
    # Display the best fitness in each culture
    for i, population in enumerate(populations):
        fitness_values = [fitness(individual) for individual in population]
        print(f"Culture {i}: Best Fitness = {np.max(fitness_values)}")


all_solutions = [individual for population in populations for individual in population]
best_solution = max(all_solutions, key=fitness)
print("Best solution found:", best_solution)
print("Fitness of the best solution:", fitness(best_solution))
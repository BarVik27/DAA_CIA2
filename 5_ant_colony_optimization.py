import numpy as np
import random

#  adjacency matrix
graph = np.array([[0, 2, 3, 0, 0],
                  [2, 0, 0, 5, 6],
                  [3, 0, 0, 7, 0],
                  [0, 5, 7, 0, 4],
                  [0, 6, 0, 4, 0]])


num_ants = 10
alpha = 1.0
beta = 2.0
rho = 0.5
Q = 1.0


pheromone = np.ones(graph.shape) / len(graph)


def path_length(path):
    length = 0
    for i in range(len(path)-1):
        length += graph[path[i]][path[i+1]]
    return length


def update_pheromone(paths, lengths):
    pheromone *= (1-rho)
    for i in range(len(paths)):
        for j in range(len(paths[i])-1):
            pheromone[paths[i][j]][paths[i][j+1]] += Q/lengths[i]


for i in range(100):
    ant_paths = []
    ant_lengths = []
    for j in range(num_ants):
        
        path = [random.randint(0, len(graph)-1)]
       
        while len(path) < len(graph):
            
            prob = pheromone[path[-1]] ** alpha * (1/graph[path[-1]]) ** beta
            prob /= prob.sum()
           
            next_node = np.random.choice(range(len(graph)), p=prob)
          
            path.append(next_node)
       
        length = path_length(path)
        
        ant_paths.append(path)
        ant_lengths.append(length)
   
    update_pheromone(ant_paths, ant_lengths)
#  shortest path
shortest_path = ant_paths[np.argmin(ant_lengths)]
print('Shortest Path:', shortest_path)
print('Shortest Path Length:', min(ant_lengths))

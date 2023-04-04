import numpy as np

class AntColony:
    def __init__(self, size, density, start, end, alpha=1, beta=2, evap_rate=0.5, generations=100):
        self.size = size
        self.density = density
        self.start = start
        self.end = end
        self.alpha = alpha
        self.beta = beta
        self.evap_rate = evap_rate
        self.generations = generations
        
        self.graph = self.generate_problem(size, density)
        self.pheromones = np.ones((size, size))
        
    def generate_problem(self, size, density):
        graph = np.full((size, size), np.inf)
        for i in range(size):
            for j in range(i, size):
                if np.random.random() < density and i != j:
                    w = np.random.randint(1, 20)
                    graph[i][j] = w
                    graph[j][i] = w
        return graph
        
    def choose_next_vertex(self, curr_pos, visited):
        unvisited = np.where(visited == False)[0]
        graph = self.graph[curr_pos, unvisited]
        pheromones = self.pheromones[curr_pos, unvisited]
        weights = np.power(pheromones, self.alpha) * np.power(1 / graph, self.beta)
        weights /= np.sum(weights)
        next_vertex = np.random.choice(unvisited, p=weights)
        return next_vertex
        
    def traverse(self):
        curr_pos = self.start
        path = [curr_pos]
        visited = np.zeros(self.size, dtype=bool)
        visited[curr_pos] = True
        cost = 0
        
        while curr_pos != self.end:
            next_vertex = self.choose_next_vertex(curr_pos, visited)
            visited[next_vertex] = True
            cost += self.graph[curr_pos][next_vertex]
            path.append(next_vertex)
            curr_pos = next_vertex
            
        return path, cost
        
    def release_generation(self):
        paths, costs = [], []
        for i in range(self.size):
            path, cost = self.traverse()
            paths.append(path)
            costs.append(cost)
        return paths, costs
        
    def update_pheromones(self, paths, costs):
        self.pheromones *= (1 - self.evap_rate)
        for path, cost in zip(paths, costs):
            for i in range(len(path) - 1):
                curr_pos, next_pos = path[i], path[i+1]
                self.pheromones[curr_pos][next_pos] += 1 / cost
        
    def run(self):
        for i in range(self.generations):
            paths, costs = self.release_generation()
            self.update_pheromones(paths, costs)
            best_path, best_cost = paths[np.argmin(costs)], np.min(costs)
            print(f"Generation {i+1}, Best Path: {best_path}, Cost: {best_cost}")



ac = AntColony(size=10, density=0.5, start=0, end=7)
ac.run()
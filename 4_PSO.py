import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 1 + 2*x - x**2

def PSO(f, n_particles=50, n_iterations=100, c1=2, c2=2, w=0.7):
    x_min, x_max = -10, 10
    particles = np.random.uniform(x_min, x_max, size=(n_particles, 1))
    velocities = np.zeros((n_particles, 1))
    best_positions = particles.copy()
    best_scores = f(best_positions)
    
    global_best_position = best_positions[np.argmax(best_scores)]
    global_best_score = np.max(best_scores)
    
    for i in range(n_iterations):
        r1 = np.random.uniform(size=(n_particles, 1))
        r2 = np.random.uniform(size=(n_particles, 1))
        
        velocities = w * velocities \
                    + c1 * r1 * (best_positions - particles) \
                    + c2 * r2 * (global_best_position - particles)
        particles += velocities
        particles = np.clip(particles, x_min, x_max)
        
        scores = f(particles)
        improved_indices = scores > best_scores
        best_positions[improved_indices] = particles[improved_indices]
        best_scores[improved_indices] = scores[improved_indices]
        
        if np.max(best_scores) < global_best_score:
            global_best_score = np.max(best_scores)
            global_best_position = best_positions[np.argmax(best_scores)]
            
    plt.plot(particles, f(particles), 'bo', label='particles')
    plt.plot(best_positions, f(best_positions), 'ro', label='best positions')
    plt.plot(global_best_position, global_best_score, 'go', label='global best')
    plt.legend()
    plt.xlim(x_min, x_max)
    plt.ylim(-100, 100)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'PSO: x={global_best_position[0]:.2f}, f(x)={global_best_score:.2f}')
    plt.show()
        
    return global_best_position, global_best_score
    
best_position, best_score = PSO(f)
print(f'The maximum of f(x) = 1+2x-x^2 is at x = {best_position[0]:.2f}, with a value of {best_score:.2f}.')

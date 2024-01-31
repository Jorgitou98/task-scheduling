import random
import numpy as np

def get_input_sizes(num_task_test = False):
    if num_task_test:
        n_inf = int(input("Minimum number of task: "))
        n_sup = int(input("Maximum number of task: "))
        reps = int(input("Repetition of each task size: "))
        task_sizes = (n_inf, n_sup, reps)
    else:
        reps = int(input("Number of repetition: "))
        n = int(input("Number of task: "))
        task_sizes = n, reps
    # Number of processors
    m = int(input("Number of processors: "))
    # Epsilon for extra approximation error
    epsilon = float(input("Epsilon: "))

    return task_sizes, m, epsilon


# Generate inputs for the problem
def generate_tasks(n, m):
    # Time of each task using one processor
    times_one = [random.uniform(5, 100) for _ in range(n)]
    # times_one = [random.uniform(5, 10) for _ in range(7*n//8)] + [random.uniform(1000, 2000) for _ in range(n//8)]
    # Recursive and random generate decrasing times for many processor
    def rand_multiprocess_times(last_time, p):
        if p >= m:
            return []
        random_factor = np.clip(random.gauss(0.5, 0.5), 0, 1)
        new_time = (p + random_factor) / (p + 1) * last_time
        return [new_time] +  rand_multiprocess_times(new_time, p + 1)
    # Add time for each task with more processors (monotony property)
    times = [[time_one] + rand_multiprocess_times(time_one, 1) for time_one in times_one]
    return times

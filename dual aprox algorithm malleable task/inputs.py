import random
import numpy as np

# Generate inputs for de problem
def get_inputs():
    # Number of task
    n = int(input("Number of task: "))
    # Number of processors
    m = int(input("Number of processors: "))
    # Epsilon for extra approximation error
    epsilon = float(input("Epsilon: "))

    # Time of each task using one processor
    times_one = [random.uniform(5, 1000) for _ in range(n)]
    # Recursive an random generate decrasing times for many processor
    def rand_multiprocess_times(last_time, p):
        if p > m:
            return []
        random_factor = np.clip(random.gauss(0.5, 0.5), 0, 1)
        new_time = (p + random_factor) / (p + 1) * last_time
        return [new_time] +  rand_multiprocess_times(new_time, p + 1)
    # Add time for each task with more processors (monotony property)
    times = [[time_one] + rand_multiprocess_times(time_one, 2) for time_one in times_one]
    print("Task times: ", times)
    return n, m, epsilon, times

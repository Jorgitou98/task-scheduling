import random
import numpy as np


# Generate inputs for the problem
def generate_tasks():
    n = int(input("Number of task: "))
    m = 4
    # Time of each task using one processor
    times = [{1: random.uniform(5, 1000)} for _ in range(n)]
    # Recursive and random generate decrasing times for many processor
    def rand_multiprocess_times(task_t):
        for p in range(1, 4):
            random_factor = np.clip(random.gauss(0.1, 0.1), 0, 1)
            task_t[p+1] = (p + random_factor) / (p + 1) * task_t[p]
        del task_t[3]
        return task_t
    # Add time for each task with more processors (monotony property)
    times = [rand_multiprocess_times(task_t) for task_t in times]
    return times

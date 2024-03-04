import random
import numpy as np
from pprint import pprint
def generate_tasks():
    available_devices = ["A30", "A100"]
    while True:
        device = input("Goal device (A30 or A100): ")
        if device in available_devices:
            break
    n = int(input("Number of task (n): "))
    perc_available = 100

    instance_sizes = [1,2,4] if device == "A30" else [1,2,3,4,7] if device == "A100" else None
    perc_scale = {}
    for size in instance_sizes:
        perc = float(input(f"Percentage scale until {size} slices (0-{perc_available}%): "))
        assert(0 <= perc and perc <= perc_available)
        perc_scale[size] = perc
        perc_available -= perc
    perc_membound = float(input("Percentage memory bound (0-100%): "))
    assert(0 <= perc and perc <= 100)
    n_slices = instance_sizes[-1]
    times = []
    for scale_size in instance_sizes:
        n_instance_scale_size = int(n * perc_scale[scale_size] / 100)
        times_instance_scale_size =  [[(1, random.uniform(4, 10))] for _ in range(n_instance_scale_size)]
        n_mem_bound = n_instance_scale_size * perc_membound // 100
        for i in range(n_instance_scale_size):
            super_linear_grow = i < n_mem_bound
            for size in range(2, n_slices+1):
                _, last_time = times_instance_scale_size[i][-1]
                # Escala mal
                if size > scale_size:
                    next_time = (size - 1 + np.clip(np.random.normal(0.75, 0.25), 0.5, 1)) / size * last_time
                # Si sigue siendo memory bound y hemos escalado en memoria (de 3 a 4 slices no se escala en A100)
                elif super_linear_grow and device == "A100" and size != 4:
                    next_time = (size - 1 + np.clip(np.random.normal(-0.25, 0.25), -0.5, 0)) / size * last_time
                    if random.random() <= 0.7:
                        super_linear_grow = False
                else:
                    next_time = (size - 1 + np.clip(np.random.normal(0.1, 0.05), 0, 0.2)) / size * last_time

                times_instance_scale_size[i].append((size, next_time))
        times += times_instance_scale_size
        # Remove times of isntance sizes not valid
        times = [[(slices, time) for slices, time in task_times if slices in instance_sizes] for task_times in times]
        pprint(times)
    return device, times, instance_sizes

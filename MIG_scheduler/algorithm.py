from pprint import pprint

def create_allotments_family(times, instance_sizes):
    # Función para calcular el trabajo de una tarea con ciertos gpcs
    def work(time_task):
        slices, time = time_task
        return slices * time
    allotmets_family = [[min(times_task, key=work) for times_task in times]]

    n_slices = instance_sizes[-1]
    while True:
        allotment_prev = allotmets_family[-1]
        index_max_time = max(enumerate(allotment_prev), key=lambda x: x[1][1])[0]
        num_slices, time = allotment_prev[index_max_time]
        if num_slices == n_slices:
            break
        allotment_curr = allotment_prev.copy()
        more_slices_task = [(slices, time) for slices, time in times[index_max_time] if slices > num_slices]
        allotment_curr[index_max_time] = min(more_slices_task, key=work)
        allotmets_family.append(allotment_curr)
    print("\n\nAllotments family\n\n")
    pprint(allotmets_family)
    return allotmets_family
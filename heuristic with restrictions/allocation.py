
def _alloc_makespan_lb(times, m = 4):
    # Minimum number of processors to not exising a given limit for each task
    min_proc_time = lambda task_t, limit: min([i for i, time in list(task_t.items()) + [(float("inf"), 0)] if time <= limit])
    min_proc_tasks = lambda limit: [min_proc_time(task_t, limit) for task_t in times]
    # Work of tasks for a given limit
    work = lambda limit : sum(min_proc * times[i][min_proc] if min_proc < float("inf") else float("inf") for i, min_proc in enumerate(min_proc_tasks(limit))) / m

    possible_times = [time for task_t in times for time in task_t.values()]
    possible_times.sort()
    index_lb = 0
    index_ub = len(possible_times) - 1
    lb_makespan_opt = float("inf")
    best_allocation = None
    while index_lb <= index_ub:
        index_middle = (index_lb + index_ub) // 2
        curr_work = work(possible_times[index_middle])
        # The lower bound of makespan result by minimizing the work and the max time
        if max(possible_times[index_middle], curr_work) < lb_makespan_opt:
            lb_makespan_opt = max(possible_times[index_middle], curr_work)
            best_allocation = min_proc_tasks(possible_times[index_middle])
        if possible_times[index_middle] > curr_work:
            index_ub = index_middle - 1
        else:
            index_lb = index_middle + 1

    return lb_makespan_opt, best_allocation
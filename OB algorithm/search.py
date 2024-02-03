import numpy as np
from itertools import chain
from assign import assign_plane_pos
from plotting import draw_shelve_stacked_rects

def _makespan_lower_bound(times, m):
    # Minimum number of processors to not exising a given limit for each task
    min_proc_time = lambda task_t, limit: next((i + 1 for i, time in enumerate(task_t) if time <= limit), float("inf"))
    min_proc_tasks = lambda limit: [min_proc_time(task_t, limit) for task_t in times]
    # Work of tasks for a given limit
    work = lambda limit : sum(min_proc * times[i][min_proc - 1] if min_proc < float("inf") else float("inf") for i, min_proc in enumerate(min_proc_tasks(limit))) / m

    possible_times = list(chain(*times))
    possible_times.sort()
    index_lb = 0
    index_ub = len(possible_times) - 1
    lb_makespan_opt = float("inf")
    while index_lb <= index_ub:
        index_middle = (index_lb + index_ub) // 2
        curr_work = work(possible_times[index_middle])
        # The lower bound of makespan result by minimizing the work and the max time
        lb_makespan_opt = min(lb_makespan_opt, max(possible_times[index_middle], curr_work))
        if possible_times[index_middle] > curr_work:
            index_ub = index_middle - 1
        else:
            index_lb = index_middle + 1
    return lb_makespan_opt

def schedule(times, m):
    times = sorted(times, key=lambda task: task[0], reverse=False)
    makespan_lb = _makespan_lower_bound(times, m)
    n = len(times)
    makespan = float("inf")
    lm_loc_sol, hm_loc_sol = None, None
    for k in range(n, -1, -1):
        times_lm = times[:k]
        times_hm = times[k:]
        real_makespan, lm_loc, hm_loc = assign_plane_pos(m, times_lm, times_hm)
        print("k:", k)
        #draw_shelve_stacked_rects(real_makespan, makespan_lb, m, lm_loc, hm_loc)
        if real_makespan < makespan:
            makespan = real_makespan
            lm_loc_sol, hm_loc_sol = lm_loc, hm_loc
    return makespan_lb, makespan, lm_loc_sol, hm_loc_sol
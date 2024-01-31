import heapq
import numpy as np
import copy

def _consecutive_processor_assign(first_proc, task_set, proc_time):
    for stacked_task in task_set:
            first_time = 0
            for task in stacked_task:
                task["x"] = first_proc
                task["y"] = first_time
                first_time += task["time"]
            for proc in range(first_proc, first_proc + task["num_proc"]):
                proc_time[proc] = first_time
            first_proc += task["num_proc"]
    return first_proc, task_set, proc_time

def _assign_to_less_load(task, proc_time):
    proc_less_load = min(proc_time, key=proc_time.get)
    task["x"] = proc_less_load
    task["y"] = proc_time[proc_less_load]
    proc_time[proc_less_load] += task["time"]
    return task, proc_time

def _max_sliding_window(dic, k):
	ans = []
	heap = []
      
	for i in range(k):
		heapq.heappush(heap, (-dic[i], i))

	# The maximum element in the first window
	ans.append(-heap[0][0])
	# Process the remaining elements
	for i in range(k, len(dic)):
		heapq.heappush(heap, (-dic[i], i))
		# Remove elements that are outside the current window
		while heap[0][1] <= i - k:
			heapq.heappop(heap)
		# The maximum element in the current window
		ans.append(-heap[0][0])
	return ans


def _assign_to_less_load_window(task, proc_time):
    win_max_times = _max_sliding_window(proc_time, task["num_proc"])
    min_time_max_win = min(win_max_times)
    first_proc_less_load = win_max_times.index(min_time_max_win)
    task["x"] = first_proc_less_load
    task["y"] = min_time_max_win
    for proc in range(first_proc_less_load, first_proc_less_load + task["num_proc"]):
        proc_time[proc] = min_time_max_win + task["time"]
    return task, proc_time

def _makespan_bounds(m, task_set, times):
    makespan_lb = 0
    makespan_ub = 0
    for task in task_set:
        makespan_ub += times[task["task_i"]][m-1]
        makespan_lb += times[task["task_i"]][0]
    makespan_lb /= m
    return makespan_lb, makespan_ub

def _multi_layer_sched(m, limit, critical_task, proc_time, times):
    # Copy for change locally before assign (possibily its not a valid solution)
    critical_task = copy.deepcopy(critical_task)
    proc_time = proc_time.copy()
    s = 0
    avp = m
    min_proc_time = lambda task_t, limit: next((i + 1 for i, time in enumerate(task_t) if time <= limit), float("inf")) 
    c = 0
    i = 0
    while i < len(critical_task):
        task = critical_task[i]
        proc_need = min_proc_time(times[task["task_i"]], limit)
        if proc_need <= avp:
            task["num_proc"] = proc_need
            task["x"] = m - avp
            task["y"] = s
            task["time"] = times[task["task_i"]][proc_need - 1]
            for proc in range(task["x"], task["x"] + proc_need):
                proc_time[proc] += task["time"]
            avp -= proc_need
            c = max(c, task["time"])
        elif proc_need > m:
            return False, None, None
        else:
             s += c
             limit -= c
             if limit <= 0:
                  return False, None, None
             c, avp = 0, m
             i -= 1
        i += 1
    return True, critical_task, proc_time


              

def _shorten_critical_task(m, critical_task, times, proc_time):
    # Assign tau_2: For 3/2-approximation it is not necessary to order decreasingly, but it works better like this
    critical_task = sorted(critical_task, key=lambda task: task["time"], reverse=True)
    makespan_lb, makespan_ub = _makespan_bounds(m = m, task_set = critical_task, times = times)
    makespan_space = np.arange(makespan_lb, makespan_ub + 0.02, 0.01)
    left_pos = 0
    right_pos = len(makespan_space) - 1
    best_tau2 = None
    best_proc_time = None
    while left_pos <= right_pos:
        middle_pos = (left_pos + right_pos) // 2
        possible, critical_task_sched, proc_time_sched = _multi_layer_sched(m, makespan_space[middle_pos], critical_task, proc_time, times)
        if possible:
            best_tau2 = critical_task_sched
            best_proc_time = proc_time_sched
            right_pos = middle_pos - 1 
        else:
            left_pos = middle_pos + 1
    return best_tau2, best_proc_time
              

def assign_plane_pos(m, sol, times):
    tau_0, tau_1, tau_2, tau_s = sol
    first_proc = 0
    proc_time = {i : 0 for i in range(m)}
    # Assign tau_2
    tau_2, proc_time = _shorten_critical_task(m, tau_s + tau_2, times, proc_time)
    # Assign tau_1
    tau_1 = sorted(tau_1, key=lambda task: task["time"], reverse=True)
    for task in tau_1:
        task, proc_time = _assign_to_less_load_window(task, proc_time)

    real_makespan = max(proc_time.values())
    return real_makespan, (tau_1, tau_2)
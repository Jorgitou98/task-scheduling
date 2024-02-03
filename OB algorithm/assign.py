import numpy as np
import heapq
from pprint import pprint
import copy

def _lpt_alg(times_lm, proc_time):
    n = len(times_lm)
    lm_loc = [{} for _ in range(n)]
    for loc, task_t in zip(lm_loc, times_lm):
        proc_less_load = min(proc_time, key=lambda proc: proc_time[proc][-1])
        loc["x"] = proc_less_load 
        loc["y"] = proc_time[proc_less_load][-1]
        loc["num_proc"] = 1
        loc["time"] = task_t[0]
        proc_time[proc_less_load].append(loc["y"] + loc["time"])
        loc["end_time"] = proc_time[proc_less_load][-1]
    return lm_loc, proc_time


def _max_sliding_window(dic, k):
	ans, heap = [], []
      
	for i in range(k):
		heapq.heappush(heap, (-dic[i][-1], i))

	# The maximum element in the first window
	ans.append(-heap[0][0])
	# Process the remaining elements
	for i in range(k, len(dic)):
		heapq.heappush(heap, (-dic[i][-1], i))
		# Remove elements that are outside the current window
		while heap[0][1] <= i - k:
			heapq.heappop(heap)
		# The maximum element in the current window
		ans.append(-heap[0][0])
	return ans



def _improve_critical_task(lm_loc, times_lm, proc_time):
    if lm_loc == []:
         return
    task_i, critical_task = max(enumerate(lm_loc), key=lambda task: task[1]["end_time"])
    curr_makespan = critical_task["end_time"]

    # Remove task from previous place
    for proc in range(critical_task["x"], critical_task["x"] + critical_task["num_proc"]):
        proc_time[proc].pop()
    
    # Calculate best position for one more processor
    win_max_times = _max_sliding_window(proc_time, critical_task["num_proc"] + 1)
    min_time_max_win = min(win_max_times)
    first_proc_less_load = win_max_times.index(min_time_max_win)
    time_one_proc_more = times_lm[task_i][(critical_task["num_proc"] + 1) - 1]

    # If its not going to improve,put the task in the same place and finish
    if curr_makespan <= min_time_max_win + time_one_proc_more:
        for proc in range(critical_task["x"], critical_task["x"] + critical_task["num_proc"]):
            proc_time[proc].append(curr_makespan)
            return
    print("Improving")
    critical_task["num_proc"] += 1
    critical_task["time"] = times_lm[task_i][critical_task["num_proc"] - 1]
    
    # If it can be improved, we move
    critical_task["x"] = first_proc_less_load
    critical_task["y"] = min_time_max_win
    for proc in range(first_proc_less_load, first_proc_less_load + critical_task["num_proc"]):
        proc_time[proc].append(min_time_max_win + critical_task["time"])
    critical_task["end_time"] = critical_task["y"] + critical_task["time"]

    # Recursive call for repeat the process
    _improve_critical_task(lm_loc, times_lm, proc_time)


def _multi_layer_sched(m, limit, proc_time, times):
    n = len(times)
    hm_loc = [{} for _ in range(n)]
    proc_time = copy.deepcopy(proc_time)
    min_proc_time = lambda task_t, limit: next((i + 1 for i, time in enumerate(task_t) if time <= limit), float("inf")) 
    s, avp, c, i = 0, m, 0, 0
    while i < n:
        task_loc, task_t = hm_loc[i], times[i]
        proc_need = min_proc_time(task_t, limit)
        if proc_need <= avp:
            task_loc["num_proc"] = proc_need
            task_loc["x"] = m - avp
            task_loc["y"] = s
            task_loc["time"] = task_t[proc_need - 1]
            for proc in range(task_loc["x"], task_loc["x"] + proc_need):
                proc_time[proc].append(s + task_loc["time"])
            task_loc["end_time"] = s + task_loc["time"]
            avp -= proc_need
            c = max(c, task_loc["time"])
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
    return True, hm_loc, proc_time
              

def _assign_hm(m, times_hm, proc_time):
    makespan_lb = sum(map(lambda task_t: task_t[0], times_hm)) / m
    makespan_ub = sum(map(lambda task_t: task_t[m-1], times_hm))
    makespan_space = np.arange(makespan_lb, makespan_ub + 0.02, 0.01)
    left_pos = 0
    right_pos = len(makespan_space) - 1
    hm_loc, best_proc_time = None, None
    while left_pos <= right_pos:
        middle_pos = (left_pos + right_pos) // 2
        possible, hm_sched, proc_time_sched = _multi_layer_sched(m, makespan_space[middle_pos], proc_time, times_hm)
        if possible:
            hm_loc = hm_sched
            best_proc_time = proc_time_sched
            right_pos = middle_pos - 1 
        else:
            left_pos = middle_pos + 1
    return hm_loc, best_proc_time
              

def assign_plane_pos(m, times_lm, times_hm):
    # Momentaneo. Pensar como hacer para no tener esta estructura O(n*m). Ayuda en el método _improve_critical_task
    proc_time = {i : [0] for i in range(m)}
    hm_loc, proc_time = _assign_hm(m, times_hm, proc_time)
    lm_loc, proc_time = _lpt_alg(times_lm, proc_time)
    _improve_critical_task(lm_loc, times_lm, proc_time)
    real_makespan = max(proc[-1] for proc in proc_time.values())
    return real_makespan, lm_loc, hm_loc
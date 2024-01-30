import heapq

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

def assign_plane_pos(m, sol):
    tau_0, tau_1, tau_2, tau_s = sol
    first_proc = 0
    proc_time = {i : 0 for i in range(m)}
    # Assign tau_0
    first_proc, tau_0, proc_time = _consecutive_processor_assign(first_proc, tau_0, proc_time)
    # Assign tau_1
    print(len(tau_1))
    _, tau_1, proc_time = _consecutive_processor_assign(first_proc, list(map(lambda t: [t], tau_1)), proc_time)
    tau_1 = list(map(lambda t: t[0], tau_1))
    print(len(tau_1))
    # Assign tau_s: For 3/2-approximation it is not necessary to order decreasingly, but it works better like this
    tau_s = sorted(tau_s, key=lambda task: task["time"], reverse=True)
    for task in tau_s:
        task, proc_time = _assign_to_less_load(task, proc_time)
        task["num_proc"] = 1
    # Assign tau_2: For 3/2-approximation it is not necessary to order decreasingly, but it works better like this
    tau_2 = sorted(tau_2, key=lambda task: task["time"], reverse=True)
    for task in tau_2:
        task, proc_time = _assign_to_less_load_window(task, proc_time)

    real_makespan = max(proc_time.values())
    return real_makespan, (tau_0, tau_1, tau_2, tau_s)
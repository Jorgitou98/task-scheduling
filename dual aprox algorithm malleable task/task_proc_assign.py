
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


def assign_plane_pos(m, tau_0, tau_1, tau_2, tau_s):
    first_proc = 0
    proc_time = {i : 0 for i in range(m)}
    first_proc, tau_0, proc_time = _consecutive_processor_assign(first_proc, tau_0, proc_time)
    _, tau_1, proc_time = _consecutive_processor_assign(first_proc, tau_1, proc_time)
    # For the 3/2-approximation it is not necessary to order decreasingly tau_0, but it works better like this
    tau_s = sorted(tau_s, key=lambda task: task["time"], reverse=True)
    for task in tau_s:
        task, proc_time = _assign_to_less_load(task, proc_time)
        task["num_proc"] = 1
    # For the 3/2-approximation it is not necessary to order decreasingly tau_2, but it works better like this
    tau_2 = sorted(tau_2, key=lambda task: task["time"], reverse=True)
    
    return tau_0, tau_1, tau_2, tau_s
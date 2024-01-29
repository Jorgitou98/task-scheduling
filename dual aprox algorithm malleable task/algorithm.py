import numpy as np
from operator import itemgetter
from itertools import chain
from show_and_plot import show_algorithm_sets

def makespan_lower_bound(times, m):
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

def _refinement_rules(tau1, tau2, m, d, times):
    tau0 = []
    some_rule_exec = True
    while some_rule_exec:
        some_rule_exec = False

        # Rule 3
        procs_per_stack_tau1 = map(lambda task_stack: max(map(itemgetter("num_proc"), task_stack)), tau1)
        idle_proc_tau1 = m - sum(procs_per_stack_tau1)
        if idle_proc_tau1 == 0:
            continue
        tasks_to_idles = [task for task_stack in tau2 for task in task_stack if times[task["task_i"]][idle_proc_tau1-1] <= 3*d/2]
        if tasks_to_idles == []:
            continue
        some_rule_exec = True
        task_to_idles = tasks_to_idles[0]
        # Remove moved task from tau2
        tau2 = [[task for task in task_stack if task["task_i"] != task_to_idles["task_i"]] for task_stack in tau2]
        # Removed empty list (processors without any task)
        tau2 = [task_stack for task_stack in tau2 if task_stack != []]
        min_proc_time = lambda task_t, limit: next((i + 1 for i, time in enumerate(task_t) if time <= limit), float("inf"))
        task_proc_3d2 = min_proc_time(times[task_to_idles["task_i"]], 3*d/2)
        
        task_to_idles["num_proc"] = task_proc_3d2
        task_to_idles["time"] = times[task_to_idles["task_i"]][task_proc_3d2 - 1]
        if task_to_idles["time"] >= d:
            tau0.append([task_to_idles])
        else:
            tau1.append([task_to_idles])

        # Rule 1
        task_to_tau0 = [task for task_stack in tau1 for task in task_stack if task["time"] < 3/4*d and task["num_proc"] > 1]
        # Removed moved task from tau1
        tau1 = [[task for task in task_stack if task["time"] >= 3/4*d or task["num_proc"] <= 1] for task_stack in tau1]
        # Removed empty list (processors without any task)
        tau1 = [task_stack for task_stack in tau1 if task_stack != []]
        # Insert moved task to tau0
        for task in task_to_tau0:
            some_rule_exec = True
            # Assign one processor less
            task["num_proc"] = task["num_proc"] - 1
            # Assign time of one processor less
            task["time"] = times[task["task_i"]][task["num_proc"] - 1]
            # Add the task to tau0
            tau0.append([task])
        
        # Rule 2
        task_stackable_to_tau0 = [task for task_stack in tau1 for task in task_stack if task["time"] < 3/4*d and task["num_proc"] == 1]
        # Removed moved task from tau1
        tau1 = [[task for task in task_stack if task["time"] >= 3/4*d or task["num_proc"] > 1] for task_stack in tau1]
        # Removed empty list (processors without any task)
        tau1 = [task_stack for task_stack in tau1 if task_stack != []]
        n_task_stackable = len(task_stackable_to_tau0)
        # Insert moved task to tau0
        if n_task_stackable > 1:
            some_rule_exec = True
            n_stack_task_pairs = n_task_stackable // 2
            # If there is a task without pair, it would be in tau1 for the next iteration
            if n_task_stackable % 2 == 1:
                tau1.append([task_stackable_to_tau0[-1]])
            # Putting rest of stackable task in tau0
            for i in range(n_stack_task_pairs):
                tau0.append([task_stackable_to_tau0[2*i], task_stackable_to_tau0[2*i+1]])
        

    
    return tau0, tau1, tau2





def _knapsack(item_weights, item_values, capacity):
    n = len(item_weights)
    # best_value[i][j] = minimum value (in + out of snap) for pack i first items with capacity j.
    # Note that best_value[0][j] = 0 for all j
    best_value = [[0 for _ in range(capacity + 1)]] + [[float("inf") for _ in range(capacity + 1)] for _ in range(n)]
    for i in range(1, n+1):
        for j in range(capacity+1):
            _, weight = item_weights[i-1]
            _, values = item_values[i-1]
            # Item need more capacity than available, it goes out of the snap
            if j - weight < 0:
                best_value[i][j] = best_value[i-1][j] + values["out"]
            # If item can be put in the snap, take the best decision between put in or not
            else:
                item_in = best_value[i-1][j-weight] + values["in"]
                item_out = best_value[i-1][j] + values["out"]
                best_value[i][j] = min(item_in, item_out)
    
    # Result with n items and complete capacity
    min_value = best_value[n][capacity]

    # Rebuild the solution (items in and out the snap)
    in_snap, out_snap = [], []
    j = capacity
    for i in range(n, 0, -1):
        task_i, values = item_values[i-1]
        # If the path to the optimum decide not to take the item i
        if best_value[i][j] == best_value[i-1][j] + values["out"]:
            out_snap.append(task_i)
        # If the path to the optimum decide to take the item i
        else:
            in_snap.append(task_i)
            _, weight = item_weights[i-1]
            j -= weight


    return min_value, in_snap, out_snap 




# Try to pack the tasks in <= 3/2*d time using the 2-shelves approach. Return if its posible andthe solution
def _packing(times, d, m):
    # Task with very small times (t(1) < d/2). They are asigned to one processor
    tau_s = [{"task_i": i, "time": task_t[0]} for i, task_t in enumerate(times) if task_t[0] < d/2]
    # Total area needed for very small tasks (sum of its times)
    w_s = sum(map(itemgetter("time"), tau_s))
    # Rest of task
    times_r = [(i, task_t) for i, task_t in enumerate(times) if task_t[0] >= d/2]

    # Weigths of putting tasks in knapsack: min #proc s.a t_i <= d (infinity if need more than m processors)
    min_proc_time = lambda task_t, limit: next((i + 1 for i, time in enumerate(task_t) if time <= limit), float("inf")) 
    task_weights_d = {i: min_proc_time(task_t, d) for i, task_t in times_r}
    # If some task have infinity weigth for limit time d (need more than m processor), its not possible to allocate it 
    if any(map(lambda task_w: task_w == float("inf"), task_weights_d.values())):
        return False, None

    # Values of (putting, not putting) tasks in knapsack area works with the number of processor as weight
    task_weights_d2 = {i: min_proc_time(task_t, d/2) for i, task_t in times_r}
    task_value = lambda task_i, n_proc: float("inf") if n_proc == float("inf") else n_proc * times[task_i][n_proc-1]
    task_values = {i: {"in": task_value(i, w_d), "out": task_value(i, task_weights_d2[i])} for i, w_d in task_weights_d.items()}
    min_value, tau_1, tau_2 = _knapsack(item_weights =  list(task_weights_d.items()), item_values = list(task_values.items()), capacity = m)

    # If optimal work doesnt give enough space for small tasks, the makespan d is small
    if min_value > m*d - w_s:
        return False, None
    # Match each task with the #processors and time used, according to its allocation (in tau_1 or in tau_2).
    tau_1 = [[{"task_i": index, "num_proc": task_weights_d[index], "time": times[index][task_weights_d[index] - 1]}] for index in tau_1]
    tau_2= [[{"task_i": index, "num_proc": task_weights_d2[index], "time": times[index][task_weights_d2[index] - 1]}] for index in tau_2]
    tau_0, tau_1, tau_2 = _refinement_rules(tau1 = tau_1, tau2 = tau_2, m = m, d = d, times = times)
    return True, (tau_0, tau_1, tau_2, tau_s)
    


# Solves de problem by bin search over the makespan space
def dual_schedule(m, epsilon, times):
    # Lower bound of optimal makespan
    makespan_lb =  makespan_lower_bound(times, m)
    # Double of the lower bound is an upper bound of the optimal makespan
    makespan_ub =  2*makespan_lb
    # Space of makespan for searching
    makespan_space = np.arange(makespan_lb, makespan_ub + 2*epsilon, epsilon)
    print("Size of binary search space: ", len(makespan_space))
    # Binary search over the makespan space
    left_pos = 0
    right_pos = len(makespan_space) - 1
    best_sol = None
    best_makespan = None
    while left_pos <= right_pos:
        middle_pos = (left_pos + right_pos) // 2
        
        makespan_valid, sol = _packing(times = times, d = makespan_space[middle_pos], m=m)
        if makespan_valid:
            right_pos = middle_pos - 1
            best_sol = sol
            best_makespan = makespan_space[middle_pos]
        else:
            left_pos = middle_pos + 1
    show_algorithm_sets(best_makespan, makespan_lb, best_sol)
    return best_makespan, best_sol
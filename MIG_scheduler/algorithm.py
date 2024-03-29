from collections import defaultdict
from pprint import pprint
import heapq

def create_allotments_family(times, n_slices):
    # Función para calcular el trabajo de una tarea con ciertos gpcs
    def work(time_task):
        _, slices, time = time_task
        return slices * time
    allotmets_family = [[min(times_task, key=work) for times_task in times]]
    while True:
        allotment_prev = allotmets_family[-1]
        index_max_time = max(enumerate(allotment_prev), key=lambda x: x[1][2])[0]
        _, num_slices, time = allotment_prev[index_max_time]
        if num_slices == n_slices:
            break
        allotment_curr = allotment_prev.copy()
        more_slices_task = [(index, slices, time) for index, slices, time in times[index_max_time] if slices > num_slices]
        allotment_curr[index_max_time] = min(more_slices_task, key=work)
        allotmets_family.append(allotment_curr)
    # print("\n\nAllotments family\n\n")
    # pprint(allotmets_family)
    return allotmets_family

class Task:
    def __init__(self, first_slice, slices, slices_used, start_time, time, index=None):
        self.first_slice = first_slice
        self.slices = slices
        self.slices_used = slices_used
        self.start_time = start_time
        self.time = time
        if index != None:
            self.index = index
        
    def __lt__(self, other):
        return self.start_time + self.time < other.start_time + other.time
    
    def __repr__(self):
        return f'\nTask(first_slice={self.first_slice},\n\tslices={self.slices},\n\tslices_used={self.slices_used},\n\tstart_time={self.start_time},\n\ttime={self.time})'

def tasks_scheduling(num_slices, allotment):
    # Agrupo por número de slices
    allotment_by_slices = defaultdict(list)
    for index, slices, time in allotment:
        allotment_by_slices[slices].append((time, index))
    
    # Ordeno de mayor a menor en cada grupo
    allotment_by_slices = {slices: sorted(task, reverse=True) for slices, task in allotment_by_slices.items()}
    #print(allotment_by_slices)
    scheduling = []
    pq = []
    
    # Empezamos en tiempo 0 con todos los slices
    heapq.heappush(pq, Task(first_slice=0, slices=num_slices, slices_used=0, start_time=0, time=0))
    while allotment_by_slices != {}:
        # Sacamos la primera tarea en finalizar
        task_c = heapq.heappop(pq)
        if task_c.time > 0:
            scheduling.append(task_c)
        # Tiempo en que la tarea ha finalizado
        finish_time = task_c.start_time + task_c.time
        # Si aún hay tareas de su mismo tamaño, o el tamaño es 4 y hay tareas de tamaño 3 que colocar
        if task_c.slices in allotment_by_slices or (task_c.slices == 4 and 3 in allotment_by_slices):
            # En el primer caso se usan todos los slices, en el segundo solo 3 de los 4 ocupados
            slices_used = task_c.slices if task_c.slices in allotment_by_slices else 3
            # Saco la tarea del tamaño a usar que sea más grande
            next_task_time, next_index = allotment_by_slices[slices_used].pop(0)
            # La planifico a continuación
            heapq.heappush(pq, Task(first_slice = task_c.first_slice, slices = task_c.slices,\
                                    slices_used=slices_used, start_time=finish_time, time = next_task_time,\
                                    index = next_index))
            # Si esta era la última tarea de ese tamaño, elimino el tamaño como disponible
            if allotment_by_slices[slices_used] == []:
                allotment_by_slices.pop(slices_used)
        
        # Si no hay tareas para colocar en ese tamaño, y no estamos en una hoja (tamaño 1), fraccionamos la instancia 
        elif task_c.slices > 1:
            slices_left, slices_right = (task_c.slices + 1) // 2, task_c.slices // 2
            heapq.heappush(pq, Task(first_slice = task_c.first_slice, slices = slices_left, slices_used = 0,\
                           start_time=finish_time, time=0))
            heapq.heappush(pq, Task(first_slice = task_c.first_slice + slices_left, slices=slices_right, slices_used=0,\
                           start_time=finish_time, time=0))
            
    # Guardo las últimas tareas que queden en la cola
    while pq:
        task_c = heapq.heappop(pq)
        if task_c.time > 0:
            scheduling.append(task_c)
    return scheduling

def give_makespan(scheduling):
    return max(task.start_time + task.time for task in scheduling)

def lower_bound_makespan_opt(allotmets_family, n_slices):
    allotment_0 = allotmets_family[0]
    return sum(slices*time for _, slices, time in allotment_0) / n_slices

def moldable_scheduler(n_slices, allotmets_family):
    schedulings = [tasks_scheduling(n_slices, allotment) for allotment in allotmets_family]
    # for scheduling in schedulings:
    #     print("Scheduling")
    #     print(scheduling)
    #     #draw_rects(n_slices, scheduling, lb_makespane_opt)
    makespan, scheduling_algorithm = min(((give_makespan(scheduling), scheduling) for scheduling in schedulings), key=lambda x: x[0])
    return makespan, scheduling_algorithm


from itertools import permutations


def _sum_speed(tasks_times, partition):
    speed = 0
    for task_times, instance_size in zip(tasks_times, partition):
        time_1 = next((time for _, slices, time in task_times if slices == 1), None)
        time_size = next((time for _, slices, time in task_times if slices == instance_size), None)
        speed += time_1 / time_size
    return speed


def _select_partition(times, partitions):
    best_speed = 0
    best_partition = None
    best_order = None
    for partition in partitions:
        n_instances = len(partition)
        task_goal = times[:n_instances]
        best_speed_partition = 0
        task_partition_order = None
        for task_times in permutations(task_goal):
            speed = _sum_speed(task_times, partition)
            if speed > best_speed_partition:
                best_speed_partition = speed
                task_partition_order = task_times
        #print(partition, best_speed_partition)
        if best_speed_partition > best_speed:
            best_speed = best_speed_partition
            best_partition = partition
            best_order = task_partition_order
    return best_partition, best_order

partitions_A30 = [[4], [2,2], [2,1,1], [1,1,2], [1,1,1,1]]
partitions_A100 = [[7], [4,3], [4,2,1], [4,1,1,1],\
                    [3,3], [3,2,1], [3,1,1,1],\
                    [2,2,3],[2,2,2,1], [2,2,1,1,1],\
                    [2,1,1,3],[2,1,1,2,1], [2,1,1,1,1,1],\
                    [1,1,2,3],[1,1,2,2,1], [1,1,2,1,1,1],\
                    [1,1,1,1,3],[1,1,1,1,2,1], [1,1,1,1,1,1,1]]

def no_dynamic_reconfig(device, times):
    scheduling = []
    partitions = partitions_A100 if device == "A100" else partitions_A30
    num_slices = 4 if device == "A30" else 7
    start_times = [0 for slice in range(num_slices)]
    while times != []:
        best_partition, best_order = _select_partition(times, partitions)
        first_slice = 0
        for task_times, instance_size in zip(best_order, best_partition):
            index, time = next(((index, time) for index, slices, time in task_times if slices == instance_size), None)
            slices = 4 if first_slice == 0 and instance_size == 3 else instance_size
            next_start_time = max(start_times[first_slice:first_slice+slices])
            scheduling.append(Task(first_slice=first_slice, slices=slices, slices_used=instance_size,\
                                   start_time=next_start_time, time=time, index=index))
            for slice in range(first_slice, first_slice+slices):
                start_times[slice] = next_start_time + time
            first_slice += slices

        times = times[len(best_partition):]
    return scheduling

def fifo_partition(times, partition):
    pq = []
    scheduling = []
    first_slice = 0
    for instance_size in partition:
            reserved_slices = instance_size
            if instance_size == 3 and partition[-1] != 3:
                reserved_slices = 4
            heapq.heappush(pq, Task(first_slice=first_slice, slices=reserved_slices, slices_used=instance_size,\
                                start_time=0, time=0))
            first_slice += reserved_slices
    for task_times in times:
        task_finish = heapq.heappop(pq)
        if task_finish.time > 0:
            scheduling.append(task_finish)
        next_index, next_time = next(((index, time) for index, slices, time in task_times if slices == task_finish.slices_used), None)
        heapq.heappush(pq, Task(first_slice=task_finish.first_slice, slices=task_finish.slices, slices_used=task_finish.slices_used,\
                            start_time=task_finish.start_time + task_finish.time, time=next_time, index=next_index))
    while pq:
        task_finish = heapq.heappop(pq)
        if task_finish.time > 0:
            scheduling.append(task_finish)
    return scheduling


def fifo_fixed(device, times):
    partitions = partitions_A100 if device == "A100" else partitions_A30
    best_scheduling = None
    best_makespan = float("inf")
    for partition in partitions:
        scheduling_partition = []
        pq = []
        first_slice = 0
        for instance_size in partition:
            reserved_slices = instance_size
            if instance_size == 3 and partition[-1] != 3:
                reserved_slices = 4
            heapq.heappush(pq, Task(first_slice=first_slice, slices=reserved_slices, slices_used=instance_size,\
                                start_time=0, time=0))
            first_slice += reserved_slices
        for task_times in times:
            task_finish = heapq.heappop(pq)
            if task_finish.time > 0:
                scheduling_partition.append(task_finish)
            next_index, next_time = next(((index, time) for index, slices, time in task_times if slices == task_finish.slices_used), None)
            heapq.heappush(pq, Task(first_slice=task_finish.first_slice, slices=task_finish.slices, slices_used=task_finish.slices_used,\
                                start_time=task_finish.start_time + task_finish.time, time=next_time, index=next_index))
        while pq:
            task_finish = heapq.heappop(pq)
            if task_finish.time > 0:
                scheduling_partition.append(task_finish)
        makespan_partition = give_makespan(scheduling_partition)
        if makespan_partition < best_makespan:
            best_makespan = makespan_partition
            best_scheduling = scheduling_partition
    return best_scheduling
        


        
    
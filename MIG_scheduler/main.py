from plotting import draw_rects
from algorithm import *
from inputs import generate_tasks
import random


def main():
    device, times, instance_sizes = generate_tasks()
    n_slices = instance_sizes[-1]
    random.shuffle(times)

    allotmets_family = create_allotments_family(times, n_slices)
    lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
    _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)

    scheduling_no_dynamic = no_dynamic_reconfig(device, times)
    draw_rects(n_slices, scheduling_no_dynamic, lb_makespane_opt)
    draw_rects(n_slices, scheduling_algorithm, lb_makespane_opt)
    


if __name__ == "__main__":
    main()
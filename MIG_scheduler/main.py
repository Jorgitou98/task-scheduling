from plotting import draw_rects, plot_speedup_inputs
from algorithm import *
from inputs import generate_tasks, get_input_config
import random


def main():
    repetitions, n, instance_sizes, perc_scale, perc_membound, device = get_input_config()
    for _ in range(repetitions):
        times, instance_sizes = generate_tasks(n, instance_sizes, perc_scale, perc_membound, device)
        #plot_speedup_inputs(device, times)
        
        n_slices = instance_sizes[-1]
        random.shuffle(times)

        allotmets_family = create_allotments_family(times, n_slices)
        lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
        _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)
        scheduling_fifo_fixed = fifo_fixed(device, times)
        scheduling_no_dynamic = no_dynamic_reconfig(device, times)
        makespan_fifo_fixed = give_makespan(scheduling_fifo_fixed)
        makespan_no_dynamic = give_makespan(scheduling_no_dynamic)
        makespan_algorithm = give_makespan(scheduling_algorithm)
        print("FIFO fixed ratio:", makespan_fifo_fixed / lb_makespane_opt)
        print("No dynamic ratio:", makespan_no_dynamic / lb_makespane_opt)
        print("Algorithm ratio:", makespan_algorithm / lb_makespane_opt)
        draw_rects(n_slices, scheduling_fifo_fixed, scheduling_no_dynamic, scheduling_algorithm, lb_makespane_opt)
    


if __name__ == "__main__":
    main()
from plotting import draw_rects, plot_speedup_inputs
from algorithm import *
from inputs import generate_tasks, get_input_config, read_task_rodinia
import random
import statistics

def inputs_config_task_size_test():
    repetitions = 500
    for n in [10,15,20,25,30,35]:
        n_scale = {}
        l_percs = [[(1,50),(2,50),(3,0),(4,0),(7,0)], [(1,20),(2,20),(3,20),(4,20),(7,20)], [(1,0),(2,0),(3,0),(4,50),(7,50)]]
        for percs in l_percs:
            n_in = 0
            for slices, perc in percs:
                n_scale[slices] = perc*n // 100
                n_in +=n_scale[slices]
            possible_slices = [1,2,3,4,7]
            for _ in range(n-n_in):
                while n_scale[possible_slices[0]] == 0:
                    possible_slices = possible_slices[1:]
                n_scale[possible_slices[0]] += 1
            instance_sizes = [1,2,3,4,7]
            ratios_algorithm = []
            for _ in range(repetitions):
                times, instance_sizes = generate_tasks(instance_sizes, n_scale, device="A100")
                #plot_speedup_inputs(device="A100", times=times)
                
                n_slices = instance_sizes[-1]
                random.shuffle(times)

                allotmets_family = create_allotments_family(times, n_slices)
                lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
                _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)
                # scheduling_fifo_fixed = fifo_fixed(device, times)
                # scheduling_no_dynamic = no_dynamic_reconfig(device, times)
                # makespan_fifo_fixed = give_makespan(scheduling_fifo_fixed)
                # makespan_no_dynamic = give_makespan(scheduling_no_dynamic)
                makespan_algorithm = give_makespan(scheduling_algorithm)
                ratios_algorithm.append(makespan_algorithm/lb_makespane_opt)
            
            print(f"Alg ratio n= {n}, {percs}: {statistics.mean(ratios_algorithm):.3f}+-{statistics.stdev(ratios_algorithm):.3f}")


def compare_size_test():
    repetitions = 100
    for n in [15, 30]:
        n_scale = {}
        l_percs = [[(1,50),(2,50),(3,0),(4,0),(7,0)], [(1,20),(2,20),(3,20),(4,20),(7,20)], [(1,0),(2,0),(3,0),(4,50),(7,50)]]
        for percs in l_percs:
            n_in = 0
            for slices, perc in percs:
                n_scale[slices] = perc*n // 100
                n_in +=n_scale[slices]
            possible_slices = [1,2,3,4,7]
            for _ in range(n-n_in):
                while n_scale[possible_slices[0]] == 0:
                    possible_slices = possible_slices[1:]
                n_scale[possible_slices[0]] += 1
            instance_sizes = [1,2,3,4,7]
            device = "A100"
            for times_range in [[1,100], [90,100]]:
                ratios_fixed, ratios_fixed7s, ratios_fixed1s = [], [], []
                ratios_speed_indep = []
                for i in range(repetitions):
                    times, instance_sizes = generate_tasks(instance_sizes, n_scale, 50, device, times_range)
                    #plot_speedup_inputs(device, times)
                    
                    n_slices = instance_sizes[-1]
                    random.shuffle(times)

                    allotmets_family = create_allotments_family(times, n_slices)
                    lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
                    _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)
                    scheduling_fifo_fixed = fifo_fixed(device, times)
                    scheduling_no_dynamic = no_dynamic_reconfig(device, times)
                    scheduling_7s = fifo_partition(times, [7])
                    scheduling_1s = fifo_partition(times, [1,1,1,1,1,1,1])
                    makespan_fifo_fixed = give_makespan(scheduling_fifo_fixed)
                    makespan_no_dynamic = give_makespan(scheduling_no_dynamic)
                    makespan_algorithm = give_makespan(scheduling_algorithm)
                    makespan1s = give_makespan(scheduling_1s)
                    makespan7s = give_makespan(scheduling_7s)
                    draw_rects(n_slices, scheduling_no_dynamic, scheduling_fifo_fixed, scheduling_1s, lb_makespane_opt)
                    ratios_fixed7s.append(makespan7s / makespan_algorithm)
                    ratios_fixed1s.append(makespan1s / makespan_algorithm)
                    ratios_fixed.append(makespan_fifo_fixed / makespan_algorithm)
                    ratios_speed_indep.append(makespan_no_dynamic / makespan_algorithm)
                    #print(makespan_fifo_fixed / makespan_algorithm)
                print(f"Fifo fix-best n= {n}, {percs}, {times_range}: {statistics.mean(ratios_fixed):.2f}+-{statistics.stdev(ratios_fixed):.2f}")
                print(f"Fifo fix-1s n= {n}, {percs}, {times_range}: {statistics.mean(ratios_fixed1s):.2f}+-{statistics.stdev(ratios_fixed1s):.2f}")
                print(f"Fifo fix-7s n= {n}, {percs}, {times_range}: {statistics.mean(ratios_fixed7s):.2f}+-{statistics.stdev(ratios_fixed7s):.2f}")
                print(f"Fifo speed-indep n= {n}, {percs}, {times_range}: {statistics.mean(ratios_speed_indep):.2f}+-{statistics.stdev(ratios_speed_indep):.2f}")
                print()

def rodinia_kernels_test():
    times, test_names = read_task_rodinia()
    n_slices = 7
    allotmets_family = create_allotments_family(times, n_slices)
    lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
    _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)
    scheduling_no_dynamic = no_dynamic_reconfig("A100", times)
    scheduling_fifo_fixed = fifo_fixed("A100", times)
    scheduling_7s = fifo_partition(times, [7])
    scheduling_1s = fifo_partition(times, [1,1,1,1,1,1,1])
    makespan_fifo_fixed = give_makespan(scheduling_fifo_fixed)
    makespan_no_dynamic = give_makespan(scheduling_no_dynamic)
    makespan1s = give_makespan(scheduling_1s)
    makespan7s = give_makespan(scheduling_7s)
    makespan_algorithm = give_makespan(scheduling_algorithm)
    print(f"Rho Rodinia: {makespan_algorithm/ lb_makespane_opt:.3f}")
    print(f"Ratio 1s: {makespan1s/ makespan_algorithm:.3f}")
    print(f"Ratio 7s: {makespan7s/ makespan_algorithm:.3f}")
    print(f"Ratio Fix-Part-Best: {makespan_fifo_fixed/ makespan_algorithm:.3f}")
    print(f"Ratio Speed-Indep: {makespan_no_dynamic/ makespan_algorithm:.3f}")
    draw_rects(n_slices, scheduling_no_dynamic, scheduling_1s, scheduling_fifo_fixed, scheduling_7s, scheduling_algorithm, lb_makespane_opt, names = test_names)

def main():
    #compare_size_test()
    inputs_config_task_size_test()
    #rodinia_kernels_test()
    # repetitions, instance_sizes, n_scale, perc_membound, device = get_input_config()
    # for _ in range(repetitions):
    #     times, instance_sizes = generate_tasks(instance_sizes, n_scale, perc_membound, device)
    #     plot_speedup_inputs(device, times)
        
    #     n_slices = instance_sizes[-1]
    #     random.shuffle(times)

    #     allotmets_family = create_allotments_family(times, n_slices)
    #     lb_makespane_opt = lower_bound_makespan_opt(allotmets_family, n_slices)
    #     _, scheduling_algorithm = moldable_scheduler(n_slices, allotmets_family)
    #     scheduling_fifo_fixed = fifo_fixed(device, times)
    #     scheduling_no_dynamic = no_dynamic_reconfig(device, times)
    #     makespan_fifo_fixed = give_makespan(scheduling_fifo_fixed)
    #     makespan_no_dynamic = give_makespan(scheduling_no_dynamic)
    #     makespan_algorithm = give_makespan(scheduling_algorithm)
    #     print("FIFO fixed ratio:", makespan_fifo_fixed / lb_makespane_opt)
    #     print("No dynamic ratio:", makespan_no_dynamic / lb_makespane_opt)
    #     print("Algorithm ratio:", makespan_algorithm / lb_makespane_opt)
    #     draw_rects(n_slices, scheduling_fifo_fixed, scheduling_no_dynamic, scheduling_algorithm, lb_makespane_opt)
    #     print("Ratio:", makespan_algorithm/lb_makespane_opt)
    #     print(f"Ratio Fix-Part-Best: {makespan_fifo_fixed/ makespan_algorithm:.3f}")
        

if __name__ == "__main__":
    main()
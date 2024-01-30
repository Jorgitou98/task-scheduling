from inputs import get_inputs
from algorithm import dual_schedule
from show_and_plot import draw_shelve_stacked_rects
from task_proc_assign import assign_plane_pos

def main():
    n, m, epsilon, times = get_inputs()
    # Call to the algorithm with problem inputs
    best_makespan, (tau_0, tau_1, tau_2, tau_s) = dual_schedule(m = m, epsilon = epsilon, times = times)
    real_makespan, (tau_0, tau_1, tau_2, tau_s) = assign_plane_pos(m, tau_0, tau_1, tau_2, tau_s)   
    draw_shelve_stacked_rects(real_makespan = real_makespan, d = best_makespan, m = m, tau_0 = tau_0, tau_1 = tau_1, tau_2 = tau_2, tau_s = tau_s)

if __name__ == "__main__":
    main()
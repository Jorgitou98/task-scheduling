import inputs as inp
from algorithm import dual_schedule
from show_and_plot import draw_shelve_stacked_rects, draw_ratios
from task_proc_assign import assign_plane_pos
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_task_test', action="store_true", help='Run test with many task size n')
args = parser.parse_args()

def compute_ratios(n_inf, n_sup, reps, m, epsilon):
    ratios = []
    for n in range(n_inf, n_sup+1):
        mean_ratio = 0
        for _ in range(reps):
            times = inp.generate_tasks(n = n, m = m)
            best_makespan, real_makespan, sol = solve_instance(m, epsilon, times)
            ratio = real_makespan / best_makespan
            mean_ratio += ratio
        mean_ratio /= reps
        ratios.append(mean_ratio)
    return ratios

def solve_instance(m, epsilon, times):
    # Call to the algorithm with problem inputs
    best_makespan, sol = dual_schedule(m = m, epsilon = epsilon, times = times)
    # Assign the tasks to specific processors and times
    real_makespan, sol = assign_plane_pos(m, sol)   
    return best_makespan, real_makespan, sol



def main():
    task_sizes, m, epsilon = inp.get_input_sizes(num_task_test = args.num_task_test)
    if args.num_task_test:
        n_inf, n_sup, reps = task_sizes
        ratios = compute_ratios(n_inf, n_sup, reps, m, epsilon)
        draw_ratios(n_range = range(n_inf, n_sup+1), ratios = ratios)
    else:
        n = task_sizes
        times = inp.generate_tasks(n = n, m = m)
        best_makespan, real_makespan, sol = solve_instance(m, epsilon, times)      
        # Draw the solution and show some outputs
        draw_shelve_stacked_rects(real_makespan = real_makespan, d = best_makespan, m = m, sol = sol)
    


if __name__ == "__main__":
    main()
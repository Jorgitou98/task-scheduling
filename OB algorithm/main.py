import inputs as inp
from search import schedule
from plotting import draw_shelve_stacked_rects, draw_ratios
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_task_test', action="store_true", help='Run test with many task sizes n')
args = parser.parse_args()

def compute_ratios(n_inf, n_sup, reps, m):
    ratios = []
    for n in range(n_inf, n_sup+1):
        mean_ratio = 0
        for _ in range(reps):
            times = inp.generate_tasks(n = n, m = m)
            makespan_lb, makespan, _, _ = schedule(times, m) 
            ratio = makespan / makespan_lb
            mean_ratio += ratio
        mean_ratio /= reps
        ratios.append(mean_ratio)
        if n > n_inf and (n - n_inf) % 20 == 0:
            draw_ratios(n_range = range(n_inf, n+1), ratios = ratios)
    return ratios


def main():
    task_sizes, m= inp.get_input_sizes(num_task_test = args.num_task_test)
    if args.num_task_test:
        n_inf, n_sup, reps = task_sizes
        ratios = compute_ratios(n_inf, n_sup, reps, m)
        draw_ratios(n_range = range(n_inf, n_sup+1), ratios = ratios)
    else:
        n, reps = task_sizes
        for _ in range(reps):
            times = inp.generate_tasks(n = n, m = m)
            makespan_lb, makespan, lm_loc_sol, hm_loc_sol = schedule(times, m)      
            # Draw the solution and show some outputs
            draw_shelve_stacked_rects(real_makespan = makespan, d = makespan_lb, m = m, lm_loc = lm_loc_sol, hm_loc = hm_loc_sol)
    


if __name__ == "__main__":
    main()
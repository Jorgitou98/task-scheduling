from inputs import generate_tasks
from allocation import _alloc_makespan_lb

def main():
    times = generate_tasks()
    lb_makespan_opt, best_allocation = _alloc_makespan_lb(times)
    print(lb_makespan_opt, best_allocation)


if __name__ == "__main__":
    main()
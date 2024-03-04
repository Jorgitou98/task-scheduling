import matplotlib.pyplot as plt
import matplotlib.patches as patches
from algorithm import give_makespan


def draw_rects(n_slices, scheduling, lb_makespane_opt):
    _, ax = plt.subplots()
    makespan = give_makespan(scheduling)
    error_ratio = makespan / lb_makespane_opt
    plt.title(f"n={len(scheduling)}, error ratio={error_ratio}")
    plt.axhline(y=lb_makespane_opt, color='black', alpha=0.7, label = "LB makespan opt")
    ax.set_xlim(-2, n_slices+1)
    ax.set_ylim(0, 1.1*makespan)
    for task in scheduling:
        rect = patches.Rectangle((task.first_slice, task.start_time), task.slices_used, task.time, alpha = 0.7,
                                    linewidth = 1, facecolor = "tab:orange", edgecolor = 'black')
        ax.add_patch(rect)
    plt.xlabel("Slices")
    plt.ylabel("Time")
    plt.legend()
    plt.show()
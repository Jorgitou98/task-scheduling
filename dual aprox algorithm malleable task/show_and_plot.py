import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pprint import pprint
from itertools import chain


def _draw_rects_set(ax, task_set, color):
    for task in task_set:
        rect = patches.Rectangle((task["x"], task["y"]), task["num_proc"], task["time"],
                                    linewidth = 1, facecolor = color, edgecolor = 'black')
        ax.add_patch(rect)

    

def draw_shelve_stacked_rects(d, m, tau_0, tau_1, tau_2, tau_s):
    _, ax = plt.subplots()
    # Configurar límites del eje
    ax.set_xlim(-2, m+1)
    ax.set_ylim(0, 3*d/2 + 20)
    plt.axhline(y=d, color='black', alpha=0.7)
    plt.axhline(y=3*d/2, color='black', alpha=0.7)
    actual_yticks = ax.get_yticks().tolist()
    actual_yticks.append(d)
    actual_yticks.append(3*d/2)
    ax.set_yticks(actual_yticks)
    actual_yticks_labels = [label.get_text() for label in ax.get_yticklabels()]
    actual_yticks_labels[-2] = f"d={d:.2f}"
    actual_yticks_labels[-1] = f"3d/2={3*d/2:.2f}"
    ax.set_yticklabels(actual_yticks_labels)

    
    _draw_rects_set(ax = ax, task_set = chain(*tau_0), color = "pink")
    _draw_rects_set(ax = ax, task_set = chain(*tau_1), color = "lightblue")
    _draw_rects_set(ax = ax, task_set = tau_s, color = "orange")
    legend_elems = [patches.Patch(linewidth = 1, facecolor = "pink", edgecolor = 'black', label='S_0'),
                    patches.Patch(linewidth = 1, facecolor = "lightblue", edgecolor = 'black', label='S_1'),
                    patches.Patch(linewidth = 1, facecolor = "yellow", edgecolor = 'black', label='S_2'),
                   patches.Patch(linewidth = 1, facecolor = "orange", edgecolor = 'black', label='S_s')]
    ax.legend(handles = legend_elems)

    actual_xticks = ax.get_xticks().tolist()
    if m not in actual_xticks:
        actual_xticks.append(m)
        ax.set_xticks(actual_xticks)
        actual_xticks_labels = [label.get_text() for label in ax.get_xticklabels()]
        actual_xticks_labels[-1] = f"{m}\nm"
        ax.set_xticklabels(actual_xticks_labels)
    
    plt.show()

def show_algorithm_sets(best_makespan, makespan_lb, best_sol):
    print("d*:", best_makespan, "w:", makespan_lb)
    print()
    best_t0, best_t1, best_t2, best_ts = best_sol
    print("t0*:")
    pprint(best_t0)
    print()
    print("t1*:")
    pprint(best_t1)
    print()
    print("t2*:")
    pprint(best_t2)
    print()
    print("ts*:")
    pprint(best_ts)
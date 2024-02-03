import matplotlib.pyplot as plt
import matplotlib.patches as patches


def _draw_rects_set(ax, task_set, color):
    for task in task_set:
        rect = patches.Rectangle((task["x"], task["y"]), task["num_proc"], task["time"],
                                    linewidth = 1, facecolor = color, edgecolor = 'black')
        ax.add_patch(rect)
    

def draw_shelve_stacked_rects(real_makespan, d, m, lm_loc, hm_loc):
    _, ax = plt.subplots()
    # Configurar límites del eje
    ax.set_xlim(-2, m+1)
    ax.set_ylim(0, 1.6*d)
    plt.axhline(y=d, color='black', alpha=0.7)
    plt.axhline(y=3*d/2, color='black', alpha=0.7)
    plt.axhline(y=real_makespan, color='red', alpha=0.7)
    actual_yticks = ax.get_yticks().tolist()
    actual_yticks.append(d)
    actual_yticks.append(3*d/2)
    actual_yticks.append(real_makespan)
    ax.set_yticks(actual_yticks)
    actual_yticks_labels = [label.get_text() for label in ax.get_yticklabels()]
    actual_yticks_labels[-3] = "d"
    actual_yticks_labels[-2] = "3d/2"
    actual_yticks_labels[-1] = "makespan"
    ax.set_yticklabels(actual_yticks_labels)

    n = len(lm_loc) + len(hm_loc) 
    for t_set, color in zip([lm_loc, hm_loc], ["pink", "lightblue"]):
        _draw_rects_set(ax = ax, task_set = t_set, color = color)

    legend_elems = [patches.Patch(linewidth = 1, facecolor = "pink", edgecolor = 'black', label='Low malleability'),
                    patches.Patch(linewidth = 1, facecolor = "lightblue", edgecolor = 'black', label='High malleability')]
    ax.legend(handles = legend_elems)

    actual_xticks = ax.get_xticks().tolist()
    if m not in actual_xticks:
        actual_xticks.append(m)
        ax.set_xticks(actual_xticks)
        actual_xticks_labels = [label.get_text() for label in ax.get_xticklabels()]
        actual_xticks_labels[-1] = f"{m}\nm"
        ax.set_xticklabels(actual_xticks_labels)

    ratio_aprox = real_makespan / d
    print("d*:", d, "real makespan:", real_makespan, "ratio aprox:", ratio_aprox) 
    plt.title(f"n = {n}, m = {m}, ratio aprox = {ratio_aprox:.2f}")
    plt.xlabel("Processors")
    plt.ylabel("Time")
    plt.show()

def draw_ratios(n_range, ratios):
    plt.plot(n_range, ratios)
    plt.show()

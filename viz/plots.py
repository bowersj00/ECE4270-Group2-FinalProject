"""Plotting templates for required figures."""

from pathlib import Path
import matplotlib.pyplot as plt


def save_bar_chart(labels, values, title, ylabel, output):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()


def save_line_plot(x, y, title, xlabel, ylabel, output):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()


# TODO(student):
# - add grouped bar chart for scheduler/workload comparison
# - add row-buffer hit rate vs queue depth plot
# - add fairness vs active threads plot
# - add heatmap for bank utilization
# - add latency vs refresh interval plot

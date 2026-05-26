import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Data — from your robustness output
settings = ["Permissive\n(F1≥0.2)",
            "Default\n(F1≥0.5)",
            "Stringent\n(F1≥0.8)",
            "Stringent F2\n(≥3)"]

fold_over_indep = [4.20, 13.00, 25.76, 56.32]

interactions = {
    "F1 × F2": [7.39,     27.11, 35029.82, 143.50],
    "F1 × F4": [39.16,     6.02,     7.99,   7.28],
    "F2 × F4": [3.28,      4.72,     5.15,  10.64],
}

# Mark the sparse-cell estimate so it's visually flagged
is_sparse_estimate = {
    "F1 × F2": [False, False, True, False],
    "F1 × F4": [False, False, False, False],
    "F2 × F4": [False, False, False, False],
}

# Plot settings
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(13, 5.5),
                                         gridspec_kw={"width_ratios": [1, 1.4]})

# === LEFT PANEL: fold over independence ===
x = np.arange(len(settings))
bar_colors_left = ["#a7c7d9", "#5e8fb0", "#3a5a7a", "#2a3d5b"]  # gradient

bars_left = ax_left.bar(x, fold_over_indep, color=bar_colors_left,
                          edgecolor="#222", linewidth=0.6, width=0.65)

ax_left.axhline(1, color="#999", linestyle="--", linewidth=0.8)
ax_left.text(len(settings) - 0.45, 1.15, "independence baseline",
             fontsize=9, color="#666", ha="right", style="italic")

ax_left.set_yscale("log")
ax_left.set_xticks(x)
ax_left.set_xticklabels(settings, fontsize=9)
ax_left.set_ylabel("Fold over independence prediction\n"
                   "(observed F1∧F2∧F4 cell / independence-predicted)", fontsize=10)
ax_left.set_title("A. Compounding strength across thresholds",
                   loc="left", fontsize=11, pad=12, fontweight="bold")

# Annotate each bar with its value
for xi, val in zip(x, fold_over_indep):
    ax_left.text(xi, val * 1.15, f"{val:.1f}×",
                 ha="center", fontsize=10, fontweight="bold", color="#222")

ax_left.set_ylim(top=ax_left.get_ylim()[1] * 1.5)

# === RIGHT PANEL: interaction effects ===
n_settings = len(settings)
n_interactions = 3
width = 0.27
x_centers = np.arange(n_settings)

# Colors for the three interaction terms — keep them distinct but harmonious
interaction_colors = {
    "F1 × F2": "#c14a4a",   # red
    "F1 × F4": "#4a8fc1",   # blue
    "F2 × F4": "#74a85c",   # green
}

# Plot each interaction series
for i, (label, values) in enumerate(interactions.items()):
    offset = (i - 1) * width  # center the three bars per setting
    bars = ax_right.bar(x_centers + offset, values,
                        width=width,
                        color=interaction_colors[label],
                        edgecolor="#222", linewidth=0.5,
                        label=label, alpha=0.92)
    
    # Annotate values, and mark sparse-cell estimates
    for xi, val, sparse in zip(x_centers + offset, values, is_sparse_estimate[label]):
        if sparse:
            # Mark the extreme value with a special annotation
            ax_right.text(xi, val * 1.6, f"{val:,.0f}×\n(sparse cell)",
                          ha="center", fontsize=8, color="#a00",
                          fontweight="bold", style="italic")
            # Add a small marker symbol on the bar
            ax_right.text(xi, val * 0.5, "*", ha="center", fontsize=18,
                          color="#fff", fontweight="bold")
        else:
            ax_right.text(xi, val * 1.25, f"{val:.1f}×",
                          ha="center", fontsize=8, color="#333")

ax_right.axhline(1, color="#999", linestyle="--", linewidth=0.8)
ax_right.text(n_settings - 0.4, 0.7, "no interaction (exp(β) = 1)",
              fontsize=9, color="#666", ha="right", style="italic")

ax_right.set_yscale("log")
ax_right.set_xticks(x_centers)
ax_right.set_xticklabels(settings, fontsize=9)
ax_right.set_ylabel("Interaction effect size: exp(β)\n"
                    "(fold deviation from independence)", fontsize=10)
ax_right.set_title("B. Pairwise interaction coefficients",
                    loc="left", fontsize=11, pad=12, fontweight="bold")

ax_right.legend(loc="upper left", fontsize=9, frameon=False)

# Push the y-axis so the sparse-cell annotation fits
ax_right.set_ylim(top=ax_right.get_ylim()[1] * 4)
ax_right.set_ylim(bottom=0.5)

plt.tight_layout()
out = "fig4_h2_compounding.pdf"
plt.savefig(out, format="pdf", bbox_inches="tight", dpi=300)
plt.savefig(out.replace(".pdf", ".png"), format="png", bbox_inches="tight", dpi=300)
print(f"Saved.")
plt.show()

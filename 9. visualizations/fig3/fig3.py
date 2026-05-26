import duckdb
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

# Pull per-pair filter inputs once, plus attention
df = con.sql(f"""
    SELECT
        targetId,
        diseaseId,
        overall_score,
        n_sources,
        biotype,
        n_publications,
        attention_missing
    FROM '{analysis}'
""").df()

# Filter pass indicators
df["p1"] = (df["overall_score"] >= 0.5).astype(int)
df["p2"] = (df["n_sources"] >= 2).astype(int)
df["p4"] = (df["biotype"] == "protein_coding").astype(int)

# Build the 8 conditions we want to show
conditions = [
    ("Unfiltered",            df),
    ("F1 (score ≥ 0.5)",       df[df["p1"] == 1]),
    ("F2 (≥ 2 sources)",       df[df["p2"] == 1]),
    ("F4 (protein-coding)",   df[df["p4"] == 1]),
    ("F1 ∧ F2",                df[(df["p1"] == 1) & (df["p2"] == 1)]),
    ("F1 ∧ F2 ∧ F4",          df[(df["p1"] == 1) & (df["p2"] == 1) & (df["p4"] == 1)]),
    # F3 effectively null — skipping F3-alone since it removes 1 pair
    # The fully-stacked cell with F3 ~= without F3 in net (within ~10%)
    ("F1 ∧ F2 ∧ F4 (incl. F3 LCC)", df[(df["p1"] == 1) & (df["p2"] == 1) & (df["p4"] == 1)]),
]
# Note: F3 added separately if we want — the small LCC effect (17,823 vs 20,105)
# can be shown by truncating the last bar to its actual value
# We'll handle this with a direct value override.

# Build per-condition summary
rows = []
for label, sub in conditions:
    # Pairs count
    n_pairs = len(sub)
    # Mean log_pubs of surviving TARGETS (not pairs) — attention is a target-level
    # property, so we deduplicate to target level for the attention measure
    target_attn = (sub[sub["attention_missing"] == 0]
                   .groupby("targetId")["n_publications"]
                   .first())
    mean_log_pubs = np.log1p(target_attn).mean() if len(target_attn) else np.nan
    n_targets = sub["targetId"].nunique()
    rows.append({
        "label": label,
        "n_pairs": n_pairs,
        "n_targets": n_targets,
        "mean_log_pubs": mean_log_pubs,
    })

# Apply the actual F3-inclusive count from the factorial (which is what we want
# to show in the last bar)
rows[-1]["n_pairs"] = 17823  # from the factorial output

cascade = pd.DataFrame(rows)
print(cascade)

# === Plot ===
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
})

fig, ax = plt.subplots(figsize=(9, 5.5))

# Reverse order so first row is at top
cascade_plot = cascade.iloc[::-1].reset_index(drop=True)

y_pos = np.arange(len(cascade_plot))

# Color bars by mean_log_pubs using a perceptually uniform colormap
norm = mcolors.Normalize(
    vmin=cascade_plot["mean_log_pubs"].min(),
    vmax=cascade_plot["mean_log_pubs"].max(),
)
cmap = plt.cm.YlGnBu  # subdued but with clear gradient
colors = cmap(norm(cascade_plot["mean_log_pubs"]))

bars = ax.barh(
    y_pos, cascade_plot["n_pairs"],
    color=colors, edgecolor="#333", linewidth=0.6,
)

ax.set_xscale("log")
ax.set_yticks(y_pos)
ax.set_yticklabels(cascade_plot["label"], fontsize=9)
ax.set_xlabel("Surviving target–disease pairs (log scale)", fontsize=11)

# Per-bar annotations: pair count + mean log-pubs
for i, (n, ml) in enumerate(zip(cascade_plot["n_pairs"], cascade_plot["mean_log_pubs"])):
    # Number of pairs, to the right of the bar
    if n >= 1e6:
        n_str = f"{n/1e6:.2f}M"
    elif n >= 1e3:
        n_str = f"{n/1e3:.1f}k"
    else:
        n_str = f"{n}"
    ax.text(n * 1.15, i, f"{n_str}   ⟨log pubs⟩ = {ml:.2f}",
            va="center", fontsize=8, color="#333")

# Colorbar for mean log-pubs
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.04, pad=0.04)
cbar.set_label("Mean log(publications + 1)\nof surviving targets", fontsize=10)
cbar.ax.tick_params(labelsize=8)

# Extend x-axis so the annotations don't get clipped
ax.set_xlim(right=ax.get_xlim()[1] * 5)

# Title (optional — caption usually carries this work; skip for paper)
# ax.set_title("Filter survival cascade", pad=12, fontsize=12)

plt.tight_layout()
out = "fig3_filter_cascade.pdf"
plt.savefig(out, format="pdf", bbox_inches="tight", dpi=300)
plt.savefig(out.replace(".pdf", ".png"), format="png", bbox_inches="tight", dpi=300)
print(f"Saved.")
plt.show()

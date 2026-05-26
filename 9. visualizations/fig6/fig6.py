import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

df = con.sql(f"SELECT * FROM '{analysis}'").df()
target_to_idx = {t: i for i, t in enumerate(df["targetId"].unique())}
disease_to_idx = {d: i for i, d in enumerate(df["diseaseId"].unique())}
df["t_idx"] = df["targetId"].map(target_to_idx)
df["d_idx"] = df["diseaseId"].map(disease_to_idx)
n_T = len(target_to_idx)
n_D = len(disease_to_idx)

F1_THRESHOLD = 0.5
F2_THRESHOLD = 2

def apply_lcc(sub):
    if len(sub) == 0:
        return sub
    rows = np.concatenate([sub["t_idx"].values, sub["d_idx"].values + n_T])
    cols = np.concatenate([sub["d_idx"].values + n_T, sub["t_idx"].values])
    data = np.ones(len(rows), dtype=np.int8)
    adj = coo_matrix((data, (rows, cols)), shape=(n_T + n_D, n_T + n_D)).tocsr()
    _, labels = connected_components(adj, directed=False)
    present = np.unique(np.concatenate([sub["t_idx"].values,
                                          sub["d_idx"].values + n_T]))
    largest = np.bincount(labels[present]).argmax()
    keep_t = labels[sub["t_idx"].values] == largest
    keep_d = labels[sub["d_idx"].values + n_T] == largest
    return sub[keep_t & keep_d]

def ranked_targets(sub):
    """Return target list ordered by descending max overall_score."""
    if len(sub) == 0:
        return []
    target_score = sub.groupby("targetId")["overall_score"].max().sort_values(ascending=False)
    return list(target_score.index)

# Build ranked lists for all 16 cells (once)
cell_labels = []
cell_ranked = []
for f1, f2, f3, f4 in product([0, 1], repeat=4):
    sub = df
    if f1: sub = sub[sub["overall_score"] >= F1_THRESHOLD]
    if f2: sub = sub[sub["n_sources"] >= F2_THRESHOLD]
    if f4: sub = sub[sub["biotype"] == "protein_coding"]
    if f3: sub = apply_lcc(sub)
    label = f"F1={f1} F2={f2} F3={f3} F4={f4}"
    cell_labels.append(label)
    cell_ranked.append(ranked_targets(sub))
    print(f"  {label}: {len(cell_ranked[-1]):,} ranked targets")

n = len(cell_labels)

def jaccard_at_window(rank_lo, rank_hi):
    """Compute pairwise Jaccard using targets at ranks [rank_lo, rank_hi)."""
    cell_sets = [set(r[rank_lo:rank_hi]) for r in cell_ranked]
    J = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = cell_sets[i], cell_sets[j]
            if len(a | b) == 0:
                J[i, j] = np.nan
            else:
                J[i, j] = len(a & b) / len(a | b)
    return J

# Three rank windows
windows = [
    ("Top tier (rank 1–100)",        0, 100),
    ("Middle tier (rank 101–1000)",  100, 1000),
    ("Lower tier (rank 1001–3000)",  1000, 3000),
]

J_matrices = [jaccard_at_window(lo, hi) for _, lo, hi in windows]

# Hierarchical clustering on the middle tier (most informative)
D = 1 - J_matrices[1]
np.fill_diagonal(D, 0)
condensed = squareform(D, checks=False)
linkage_matrix = linkage(condensed, method="average")
order = leaves_list(linkage_matrix)

# Reorder all three matrices using the same ordering
J_ordered = [J[np.ix_(order, order)] for J in J_matrices]
labels_ordered = [cell_labels[i] for i in order]

# === Plot ===
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
})

fig, axes = plt.subplots(1, 3, figsize=(20, 7.5))

for k, (ax, J, (title, lo, hi)) in enumerate(zip(axes, J_ordered, windows)):
    im = ax.imshow(J, cmap="RdYlBu_r", vmin=0, vmax=1, aspect="equal")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks(np.arange(n))
    ax.set_xticklabels(labels_ordered, rotation=45, ha="right", fontsize=7)
    if k == 0:
        ax.set_yticks(np.arange(n))
        ax.set_yticklabels(labels_ordered, fontsize=7)
    else:
        ax.set_yticks([])  # no ticks and no labels on the middle and right panels

# Single shared colorbar on the right
cbar = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.02)
cbar.set_label("Jaccard overlap of targets\n(ranked by max association score)",
               fontsize=10)
cbar.ax.tick_params(labelsize=9)

#plt.suptitle(
#    "Filter agreement decreases as rank tier decreases",
#    fontsize=13, fontweight="bold", y=1.00,
#)

out = "fig6_jaccard_tiered.pdf"
plt.savefig(out, format="pdf", bbox_inches="tight", dpi=300)
plt.savefig(out.replace(".pdf", ".png"), format="png", bbox_inches="tight", dpi=300)
print("Saved.")
plt.show()

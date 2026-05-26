import duckdb
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

con = duckdb.connect()
overall_path = "/mnt/c/Users/chieb/Downloads/OT_data/association_overall_direct/*.parquet"

gene_degree = con.sql(f"""
    SELECT targetId, COUNT(*) AS degree
    FROM '{overall_path}'
    GROUP BY targetId
""").df()

disease_degree = con.sql(f"""
    SELECT diseaseId, COUNT(*) AS degree
    FROM '{overall_path}'
    GROUP BY diseaseId
""").df()

# Paper-ready styling
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
})

fig, ax = plt.subplots(figsize=(8, 5))

# Main panel: gene distribution
n_bins = 30
bins = np.logspace(0, np.log10(gene_degree["degree"].max()), n_bins)
ax.hist(
    gene_degree["degree"], bins=bins,
    color="#3a5a7a",         # muted blue-gray
    edgecolor="none",
    alpha=0.85,
)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Gene degree (number of associated diseases)", fontsize=14)
ax.set_ylabel("Number of genes", fontsize=14)
ax.tick_params(labelsize=12)

# Annotations
ax.axvline(2, linestyle="--", color="#888", linewidth=0.8, alpha=0.7)
ax.axvline(150, linestyle="--", color="#888", linewidth=0.8, alpha=0.7)

ax.text(2, ax.get_ylim()[1] * 0.55, "Sparsely-attested\nmode",
        fontsize=6, color="#444", ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.3", fc="white",
                  ec="#bbb", lw=0.5))
ax.text(150, ax.get_ylim()[1] * 0.55, "Well-studied\nmode",
        fontsize=6, color="#444", ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.3", fc="white",
                  ec="#bbb", lw=0.5))
ax.text(15, ax.get_ylim()[1] * 0.012, "empirical\nscarcity",
        fontsize=8, color="#666", ha="center", va="center",
        style="italic")

# Inset: disease distribution
ax_inset = fig.add_axes([0.62, 0.55, 0.27, 0.30])
inset_bins = np.logspace(0, np.log10(disease_degree["degree"].max()), n_bins)
ax_inset.hist(
    disease_degree["degree"], bins=inset_bins,
    color="#7a5a3a",         # muted brown for contrast
    edgecolor="none",
    alpha=0.85,
)
ax_inset.set_xscale("log")
ax_inset.set_yscale("log")
ax_inset.tick_params(labelsize=8)
ax_inset.set_title("Disease degree distribution\n(smooth heavy tail)",
                   fontsize=7, color="#444", pad=4)
for spine in ax_inset.spines.values():
    spine.set_linewidth(0.6)
ax_inset.spines["top"].set_visible(False)
ax_inset.spines["right"].set_visible(False)

plt.tight_layout()
out = "fig2_degree_distribution.pdf"
plt.savefig(out, format="pdf", bbox_inches="tight", dpi=300)
plt.savefig(out.replace(".pdf", ".png"), format="png", bbox_inches="tight", dpi=300)
print(f"Saved to {out} and {out.replace('.pdf', '.png')}")
plt.show()

import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import matplotlib.patheffects as pe

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

# Rebuild the H3 dataset and model (matches the analysis we already ran)
target_df = con.sql(f"""
    SELECT
        targetId,
        MAX(approvedSymbol) AS symbol,
        MAX(biotype) AS biotype,
        MAX(chromosome) AS chromosome,
        MAX(constraint_bin) AS constraint_bin,
        MAX(n_publications) AS n_publications,
        MAX(ppi_degree_all) AS ppi_degree,
        MAX(attention_missing::INT) AS attn_missing,
        MAX(CASE
              WHEN overall_score >= 0.5
               AND n_sources >= 2
               AND biotype = 'protein_coding'
              THEN 1 ELSE 0
            END) AS survives
    FROM '{analysis}'
    GROUP BY targetId
""").df()

target_df = target_df[
    (target_df["attn_missing"] == 0) &
    (target_df["constraint_bin"].notna()) &
    (target_df["biotype"] == "protein_coding")
].copy()

target_df["log_pubs"] = np.log1p(target_df["n_publications"])
target_df["log_ppi"]  = np.log1p(target_df["ppi_degree"])
target_df["constraint_bin"] = target_df["constraint_bin"].astype(int)

common_chrs = set(str(c) for c in list(range(1, 23)) + ["X"])
target_df["chrom_cat"] = target_df["chromosome"].where(
    target_df["chromosome"].isin(common_chrs), "other"
)

# Refit the M3 model
model = smf.logit(
    "survives ~ log_pubs + C(constraint_bin) + log_ppi + C(chrom_cat)",
    data=target_df).fit(disp=0)
target_df["predicted_p"] = model.predict(target_df)
target_df["residual"] = target_df["survives"] - target_df["predicted_p"]

# Classify each gene by residual category
def classify(r):
    if r < -0.3: return "under"
    if r > 0.3:  return "over"
    return "neutral"
target_df["res_cat"] = target_df["residual"].apply(classify)

print(f"n = {len(target_df):,}")
print(f"  under-survivors (red):   {(target_df['res_cat']=='under').sum():,}")
print(f"  over-survivors  (blue):  {(target_df['res_cat']=='over').sum():,}")
print(f"  neutral (gray):          {(target_df['res_cat']=='neutral').sum():,}")

# Jitter the survival outcome for visibility
rng = np.random.default_rng(seed=42)
jitter_strength = 0.08
target_df["y_jitter"] = target_df["survives"] + rng.uniform(
    -jitter_strength, jitter_strength, size=len(target_df)
)

# highlight genes
under_labels = ["HIF1A", "IFNG", "MDM2"]
over_labels  = ["OR10R2", "PRCD", "GRXCR2"]

to_label_under = target_df[target_df["symbol"].isin(under_labels)].copy()
to_label_over  = target_df[target_df["symbol"].isin(over_labels)].copy()

# === Plot ===
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
})

fig, ax = plt.subplots(figsize=(11, 6.5))

# Plot in three layers so colored points appear on top of gray
colors = {"neutral": "#bbbbbb", "under": "#c0392b", "over": "#2980b9"}
sizes  = {"neutral": 4,           "under": 7,         "over": 7}
alphas = {"neutral": 0.22,        "under": 0.55,      "over": 0.55}

for cat in ["neutral", "over", "under"]:  # under last so it's on top
    sub = target_df[target_df["res_cat"] == cat]
    ax.scatter(sub["log_pubs"], sub["y_jitter"],
               c=colors[cat], s=sizes[cat], alpha=alphas[cat],
               edgecolors="none", label={
                   "neutral": "neutral (|residual| ≤ 0.3)",
                   "under":   "under-survivor (residual < −0.3)",
                   "over":    "over-survivor (residual > +0.3)"
               }[cat])

# Overlay the model's predicted probability curve.
# Average the other covariates: use the modal constraint_bin, mean log_ppi,
# modal chromosome — so the line shows P(survive) as a function of log_pubs
# at "typical" structural settings.
x_grid = np.linspace(0, target_df["log_pubs"].max(), 400)
ref = pd.DataFrame({
    "log_pubs": x_grid,
    "log_ppi":  np.full_like(x_grid, target_df["log_ppi"].mean()),
    "constraint_bin": np.full(len(x_grid), 4),  # midpoint
    "chrom_cat": np.full(len(x_grid), "1"),     # modal chromosome
})
ref["constraint_bin"] = ref["constraint_bin"].astype(int)
p_pred = model.predict(ref)
ax.plot(x_grid, p_pred, color="black", linewidth=1.5,
        label="Model-predicted P(survive)", zorder=10)

# Annotate 
# Under-survivor labels (placed below the y=0 stripe, fanned vertically)
under_y_offsets = [-0.22, -0.30, -0.38]
for (offset_y, (_, row)) in zip(under_y_offsets,
                                  to_label_under.sort_values("log_pubs",
                                                              ascending=False).iterrows()):
    ax.annotate(
        row["symbol"],
        xy=(row["log_pubs"], row["y_jitter"]),
        xytext=(row["log_pubs"], offset_y),
        fontsize=10, color="#5b1a0e", fontweight="bold",
        ha="center", va="center",
        arrowprops=dict(arrowstyle="-", color="#5b1a0e",
                        lw=0.6, alpha=0.7),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")],
        zorder=20,
    )

# Over-survivor labels (placed above the y=1 stripe)
over_y_offsets = [1.22, 1.30, 1.38]
for (offset_y, (_, row)) in zip(over_y_offsets,
                                  to_label_over.sort_values("log_pubs",
                                                              ascending=True).iterrows()):
    ax.annotate(
        row["symbol"],
        xy=(row["log_pubs"], row["y_jitter"]),
        xytext=(row["log_pubs"], offset_y),
        fontsize=10, color="#1e3f5e", fontweight="bold",
        ha="center", va="center",
        arrowprops=dict(arrowstyle="-", color="#1e3f5e",
                        lw=0.6, alpha=0.7),
        path_effects=[pe.withStroke(linewidth=2.5, foreground="white")],
        zorder=20,
    )

# annotation boxes
ax.text(6.0, 0.28,
        "Under-survivors:\nhighly-published genes\nthat did not survive",
        fontsize=10, color="#5b1a0e", ha="center", va="top", style="italic",
        bbox=dict(boxstyle="round,pad=0.4", fc="white",
                  ec="#c0392b", lw=0.8, alpha=0.95))

ax.text(3.0, 1.3,
        "Over-survivors:\nlow-publication genes\nthat survived",
        fontsize=10, color="#1e3f5e", ha="left", va="top", style="italic",
        bbox=dict(boxstyle="round,pad=0.4", fc="white",
                  ec="#2980b9", lw=0.8, alpha=0.95))

# Axes
ax.set_xlabel("log(publications + 1)", fontsize=16)
ax.set_ylabel("Survival in F1 ∧ F2 ∧ F4",
              fontsize=16)
ax.set_yticks([0, 1])
ax.set_yticklabels(["did not survive (0)", "survived (1)"])
ax.set_ylim(-0.35, 1.35)
ax.set_xlim(left=-0.3)

# Legend
leg = ax.legend(loc="center right", fontsize=10, frameon=True,
                framealpha=0.95, edgecolor="#bbb")
leg.set_zorder(30)

plt.tight_layout()
out = "fig5_h3_under_survivors.pdf"
plt.savefig(out, format="pdf", bbox_inches="tight", dpi=300)
plt.savefig(out.replace(".pdf", ".png"), format="png", bbox_inches="tight", dpi=300)
print("Saved.")
plt.show()

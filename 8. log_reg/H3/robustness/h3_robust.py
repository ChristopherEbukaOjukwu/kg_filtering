import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

# Same per-target dataset as H3 main, but pull both PPI variants
target_df = con.sql(f"""
    SELECT
        targetId,
        MAX(approvedSymbol) AS symbol,
        MAX(biotype) AS biotype,
        MAX(chromosome) AS chromosome,
        MAX(constraint_bin) AS constraint_bin,
        MAX(n_publications) AS n_publications,
        MAX(ppi_degree_all)      AS ppi_all,
        MAX(ppi_degree_curated)  AS ppi_cur,
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

target_df["log_pubs"]    = np.log1p(target_df["n_publications"])
target_df["log_ppi_all"] = np.log1p(target_df["ppi_all"])
target_df["log_ppi_cur"] = np.log1p(target_df["ppi_cur"])
target_df["constraint_bin"] = target_df["constraint_bin"].astype(int)

common_chrs = set(str(c) for c in list(range(1, 23)) + ["X"])
target_df["chrom_cat"] = target_df["chromosome"].where(
    target_df["chromosome"].isin(common_chrs), "other"
)

print(f"n = {len(target_df):,} protein-coding mapped targets with constraint")
print(f"  surviving F1∧F2∧F4: {target_df['survives'].sum():,}  "
      f"({100*target_df['survives'].mean():.1f}%)")

print(f"\nPPI degree summary (log scale):")
print(f"  log_ppi_all: mean={target_df['log_ppi_all'].mean():.2f}, "
      f"median={target_df['log_ppi_all'].median():.2f}, "
      f"missing={target_df['ppi_all'].isna().sum()}")
print(f"  log_ppi_cur: mean={target_df['log_ppi_cur'].mean():.2f}, "
      f"median={target_df['log_ppi_cur'].median():.2f}, "
      f"missing={target_df['ppi_cur'].isna().sum()}")

# Fit two parallel H3 models
m_all = smf.logit(
    "survives ~ log_pubs + C(constraint_bin) + log_ppi_all + C(chrom_cat)",
    data=target_df).fit(disp=0)
m_cur = smf.logit(
    "survives ~ log_pubs + C(constraint_bin) + log_ppi_cur + C(chrom_cat)",
    data=target_df).fit(disp=0)

# Compare key statistics
target_df["pred_all"] = m_all.predict(target_df)
target_df["pred_cur"] = m_cur.predict(target_df)
target_df["resid_all"] = target_df["survives"] - target_df["pred_all"]
target_df["resid_cur"] = target_df["survives"] - target_df["pred_cur"]

print("\n=== Model comparison: broad vs. curated PPI ===")
print(f"{'Statistic':<35} {'PPI=all (STRING)':>20} {'PPI=curated':>15}")
print(f"{'AUC':<35} {roc_auc_score(target_df.survives, target_df.pred_all):>20.4f} "
      f"{roc_auc_score(target_df.survives, target_df.pred_cur):>15.4f}")
print(f"{'Log-likelihood':<35} {m_all.llf:>20,.1f} {m_cur.llf:>15,.1f}")
print(f"{'AIC':<35} {m_all.aic:>20,.1f} {m_cur.aic:>15,.1f}")
print(f"{'β_log_pubs':<35} {m_all.params['log_pubs']:>20.4f} "
      f"{m_cur.params['log_pubs']:>15.4f}")
print(f"{'β_log_ppi':<35} {m_all.params['log_ppi_all']:>20.4f} "
      f"{m_cur.params['log_ppi_cur']:>15.4f}")
print(f"{'p(β_log_ppi)':<35} {m_all.pvalues['log_ppi_all']:>20.3e} "
      f"{m_cur.pvalues['log_ppi_cur']:>15.3e}")

# Under-survivor list overlap
under_all = set(target_df.nsmallest(100, "resid_all")["symbol"])
under_cur = set(target_df.nsmallest(100, "resid_cur")["symbol"])
overlap = under_all & under_cur

print(f"\n=== Under-survivor overlap (top 100 by residual) ===")
print(f"Top-100 in PPI-all:     {len(under_all)}")
print(f"Top-100 in PPI-curated: {len(under_cur)}")
print(f"Overlap:                {len(overlap)}  ({100*len(overlap)/100:.0f}%)")

# Pearson correlation between residual vectors
r_resid = target_df["resid_all"].corr(target_df["resid_cur"])
print(f"\nCorrelation between residual vectors: r = {r_resid:.4f}")

# Show top-20 under-survivors from BOTH models side-by-side
top_all = target_df.nsmallest(20, "resid_all")[["symbol", "log_pubs", "constraint_bin", "log_ppi_all", "pred_all", "resid_all"]]
top_cur = target_df.nsmallest(20, "resid_cur")[["symbol", "log_pubs", "constraint_bin", "log_ppi_cur", "pred_cur", "resid_cur"]]

print("\n=== Top 20 under-survivors (PPI=all) ===")
print(top_all.to_string(index=False))

print("\n=== Top 20 under-survivors (PPI=curated) ===")
print(top_cur.to_string(index=False))

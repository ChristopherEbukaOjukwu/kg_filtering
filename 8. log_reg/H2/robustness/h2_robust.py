import duckdb, numpy as np, pandas as pd
import statsmodels.formula.api as smf

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

df = con.sql(f"SELECT overall_score, n_sources, biotype FROM '{analysis}'").df()

def build_contingency(df, f1_thresh, f2_thresh):
    p1 = (df["overall_score"] >= f1_thresh).astype(int)
    p2 = (df["n_sources"]     >= f2_thresh).astype(int)
    p4 = (df["biotype"] == "protein_coding").astype(int)
    # Always emit all 8 cells, even empty ones, so the GLM has a complete design
    full = pd.MultiIndex.from_product([[0,1],[0,1],[0,1]], names=["p1","p2","p4"]).to_frame(index=False)
    obs  = pd.DataFrame({"p1": p1, "p2": p2, "p4": p4}).groupby(
        ["p1","p2","p4"]).size().reset_index(name="count")
    cont = full.merge(obs, on=["p1","p2","p4"], how="left").fillna(0)
    cont["count"] = cont["count"].astype(int)
    return cont

def run_factorial(df, f1_thresh, f2_thresh, label):
    cont = build_contingency(df, f1_thresh, f2_thresh)
    n_empty = (cont["count"] == 0).sum()
    # Apply +0.5 continuity correction if any cell is empty
    fit_cont = cont.copy()
    if n_empty > 0:
        fit_cont["count"] = fit_cont["count"] + 0.5
    N = cont["count"].sum()
    p1m = cont.loc[cont["p1"]==1, "count"].sum() / N
    p2m = cont.loc[cont["p2"]==1, "count"].sum() / N
    p4m = cont.loc[cont["p4"]==1, "count"].sum() / N
    indep_111 = N * p1m * p2m * p4m
    actual_111 = cont.loc[
        (cont["p1"]==1)&(cont["p2"]==1)&(cont["p4"]==1), "count"
    ].iloc[0]
    try:
        m2 = smf.poisson("count ~ C(p1)*C(p2) + C(p1)*C(p4) + C(p2)*C(p4)",
                         data=fit_cont).fit(disp=0)
        b12 = m2.params.get("C(p1)[T.1]:C(p2)[T.1]", np.nan)
        b14 = m2.params.get("C(p1)[T.1]:C(p4)[T.1]", np.nan)
        b24 = m2.params.get("C(p2)[T.1]:C(p4)[T.1]", np.nan)
    except Exception as e:
        b12 = b14 = b24 = np.nan
    return {
        "label": label,
        "n_empty_cells": n_empty,
        "n_f1f2f4":      int(actual_111),
        "indep_pred":    int(round(indep_111)),
        "fold_over_indep": actual_111 / max(indep_111, 1),
        "beta_f1xf2":    b12, "exp_f1xf2": np.exp(b12),
        "beta_f1xf4":    b14, "exp_f1xf4": np.exp(b14),
        "beta_f2xf4":    b24, "exp_f2xf4": np.exp(b24),
    }

settings = [
    ("Permissive (F1≥0.2)",  0.2, 2),
    ("Default    (F1≥0.5)",  0.5, 2),
    ("Stringent  (F1≥0.8)",  0.8, 2),
    ("Stringent F2 (≥3)",    0.5, 3),
]
results = [run_factorial(df, f1, f2, label) for label, f1, f2 in settings]
robust = pd.DataFrame(results)

print("\n=== Robustness across settings ===\n")
print(robust[["label", "n_empty_cells", "n_f1f2f4", "indep_pred", "fold_over_indep"]].to_string(index=False))
print("\n=== H2 interaction effects (log-scale β and fold exp(β)) ===\n")
print(robust[["label",
              "beta_f1xf2","exp_f1xf2",
              "beta_f1xf4","exp_f1xf4",
              "beta_f2xf4","exp_f2xf4"]].to_string(index=False))

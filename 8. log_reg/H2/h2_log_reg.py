import duckdb
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import chi2

con = duckdb.connect()
analysis = "/mnt/c/Users/chieb/Downloads/OT_data/analysis.parquet"

df = con.sql(f"""
    SELECT
        (overall_score >= 0.5)::INT AS p1,
        (n_sources >= 2)::INT       AS p2,
        (biotype = 'protein_coding')::INT AS p4
    FROM '{analysis}'
""").df()

contingency = df.groupby(["p1", "p2", "p4"]).size().reset_index(name="count")
contingency = contingency.sort_values(["p1", "p2", "p4"]).reset_index(drop=True)
print("Contingency table:")
print(contingency.to_string(index=False))

# Fit nested models
model_main = smf.poisson("count ~ C(p1) + C(p2) + C(p4)",
                          data=contingency).fit(disp=0)
model_2way = smf.poisson("count ~ C(p1) * C(p2) + C(p1) * C(p4) + C(p2) * C(p4)",
                          data=contingency).fit(disp=0)
model_satd = smf.poisson("count ~ C(p1) * C(p2) * C(p4)",
                          data=contingency).fit(disp=0)

print("\n=== Main effects only ===")
print(model_main.summary().tables[1])
print(f"Log-likelihood: {model_main.llf:,.1f}   params: {model_main.df_model}")

print("\n=== 2-way interactions ===")
print(model_2way.summary().tables[1])
print(f"Log-likelihood: {model_2way.llf:,.1f}   params: {model_2way.df_model}")

print("\n=== Saturated (3-way) ===")
print(model_satd.summary().tables[1])
print(f"Log-likelihood: {model_satd.llf:,.1f}   params: {model_satd.df_model}")

# Likelihood ratio tests
lr_1 = 2 * (model_2way.llf - model_main.llf)
df_1 = model_2way.df_model - model_main.df_model
p_1  = chi2.sf(lr_1, df_1)

lr_2 = 2 * (model_satd.llf - model_2way.llf)
df_2 = model_satd.df_model - model_2way.df_model
p_2  = chi2.sf(lr_2, df_2)

print(f"\n=== Likelihood ratio tests ===")
print(f"Main → 2-way:    LR = {lr_1:,.1f}  df = {df_1}  p = {p_1:.2e}")
print(f"2-way → 3-way:   LR = {lr_2:,.1f}  df = {df_2}  p = {p_2:.2e}")

# Effect sizes for the 2-way model — the interaction coefficients
# are on the log scale; exponentiating gives the multiplicative
# departure from independence.
print("\n=== 2-way interaction effect sizes (exp(β)) ===")
print("These are the ratios of observed/expected-under-independence.")
print("Values far from 1.0 = strong non-linear compounding.")
params = model_2way.params
for name, val in params.items():
    if ":" in name:
        print(f"  {name:50s}  β = {val:8.3f}   exp(β) = {np.exp(val):8.3f}")

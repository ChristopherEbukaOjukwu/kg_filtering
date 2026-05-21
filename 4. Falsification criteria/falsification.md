# Falsification Criteria for Determining Whether Hypotheses Hold

## Filter Thresholds

The main analysis uses the following filter settings:

| Filter | Main Setting | Robustness Checks |
|---|---|---|
| **F1** | Overall association score `≥ 0.5` | `≥ 0.2`, `≥ 0.8` |
| **F2** | `≥ 2` distinct data sources | `≥ 3` distinct data sources |
| **F3** | Restrict to the largest connected component | No threshold |
| **F4** | `biotype = protein_coding` | Genetic-associations data type restriction |

---

## Analysis Universe

The analysis universe consists of all target–disease pairs in:

```text
association_overall_direct
```

restricted to mapped targets.

Approximate mapped target universe:

```text
~28,000 targets after gene2ensembl mapping
```

For **H3**, the analysis is further restricted to targets with:

```text
n_publications > 0
```

This restriction is used to enable attention-based regression.

---

# H1: Each Filter Individually Retains Higher-Attention Genes

## Claim

Apply each filter alone.

For each filter, compare the mean publication attention of surviving genes versus dropped genes.

Attention is measured as:

```text
log(n_publications + 1)
```

The hypothesis is supported if surviving genes systematically have higher publication attention than dropped genes.

---

## H1 Supported If

For each of **F1**, **F2**, **F3**, and **F4** applied alone:

```text
mean log(pubs + 1) of surviving genes
>
mean log(pubs + 1) of dropped genes
```

by at least:

```text
0.5 log-units
```

This corresponds to roughly a:

```text
~1.6× difference in raw publication counts
```

The effect must also be statistically significant using:

```text
Mann-Whitney U test, p < 0.001
```

for at least:

```text
3 of 4 filters
```

---

## H1 Failed If

H1 fails if, for **2 or more filters**:

```text
attention gap between survivors and dropped genes < 0.2 log-units
```

or if the gap is in the opposite direction.

---

## Interpretation If Mixed

If **F3** or **F4** show no attention-associated retention individually, that is still a finding.

In that case, the interpretation becomes:

```text
Evidence-based filters such as F1 and F2 carry attention-associated retention,
while structural/type filters such as F3 and F4 do not.
```

So, H1 should not be treated as fully failed if only F1 and F2 show the effect.

Instead, the claim should be revised to distinguish between:

- evidence-based filters
- structural filters
- type-based filters

---

# H2: Stacked Filters Compound Non-Linearly

## Claim

Run the full `2⁴` factorial filter design.

This means testing every combination of the four filters:

```text
F1, F2, F3, F4
```

Then model gene survival probability as a function of filter indicators and their interactions.

Non-zero interaction coefficients indicate that the filters are not acting independently.

---

## Statistical Setup

Use logistic regression on per-gene survival:

```text
survive_i =
    β₀
  + β₁·F1
  + β₂·F2
  + β₃·F3
  + β₄·F4
  + β₁₂·F1·F2
  + β₁₃·F1·F3
  + β₁₄·F1·F4
  + β₂₃·F2·F3
  + β₂₄·F2·F4
  + β₃₄·F3·F4
  + optional higher-order terms
```

where each filter is a binary indicator:

```text
1 = filter applied
0 = filter not applied
```

Higher-order interaction terms may be added if pairwise interactions underdescribe the observed compounding.

---

## H2 Supported If

At least:

```text
2 of 6 pairwise interaction terms
```

have:

```text
|β| ≥ 0.3
```

on the log-odds scale, with:

```text
p < 0.01
```

after Bonferroni correction.

In addition:

```text
Top-100 gene overlap between F1-alone survivors
and F1 ∧ F2 ∧ F3 ∧ F4 survivors is < 0.7
```

This means stacking removes more than 30% of the F1-surviving gene set, despite each additional filter individually removing only a fraction of genes.

---

## H2 Failed If

H2 fails if:

```text
all pairwise interactions have |β| < 0.1
```

or if:

```text
Top-100 overlap exceeds 0.85
```

This would suggest that the filters are nearly redundant or acting mostly independently.

---

## Pivot If H2 Fails

If H2 fails, the chapter can pivot to:

```text
Filters are largely redundant: a methodological note on apparent multi-filter robustness in published pipelines.
```

In that case, the finding would be that stacking filters does not strongly alter the retained gene set beyond what individual filters already do.

---

# H3: Some Genes Under-Survive Relative to an Attention Baseline

## Claim

Build a logistic regression model predicting survival from publication attention and structural covariates.

Then identify genes whose actual survival is lower than predicted.

These genes are the:

```text
should-be-kept-but-are-not
```

cases under the model.

---

## Statistical Setup

Baseline model:

```text
P(survive_i | F1 ∧ F2 ∧ F3 ∧ F4)
=
logit⁻¹(α + γ·log(pubs_i + 1) + δ·structural_covariates_i)
```

Structural covariates include:

1. `biotype`
   - categorical
   - restricted to protein-coding genes for the main analysis

2. `chromosome`
   - categorical
   - used to absorb chromosomal biases

Compute residuals as:

```text
residual_i = actual_survival_i - predicted_P_i
```

Interpretation:

```text
negative residual = gene survived less than expected
positive residual = gene survived more than expected
```

---

## H3 Supported If

The baseline model has:

```text
AUC < 0.85
```

on hold-out data.

This means attention and structural covariates do not perfectly explain survival.

Additionally:

```text
at least 5% of genes have |residual| > 0.3
```

This indicates that a substantial under-survival or over-survival population exists.

Finally, the bottom-100 residual genes, meaning the most under-surviving genes, must show non-random structural enrichment.

At least one category must be over-represented at:

```text
p < 0.01
```

compared to the background.

Possible categories include:

- biotype
- chromosome
- constraint category
- other structural annotations

---

## H3 Failed If

H3 fails if:

```text
baseline AUC ≥ 0.95
```

This would mean that attention and structural covariates almost fully explain survival.

H3 also fails if:

```text
under-survivor residuals show no structural pattern beyond noise
```

---

## Hard Interpretation Rule

Even if H3 is supported, the interpretation must remain conservative.

Do **not** claim that under-surviving genes are:

```text
biologically important but unfairly excluded
```

The defensible claim is only:

```text
These genes survive filtering at rates lower than their measured attention
and structural features predict.
```

Causal interpretation requires evidence not available in this analysis.

For example, this analysis cannot distinguish between:

- genes being incorrectly excluded
- genes being correctly removed because of weak evidence
- genes being structurally disadvantaged by database coverage
- genes being peripheral to the filtered graph construction

---

# Cross-Cutting Commitments

## No Threshold Tuning After Seeing Results

The main F1 threshold is:

```text
F1 ≥ 0.5
```

Robustness thresholds are:

```text
F1 ≥ 0.2
F1 ≥ 0.8
```

Do not retroactively change the main threshold after seeing the results.

For example, if H2 fails at `0.5` but succeeds at `0.3`, do not switch the main analysis to `0.3`.

Instead, report all threshold results and treat inconsistency as part of the finding.

---

## Multiple Comparisons

For H2, there are:

```text
6 pairwise interaction terms
```

Using Bonferroni correction at:

```text
α = 0.01
```

means the individual test threshold is:

```text
p < 0.00167
```

This should be stated in the methods.

---

## Effect Size Reporting

Report all interaction terms regardless of statistical significance.

The main story is about effect magnitude, not only p-values.

```text
p-values are screening tools.
β coefficients carry the actual substantive claim.
```

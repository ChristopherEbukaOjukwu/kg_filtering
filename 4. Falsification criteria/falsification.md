# Falsification Criteria for Determining Whether Hypotheses Hold

This section enumerates several criteria for determining whether our hypotheses hold. 

## Filter Thresholds

The main analysis uses the following filter settings:

| Filter | Main Setting | Robustness Checks |
|---|---|---|
| **F1** | Overall association score `≥ 0.5` | `≥ 0.2`, `≥ 0.8` |
| **F2** | `≥ 2` distinct data sources | `≥ 3` distinct data sources |
| **F3** | Restrict to the largest connected component | No threshold |
| **F4** | `biotype = protein_coding` | Genetic-associations data type restriction |

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

In the case that **F3** or **F4** shows no attention-associated retention individually, the interpretation becomes:

```text
Evidence-based filters such as F1 and F2 carry attention-associated retention,
while structural/type filters such as F3 and F4 do not.
```

So, H1 is not treated as fully failed if only F1 and F2 show the effect.

Instead, we distinguish between:

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

Logistic regression is used because gene survival is a binary outcome: each gene either survives filtering or does not.

The β coefficients estimate how much each filter changes the probability of survival. Negative β values mean the filter reduces survival. Interaction coefficients, such as β₁₂ for F1×F2, test whether two filters together have an effect beyond their individual effects.

For H2, the interaction terms are the key quantities because they show whether stacked filters compound non-linearly rather than acting independently.


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

## If H2 Fails

If H2 fails:

```text
Filters are largely redundant.
```

In that case, stacking filters does not strongly alter the retained gene set beyond what individual filters already do.

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

where:

- survive_i indicates whether gene i survives the full filter stack.
- F1 ∧ F2 ∧ F3 ∧ F4 means all four filters are applied together.
- pubs_i is the publication count for gene i.
- log(pubs_i + 1) is the log-transformed publication count.
- X_i represents additional gene-level covariates.
- α is the baseline intercept.
- γ estimates the association between publication attention and survival.
- δ estimates the association between covariates and survival.
- logit⁻¹ converts the linear model output into a probability between 0 and 1.

  
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

Even if H3 is supported, the interpretation is conservative.

We do **not** claim that under-surviving genes are:

```text
biologically important but unfairly excluded
```

Our claim is only:

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

(This should be stated in the methods).

---

## Effect Size Reporting

```text
p-values are screening tools.
β coefficients carry the actual substantive claim.
```

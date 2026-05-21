# H2 Logistic Regression

## Setup

The H2 analysis tests whether the four filters compose independently or whether they interact.

### Unit of Analysis

The unit of analysis is the:

```text
target–disease pair
```

The full analysis population is:

```text
4,508,002 target–disease pairs
```

---

## Outcome Variable

The outcome variable is survival in the fully filtered cell:

```text
F1 ∧ F2 ∧ F3 ∧ F4
```

This is binary:

```text
1 = target–disease pair survives the full filter stack
0 = target–disease pair does not survive the full filter stack
```

---

## Predictors

The predictors are binary indicators for whether each target–disease pair passes each individual filter:

```text
passes_F1
passes_F2
passes_F3
passes_F4
```

where:

```text
1 = pair passes the filter
0 = pair does not pass the filter
```

The model also includes pairwise interaction terms:

```text
F1 × F2
F1 × F3
F1 × F4
F2 × F3
F2 × F4
F3 × F4
```

---

# Conceptual Question

The core question is:

```text
Can fully stacked survival be explained by the individual filters alone,
or do the filters interact?
```

If the individual filter indicators predict stacked survival with little interaction, then the filters are mostly composing additively.

If interaction effects are large, then the filters are not independent. Instead, the effect of one filter depends on whether another filter has already been applied.

This would support H2.

---

# Important Subtlety

H2 is not simply asking whether individual filter flags predict full-stack survival.

That would be partly trivial, because the fully filtered cell is defined by the filters.

The real H2 question is:

```text
Does the size and composition of each filtered subgraph deviate from what the marginal filter rates would predict under independence?
```

In other words:

```text
Are the filters combining in a way that is more or less selective than expected from their individual retention rates?
```

---

# The Log-Linear Setup

Let:

```text
n_abcd
```

be the count of target–disease pairs in the factorial cell:

```text
(F1 = a, F2 = b, F3 = c, F4 = d)
```

where each of:

```text
a, b, c, d ∈ {0, 1}
```

The 16 values of `n_abcd` come from the full `2⁴` factorial table.

---

## Independence Expectation

Under independence of the four filters, the expected count in each cell would be proportional to the product of the marginal filter probabilities:

```text
E[n_abcd] ∝ P(F1 = a) × P(F2 = b) × P(F3 = c) × P(F4 = d)
```

If the observed cell counts deviate from this multiplicative expectation, that deviation indicates interaction among the filters.

---

# Poisson / Log-Linear Model

A Poisson regression can be fit to the 16 factorial cell counts.

The model decomposes deviations from independence into:

- main effects
- two-way interactions
- optional higher-order interactions

Conceptually:

```text
log(E[n_abcd]) =
    β₀
  + β₁F1
  + β₂F2
  + β₃F3
  + β₄F4
  + β₁₂(F1 × F2)
  + β₁₃(F1 × F3)
  + β₁₄(F1 × F4)
  + β₂₃(F2 × F3)
  + β₂₄(F2 × F4)
  + β₃₄(F3 × F4)
```

where:

- `β₀` is the baseline log-count.
- `β₁`, `β₂`, `β₃`, and `β₄` are main effects for each filter.
- interaction coefficients such as `β₁₂` measure whether two filters combine differently than expected from their individual effects.

---

# Interpretation of Interaction Terms

Significant interaction coefficients indicate that the filters are not acting independently.

For example:

```text
β₁₂ ≠ 0
```

means that F1 and F2 interact.

In plain terms:

```text
The effect of F1 depends on whether F2 is also applied,
or the effect of F2 depends on whether F1 is also applied.
```

If multiple interaction terms are large, H2 is supported.

---

# Nested-Subset Issue

One complication is that the factorial cells are not independent populations.

Each filtered cell is a subset of the original unfiltered target–disease universe.

Therefore, the analysis should be framed carefully.

Instead of treating the 16 cells as unrelated groups, we recast the data as a `2⁴` contingency table over the four binary filter-pass indicators:

```text
passes_F1
passes_F2
passes_F3
passes_F4
```

for each of the:

```text
4,508,002 target–disease pairs
```

This preserves the correct relationship between the filters and the original data universe.

---

# Practical Implementation

Although the H2 logic can be expressed using the 16-cell factorial table, the practical implementation uses the per-pair version for clarity and ease of fitting.

Source script:

```text
h2_log_reg.py
```

---

# H2 Decision Rule

H2 is supported if the fitted model shows meaningful interaction effects among filters.

In practical terms:

```text
Large interaction terms = filters compound non-linearly
Small interaction terms = filters are mostly additive or redundant
```

The key test is whether stacked filtering produces survivor sets that differ from what would be expected based only on individual filter retention rates.

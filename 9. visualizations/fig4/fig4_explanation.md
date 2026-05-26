# What the Figure Shows

Filters applied together do not just randomly combine separate rules; they stack rules that often point toward the same subset.

## Panel A: Compounding Strength Across Thresholds

Panel A shows four bars, one for each threshold setting.

Each bar shows the ratio between:

```text
observed count of pairs surviving F1 ∧ F2 ∧ F4
```

and:

```text
count predicted under independent filtering
```

The y-axis is log-scaled.

A horizontal dashed line at:

```text
1.0
```

marks the independence baseline.

If the filters acted independently, every bar would sit on this line.

---

## Panel A Results

All four bars sit far above the independence baseline.

| Threshold Setting | Fold Over Independence |
|---|---:|
| Permissive: F1 ≥ 0.2 | 4.2× |
| Default: F1 ≥ 0.5 | 13.0× |
| Stringent: F1 ≥ 0.8 | 25.8× |
| Stringent F2: ≥ 3 sources | 56.3× |

The trend is monotone and substantial.

As filters become more selective, the gap between observed survival and independence-predicted survival grows.

The minimum compounding effect is:

```text
4.2×
```

under the permissive threshold.

The maximum compounding effect is:

```text
56.3×
```

under the stringent F2 setting.

Across all four settings, the filters compound super-multiplicatively.

---

## Key Interpretation from Panel A

The fact that:

```text
4.2×
```

is the lowest value seen anywhere is itself a finding.

Even under the most permissive threshold tested, the joint filter cell contains roughly four times more target–disease pairs than independent filtering would predict.

In simple terms:

```text
H2 is supported even under lenient filtering.
```

---

# Panel B: Pairwise Interaction Coefficients

Panel B shows twelve bars in three colors, grouped by threshold setting.

Each color tracks one pairwise interaction term from the log-linear model.

The plotted quantity is:

```text
exp(β)
```

where `β` is the log-linear interaction coefficient.

The y-axis is log-scaled to keep all values visible because the interaction strengths span several orders of magnitude.

---

## Reading Panel B by Interaction

### F1 × F2

The F1 × F2 interaction increases sharply as F1 becomes more stringent.

| Setting | exp(β) |
|---|---:|
| Permissive | 7.4× |
| Default | 27.1× |
| Stringent | 35,030× |
| Stringent F2 | 143× |

F1 × F2 is the largest interaction at the default and stringent settings.

The stringent F1 value is marked as a sparse-cell estimate.

---

### F1 × F4

The F1 × F4 interaction is largest at the permissive threshold.

| Setting | exp(β) |
|---|---:|
| Permissive | 39.2× |
| Default | 6.0× |
| Stringent | 8.0× |
| Stringent F2 | 7.3× |

At the permissive setting, the looser F1 threshold allows more non-protein-coding pairs to pass.

This gives F4 more marginal work to do.

At stricter F1 thresholds, F1 already implicitly selects for protein-coding targets, so the marginal contribution of F4 becomes smaller.

---

### F2 × F4

The F2 × F4 interaction is the smallest of the three pairwise interactions, but it is still above the no-interaction baseline in every setting.

| Setting | exp(β) |
|---|---:|
| Permissive | 3.3× |
| Default | 4.7× |
| Stringent | 5.2× |
| Stringent F2 | 10.6× |

The F2 × F4 interaction grows modestly with F2 stringency.

---

# Main Patterns in Panel B

Panel B shows two important patterns.

## 1. No Interaction Is Null

All twelve bars sit above:

```text
1×
```

which is the no-interaction baseline.

This means that, regardless of threshold setting, all three filter pairs interact super-multiplicatively.

In simple terms:

```text
Every tested filter pair co-occurs more often than independence predicts.
```

---

## 2. The Dominant Interaction Depends on Threshold

The strongest interaction changes depending on threshold setting.

| Threshold Setting | Dominant Interaction |
|---|---|
| Permissive | F1 × F4 |
| Default | F1 × F2 |
| Stringent | F1 × F2 |
| Stringent F2 | F1 × F2 |

This is mechanistically interpretable.

At low F1 thresholds, evidence quality and biotype carve out different populations, so their joint constraint is informative.

At high F1 thresholds, evidence quality has already done much of the work of selecting protein-coding targets.

Therefore, F1 × F2 dominates under stricter evidence filtering.

---

# Sparse-Cell Caveat for Stringent F1 × F2

The Stringent F1 × F2 bar requires an explicit caveat.

At:

```text
F1 ≥ 0.8
```

three of the eight contingency cells are empty.

Without a continuity correction, the model’s Hessian is singular.

The reported value:

```text
35,030×
```

comes from a `+0.5` Haldane continuity correction.

This value should be interpreted as order-of-magnitude rather than precise.

The substantive conclusion is:

```text
The interaction is so large that essentially all stringent-F1 survivors also satisfy F2.
```

The asterisk and italicized label in the figure should communicate this caveat clearly.

---

# What the Two Panels Together Establish

Panel A shows that the joint filter cell departs substantially from independence across every threshold setting.

Panel B shows that this departure is not caused by one filter alone.

Instead, it reflects genuine pairwise interactions that vary with stringency.

Together, the panels establish that H2 is robust.

The non-linear compounding result is not a knife-edge sensitivity to the default threshold:

```text
F1 ≥ 0.5
```

Instead, non-linear compounding appears to be a structural property of the filter stack.

---

# Caption

**Figure 4. Filter stacking compounds non-linearly across the range of practitioner-reported thresholds (H2).**  
(A) Ratio between the observed count of target–disease pairs surviving F1 ∧ F2 ∧ F4 and the count predicted under independence of the three filters, across four threshold settings spanning permissive, default, and stringent filtering regimes. The y-axis is log-scaled; the dashed line marks the independence baseline. All four settings yield fold-over-independence values of 4× or greater, with the magnitude growing monotonically with filter stringency.  
(B) Pairwise interaction coefficients, plotted as `exp(β)`, from log-linear Poisson regression on the `2³` contingency table of filter-pass indicators for the same four settings. Each filter pair is shown separately. The y-axis is log-scaled; the dashed line marks `exp(β) = 1`, corresponding to no interaction. All twelve interaction terms exceed the no-interaction baseline, supporting H2 in every setting. The dominant interaction shifts with threshold: F1 × F4 dominates at the permissive setting, while F1 × F2 dominates at default and stringent settings. The Stringent F1 × F2 value, marked with an asterisk, is estimated with a `+0.5` Haldane continuity correction because three of the eight contingency cells are empty at F1 ≥ 0.8, where all F1 survivors also satisfy F2 and are protein-coding. The reported value is therefore order-of-magnitude rather than precise. The robustness of H2 across thresholds, combined with the interpretable shift in dominant interactions, indicates that non-linear compounding is a structural property of the filter stack rather than an artifact of any single threshold choice.

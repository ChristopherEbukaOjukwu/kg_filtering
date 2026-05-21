# What the Factorial Shows

## 1. H1: Attention-Associated Retention Is Strongly Supported

The factorial results support H1 decisively.

Mean publication attention increases monotonically as filters are added, exactly as predicted.

Attention is measured as:

```text
log(n_publications + 1)
```

Approximate raw publication counts are recovered as:

```text
exp(mean_log_pubs) - 1
```

---

## Mean Attention Across Filter Cells

| Filter Cell | Mean `log(pubs + 1)` | Approx. Publications per Gene |
|---|---:|---:|
| No filters | 2.59 | ~13 |
| F4 alone | 3.76 | ~43 |
| F2 alone | 4.12 | ~61 |
| F1 alone | 4.41 | ~82 |
| F1 ∧ F2 | 4.63 | ~102 |
| F1 ∧ F2 ∧ F3 ∧ F4 | 4.75 | ~116 |

Every filter individually raises the mean attention level among surviving genes.

The fully filtered cell has approximately:

```text
~9× more publications per surviving gene
```

than the unfiltered baseline.

This supports H1 with a substantially larger effect size than the preregistered threshold of:

```text
≥ 0.5 log-units
```

The gap between the unfiltered baseline and any single-filter cell exceeds:

```text
1 log-unit
```

---

## Variance Also Declines

The variance of `log(pubs + 1)` also drops monotonically:

```text
3.77 → 1.07
```

This means the filters do not only shift the mean attention level upward.

They also make the surviving gene population more homogeneous around well-studied genes.

Simply,

```text
Filtering both increases attention and narrows the survivor set.
```

---

# 2. F3: Largest Connected Component Does Almost Nothing

F3 has almost no effect on the unfiltered graph.

| Condition | Surviving Pairs |
|---|---:|
| Without F3 | 4,508,002 |
| With F3 | 4,508,001 |

Only one target–disease pair is removed.

This means the unfiltered graph is already essentially one connected component.

There is little peripheral structure for F3 to remove.

---

## Interpretation

F3 only begins to matter after filters such as F1 or F2 carve the graph into smaller pieces and expose isolated subgraphs.

Even then, F3 removes only a few thousand pairs at most.

This changes the H2 story.

The non-linear compounding effect is unlikely to be driven by F3.

Instead, the main interaction effects will likely come from:

```text
F1 × F2
F1 × F4
F2 × F4
```

rather than interactions involving F3.


---

# 3. F4: Protein-Coding Constraint Does Little Once Other Filters Are Applied

F4 removes many targets when applied alone, but it adds very little once F1 or F2 is already applied.

## Protein-Coding Composition

| Filter Cell | Total Targets | Protein-Coding Targets | Percent Protein-Coding |
|---|---:|---:|---:|
| No filters | 31,275 | 19,596 | 62.7% |
| F1 alone | 8,233 | 8,142 | 98.9% |
| F1 ∧ F2 | 5,815 | 5,792 | 99.6% |

F1 by itself almost completely selects for protein-coding genes.

Applying F4 on top of F1 removes only:

```text
91 targets out of 8,142
```

---

## Interpretation

F4 does substantial work alone:

```text
31,275 total targets → 19,596 protein-coding targets
```

This removes:

```text
11,679 targets
```

But after F1 is applied, F4 does almost no additional work:

```text
8,142 protein-coding F1 survivors
```

Only 91 targets are removed by adding F4 on top of F1.

This is a strong H2 signal.

It shows that the marginal effect of F4 collapses once F1 is already applied.

In other words:

```text
F1 already implicitly selects for protein-coding genes.
```

The interaction term:

```text
β_F1·F4
```

should be large, because F4 behaves very differently depending on whether F1 has already been applied.

---

# 4. F1 and F2 Partially Overlap, but Each Contributes Uniquely

F1 and F2 are not redundant.

| Filter Cell | Surviving Pairs |
|---|---:|
| F1 alone | 39,833 |
| F2 alone | 179,751 |
| F1 ∧ F2 | 20,139 |

---

## Marginal Effects

From F1 to F1 ∧ F2:

```text
39,833 → 20,139
```

This removes:

```text
19,694 pairs
```

or about:

```text
49% of F1 survivors
```

So F2 substantially prunes the F1 survivor set.

From F2 to F1 ∧ F2:

```text
179,751 → 20,139
```

This removes:

```text
159,612 pairs
```

or about:

```text
89% of F2 survivors
```

So F1 strongly prunes the F2 survivor set.

---

## Interpretation

F1 and F2 capture different aspects of evidence.

F1 captures:

```text
strong overall evidence
```

including some single-source curated entries.

F2 captures:

```text
broad evidence support
```

including associations with multiple moderate sources.

The intersection contains target–disease pairs where both criteria align:

```text
strong evidence + broad evidence support
```

---

## H2 Interpretation

Stacked F1 and F2 do not behave as fully independent filters, and they do not behave as fully redundant filters either.

A simple independence expectation would predict approximately:

```text
~1,588 surviving pairs
```

A fully redundant interpretation would predict something closer to:

```text
~39,833 surviving pairs
```

The observed value is:

```text
20,139 surviving pairs
```

This sits between those extremes.

That places F1 and F2 in the interaction-effect regime:

```text
partially overlapping, partially distinct, and jointly more selective than either filter alone
```

---

# 5. Constraint Coverage Stays High Throughout

Constraint coverage remains high across all factorial cells.

Across cells, `pct_with_constraint` stays around:

```text
95%–97%
```

This is important for H3.

It means the H3 structural baseline is feasible because the analysis does not lose too much constraint information after filtering.

In other words:

```text
H3 regression will not be bottlenecked by missing constraint covariates.
```

This supports using constraint measures, especially LOF constraint, as a structural covariate in the H3 model.

---

# Summary of Main Findings

| Finding | Interpretation |
|---|---|
| H1 is strongly supported | Filters retain genes with higher publication attention. |
| Mean attention rises monotonically | More filtering produces more attention-enriched survivor sets. |
| Variance in attention declines | Filters homogenize the survivor set around well-studied genes. |
| F3 has near-zero effect | The graph is already mostly connected. |
| F4 matters alone but little after F1 | F1 implicitly selects protein-coding genes. |
| F1 and F2 are partially overlapping | They capture different evidence dimensions. |
| Constraint coverage remains high | H3 regression is feasible. |

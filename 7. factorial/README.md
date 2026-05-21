# Pre-Factorial Sanity Check

Before running the full 16-cell factorial analysis, we first verify that each filter gives sensible counts when applied individually.

This step helps catch issues such as:

- off-by-one threshold bugs
- column-name typos
- incorrect filter logic
- unexpected missingness
- join-related row inflation

Source script:

```text
prefactorial_sanity_check.py
```

---

## Individual Filter Counts

| Filter | Surviving Target–Disease Pairs | Percent of Total |
|---|---:|---:|
| Total target–disease pairs | 4,508,002 | 100.0% |
| F1 alone: score `≥ 0.5` | 39,833 | 0.88% |
| F2 alone: `n_sources ≥ 2` | 179,751 | 3.99% |
| F4 alone: protein-coding | 4,389,628 | 97.4% |

---

## Protein-Coding Restricted Counts

| Metric | Count | Interpretation |
|---|---:|---|
| Target–disease pairs restricted to protein-coding targets | 4,389,628 | protein-coding subset |
| F1 within protein-coding | 39,722 | 99.7% of all F1 survivors |
| F2 within protein-coding | 178,791 | 99.5% of all F2 survivors |

Protein-coding target coverage:

```text
19,596 / 31,275 targets
```

---

# The 16-Cell Factorial

## Conceptual Structure

The factorial analysis evaluates every binary combination of the four filters:

```text
F1, F2, F3, F4
```

Since each filter can be either applied or not applied, the design has:

```text
2⁴ = 16 cells
```

For each of the 16 filter combinations, we apply the corresponding filters to the canonical table and record summary metrics.

---

## Filter Application Logic

Cells without F3 are simple table filters.

These can be implemented as standard `WHERE`-clause filters, such as:

```text
overall_score ≥ 0.5
n_sources ≥ 2
biotype = "protein_coding"
```

Cells with F3 require graph construction.

For these cells, we first apply the relevant non-F3 filters, then construct the surviving bipartite target–disease graph and compute its largest connected component.

This is slower than simple table filtering, but still tractable.

---

## Per-Cell Metrics to Record

For each factorial cell, record the following metrics:

| Metric | Description |
|---|---|
| `n_pairs` | number of surviving target–disease pairs |
| `n_targets` | number of distinct surviving targets |
| `n_diseases` | number of distinct surviving diseases |
| `mean_log_pubs` | mean `log(n_publications + 1)` among surviving targets |
| `var_log_pubs` | variance of `log(n_publications + 1)` among surviving targets |
| `pct_protein_coding` | percent of surviving targets that are protein-coding |
| `pct_with_constraint` | percent of surviving targets with gnomAD constraint coverage |

---

## H1 Signal

The main attention-related quantity from the factorial output is:

```text
mean_log_pubs
```

This measures whether each filter combination retains genes with higher prior publication attention.

Attention is defined as:

```text
log(n_publications + 1)
```

where:

- `n_publications` is the number of PubMed publications linked to a gene.
- `+1` allows genes with zero publications to remain in the analysis.
- `log` compresses the highly skewed publication-count distribution.

---

## Factorial Source and Output

Source script:

```text
factorial.py
```

Output file:

```text
factorial_main.csv
```

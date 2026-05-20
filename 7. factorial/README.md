## Pre-factorial sanity check. 

Before running 16 cells, verify that applying each filter individually gives sensible counts. 
This catches off-by-one threshold bugs and column-name typos, before they propagate across 16 cells.
source: prefactorial_sanity_check.py

Total target-disease pairs:         4,508,002   (100.0%)
F1 alone (score ≥ 0.5):                39,833    (0.88%)
F2 alone (n_sources ≥ 2):             179,751    (3.99%)
F4 alone (protein-coding):          4,389,628   (97.4%)

Restricted to protein-coding:       4,389,628
  F1 within PC:                        39,722    (99.7% of all F1 survivors)
  F2 within PC:                       178,791    (99.5% of all F2 survivors)
PC targets total:                       19,596 / 31,275

# The 16-cell factorial
Conceptual structure.
For each of 16 binary combinations of (F1, F2, F3, F4), we apply the corresponding filters to the canonical table and record per-cell metrics. Cells without F3 are pure WHERE-clause filters. Cells with F3 require computing the largest connected component of the surviving bipartite graph — slower, but still tractable. 

**Per-cell metrics to record:**
1. n_pairs: surviving target-disease pairs
2. n_targets: distinct surviving targets
3. n_diseases: distinct surviving diseases
4. mean_log_pubs: mean log(n_publications + 1) among surviving targets (the H1 signal)
5. var_log_pubs: variance of the above
6. pct_protein_coding: biotype composition (sanity)
7. pct_with_constraint: gnomAD coverage among survivors

Factorial source code: factorial.py and output: factorial_main.csv

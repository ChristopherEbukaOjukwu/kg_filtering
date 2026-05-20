# Pre-factorial sanity check. 

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

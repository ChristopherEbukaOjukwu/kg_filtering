## What the factorial shows
1. H1 (attention bias) is supported, decisively.
mean_log_pubs rises monotonically as filters are added, exactly as predicted.
No filters (baseline):       2.59  log(pubs+1)   ≈ 13 publications per gene
F4 alone:                    3.76                ≈ 43 publications
F2 alone:                    4.12                ≈ 61 publications
F1 alone:                    4.41                ≈ 82 publications
F1 ∧ F2:                     4.63                ≈ 102 publications
F1 ∧ F2 ∧ F3 ∧ F4:           4.75                ≈ 116 publications
Every filter individually raises the mean attention level among survivors. The fully-filtered cell has ~9× more publications per surviving gene than the unfiltered baseline. H1 is supported with a substantially larger effect size than your preregistered ≥0.5 log-unit threshold — the gap between baseline and any single-filter cell exceeds 1 log-unit.
The variance of log-pubs also drops monotonically (3.77 → 1.07), meaning filters don't just shift the mean attention — they homogenize the surviving gene population around well-studied genes.
2. F3 (largest connected component) is doing almost nothing.
Look closely:
Without F3:    4,508,002 pairs
With F3:       4,508,001 pairs   (lost 1 pair)
The unfiltered graph is already essentially one connected component. There is no peripheral structure to remove. F3 only starts mattering after F1 or F2 carve the graph up enough to expose isolated subgraphs. Even then, F3 only removes a few thousand pairs at most.
This is a genuine finding for your chapter, but it changes the H2 story. F3 will contribute almost nothing to the interaction effects. The non-linear compounding story is going to live in F1 × F2 (and to a lesser extent F1 × F4 and F2 × F4), not in anything involving F3.
This is also somewhat embarrassing for the chapter outline's framing of F3 as a co-equal filter — it really isn't in this data. You have two options when you write up: (a) keep F3 in the factorial and report its near-null effect as a finding (honest, methodologically clean), or (b) reframe F3 as a structural filter whose role is to verify the absence of peripheral fragmentation rather than to actively prune. Option (a) is cleaner.
3. F4 (protein-coding) is also doing very little once other filters are on.
No filters:                  31,275 targets total, 19,596 protein-coding (62.7%)
F1 alone:                     8,233 targets, 8,142 protein-coding (98.9%)
F1 ∧ F2:                      5,815 targets, 5,792 protein-coding (99.6%)
F1 by itself almost completely implicit-selects for protein-coding genes. F4 adds only marginal additional filtering after F1 or F2 is on. The percentage of protein-coding survivors in F1-alone is 99.7% — applying F4 on top removes 91 targets out of 8,142.
This is your strongest H2 signal in absolute terms: F4's marginal effect collapses dramatically once F1 is applied. That's the non-linear compounding pattern in its starkest form — a filter that does substantial work alone (removing 11,679 of 31,275 targets) does almost no work on top of F1 (removing 91 of 8,142). The interaction term β_{F1·F4} will be large and negative.
4. F1 and F2 are partially overlapping but each contributes uniquely.
F1 alone keeps 39,833 pairs.
F2 alone keeps 179,751 pairs.
F1 ∧ F2 keeps 20,139 pairs.
From F1 to F1 ∧ F2: we lose 19,694 pairs (49% reduction). F2 substantially prunes the F1 survivors.
From F2 to F1 ∧ F2: we lose 159,612 pairs (89% reduction). F1 brutally prunes the F2 survivors.
The two filters are not redundant. F1 catches "strong evidence" cases that F2 misses (single-source curated entries), and F2 catches "broad evidence" cases that F1 misses (multi-source moderate scores). The intersection is where both criteria align.
This is the cleanest H2 story you'll get: stacked, F1 and F2 don't act independently (which would predict ~1,588 surviving pairs) and they don't act collinearly (which would predict ~39,833 surviving pairs). The actual 20,139 sits halfway between — exactly the "interaction effect" regime.
5. Constraint coverage stays high throughout.
pct_with_constraint stays in the 95-97% range across all cells. This means H3's structural baseline will work — you're not running out of measurable constraint data even in the smallest cells. The H3 regression won't be bottlenecked by missing covariates.

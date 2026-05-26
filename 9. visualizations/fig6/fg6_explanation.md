# What the Heatmap Shows

```
Filters do not change the top-ranked genes much, but they change the middle and lower-ranked genes a lot.
```

The three panels show pairwise agreement between all 16 factorial filter combinations.

Each panel uses the same 16 filter combinations on both axes.

The row and column order is shared across panels, so the same cell pair can be compared across the top, middle, and lower ranking tiers.

The ordering is based on hierarchical clustering from the middle-tier similarity matrix.

---

# Reading the Panels

## Top Tier: Ranks 1–100

The top-tier panel is almost uniformly deep red.

This means that the top 100 genes ranked by maximum Open Targets overall association score are nearly identical across all 16 filter combinations.

In simple terms:

```text
The headline genes are filter-invariant.
```

A few cells are slightly less saturated, especially those involving:

```text
F1 = 1 ∧ F3 = 1
```

But even there, the Jaccard overlap remains high:

```text
Jaccard > ~0.7
```

So the top-ranked genes are very stable.

---

## Middle Tier: Ranks 101–1000

The middle-tier panel shows more divergence.

The main red block still indicates strong agreement among many filter combinations.

However, the cells where both F1 and F3 are applied show lower overlap with the rest of the matrix.

These appear as an orange-yellow band on the right side of the heatmap.

For these cells, Jaccard overlap drops to approximately:

```text
0.55–0.70
```

This means the middle-ranked gene set is starting to depend more strongly on which filters are applied.

The F1 = 1 ∧ F3 = 1 cells also differ modestly from each other depending on F2 status.

In simple terms:

```text
The middle of the ranking is less stable than the top.
```

---

## Lower Tier: Ranks 1001–3000

The lower-tier panel shows the strongest divergence.

The cells involving:

```text
F1 = 1 ∧ F2 = 1 ∧ F3 = 1
```

drop to deep blue against the unfiltered or lightly filtered cells.

In some places, the Jaccard overlap falls below:

```text
0.3
```

This means that the lower-ranked gene lists share less than 30% of their genes across some filter combinations.

Even within the broader “everything else” block, agreement is no longer perfect.

Cells with:

```text
F1 = 1 ∧ F3 = 1 ∧ F2 = 0
```

show only around:

```text
0.5
```

overlap with the rest.

In simple terms:

```text
At the lower part of the ranking, filter choice strongly determines which genes appear.
```

---

# What the Gradient Means

The three panels together make one central argument:

```text
Filters agree about the obvious top genes,
but they disagree increasingly as we move down the ranking.
```

The top 100 genes are robust across filters.

The middle and lower tiers are contested.

This matters because the chapter’s H3 finding sits mostly in these middle and lower tiers.

The under-survivor population is large:

```text
4,004 genes
22.5% of protein-coding targets
```

These are not usually the top 100 genes.

They are the genes whose presence in the filtered knowledge graph depends on which filters are applied.

---

# Main Interpretation

## 1. The Top Genes Are Stable

The top-ranked genes are largely the same across filter combinations.

These are probably the strongest, most canonical, highest-scoring genes.

Filter choice does not meaningfully change the top of the ranking.

---

## 2. The Middle and Lower Tiers Are Filter-Sensitive

The main effect of filtering appears in the larger middle and lower sections of the ranking.

These are the genes whose inclusion depends on the specific filter stack.

So the chapter’s claim is not:

```text
filters completely change the headline genes
```

Instead, the claim is:

```text
filters reshape the much larger set of genes below the obvious top-ranked group
```

---

## 3. F1 and F3 Drive Most Ranking Divergence

Two filters matter most for divergence:

```text
F1
F3
```

F1 alone is selective, but it does not completely restructure rankings.

F3 alone removes almost nothing from the unfiltered graph.

However, when F1 and F3 are combined, the graph is carved in a way that exposes peripheral structure to largest-connected-component pruning.

This changes the ranked list most strongly in the middle and lower tiers.

---

## 4. F2 Adds Divergence in the Lower Tier

F2 contributes most when combined with F1 and F3.

The deepest blue cells are all associated with:

```text
F1 = 1 ∧ F2 = 1 ∧ F3 = 1
```

This means the strict evidence filters plus graph-structure filtering jointly alter the lower-ranked gene set.

---

## 5. F4 Adds Little

F4 does not meaningfully affect ranking divergence.

Cells that differ only by F4 are almost identical across all three tiers.

This confirms the earlier redundancy result:

```text
By the time other filters are applied, the retained genes are already overwhelmingly protein-coding.
```

---

# Core Takeaway

The heatmap shows that:

```text
Filter choice barely affects the top-ranked genes,
but strongly affects the middle and lower-ranked genes.
```

This supports the chapter’s larger argument.

The concern is not that filters change the obvious top 100 genes.

The concern is that filters determine which genes remain visible in the much larger middle and lower portions of the gene ranking.

That is where under-survivors and filter-sensitive genes appear.

---

# Caption

**Figure 6. Filter agreement on score-ranked target lists decays from top to bottom of the ranking.**  
Pairwise Jaccard overlap of target lists between all 16 factorial filter combinations, computed at three rank tiers within each cell’s score-ranked target set. Targets are ranked by their maximum overall association score across all surviving associations within the cell. Left panel: top tier, ranks 1–100. Middle panel: middle tier, ranks 101–1000. Right panel: lower tier, ranks 1001–3000. All three panels share the same row and column ordering, based on hierarchical clustering of the middle-tier matrix using average linkage, and the same colormap, with Jaccard values ranging from 0 to 1. In the top tier, all filter combinations produce nearly identical headline gene lists, with median Jaccard overlap greater than 0.9. Only cells combining F1 and F3 show modest divergence. In the middle tier, the F1 ∧ F3 combination produces target lists that differ substantially from non-F3 cells, with Jaccard overlap around 0.55–0.70. In the lower tier, divergence becomes severe: F1 ∧ F2 ∧ F3 cells share less than 30% of their rank-1001–3000 targets with cells lacking one or more of these filters. F4, the protein-coding restriction, shows no meaningful effect on ranking divergence at any tier. The decay of filter agreement from top to bottom confirms that the chapter’s H3 finding operates not at the very top of the score-ranked list, but in the larger middle and lower tiers where the under-survivor population resides.

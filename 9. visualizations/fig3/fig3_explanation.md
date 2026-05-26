# What the Figure Shows

The chart shows seven filter conditions applied to the same canonical analysis table of:

```text
4,508,002 target–disease pairs
```

Each horizontal bar represents one filter condition.

The bar length shows:

```text
number of surviving target–disease pairs
```

on a log-scaled x-axis.

The bar color shows:

```text
mean log(publications + 1)
```

of the surviving targets.

---

## Reading the Figure from Top to Bottom

### 1. Unfiltered Baseline

The full canonical table contains:

```text
4.51 million target–disease pairs
31,275 distinct targets
```

The mean attention of the underlying gene population is:

```text
log(pubs + 1) = 3.26
```

This corresponds to approximately:

```text
~25 publications per gene
```

on average.

The light yellow color anchors the colorbar at its lowest value.

This is the reference population against which all filter behavior is compared.

---

### 2. Individual Filters

The next rows show the individual filters applied alone.

F3 alone is omitted from the figure because it removes only one pair in the absence of other filters.

---

#### F1: Overall Association Score Threshold

```text
F1 = overall_score ≥ 0.5
```

F1 is the most aggressive individual filter.

It retains:

```text
39.8k pairs
```

which is approximately:

```text
0.9% of the full table
```

The mean attention rises sharply to:

```text
log(pubs + 1) = 4.41
```

This corresponds to approximately:

```text
~82 publications per surviving gene
```

---

#### F2: Multi-Source Evidence Requirement

```text
F2 = ≥ 2 sources
```

F2 retains:

```text
179.8k pairs
```

which is approximately:

```text
4% of the full table
```

The mean attention rises to:

```text
log(pubs + 1) = 4.14
```

---

#### F4: Protein-Coding Restriction

```text
F4 = biotype = protein_coding
```

F4 retains:

```text
4.39 million pairs
```

which is approximately:

```text
97% of the full table
```

Even though F4 removes relatively few target–disease pairs, it still raises mean attention to:

```text
log(pubs + 1) = 3.80
```

This is one of the clearest results in the chapter.

A protein-coding filter is not only a biotype filter. It also behaves like an implicit attention filter.

The excluded gene population, including many non-coding RNAs and pseudogenes, has roughly an order of magnitude less curated publication attention than the protein-coding portion.

---

# Stacked Filters

The stacked filter rows show how successive filtering layers narrow the surviving pair set.

---

## F1 ∧ F2

```text
F1 ∧ F2
```

retains:

```text
20.1k pairs
```

The mean attention reaches:

```text
log(pubs + 1) = 4.63
```

---

## F1 ∧ F2 ∧ F4

```text
F1 ∧ F2 ∧ F4
```

retains approximately the same number of pairs as F1 ∧ F2:

```text
~20.1k pairs
```

The mean attention also remains approximately the same.

This is the F4-redundancy result.

By the time F1 and F2 are applied, the surviving target–disease pairs are already essentially all protein-coding.

Therefore, F4 adds little or nothing after F1 and F2.

---

## F1 ∧ F2 ∧ F4 ∧ F3

```text
F1 ∧ F2 ∧ F4 ∧ F3
```

retains:

```text
17.8k pairs
```

This is a small additional reduction caused by the largest connected component restriction.

---

# Visual Evidence for H1

Three concurrent trends carry the H1 finding visually.

## 1. Bar Length Shrinks

The number of surviving pairs falls from:

```text
4.51 million
```

to:

```text
17.8k
```

This is a reduction of more than two orders of magnitude.

---

## 2. Color Saturates

The color shifts from pale yellow at the unfiltered baseline to deep blue in the stacked condition.

The colormap intentionally tracks the attention gradient.

As filtering becomes more restrictive, surviving targets become more publication-attended.

---

## 3. Mean Attention Increases

The annotated mean attention rises from:

```text
3.26
```

in the unfiltered baseline to:

```text
4.63
```

in the stacked condition.

This corresponds to roughly a:

```text
~4× increase
```

in mean publications per surviving gene.

---

# Summary of the Visual Pattern

All three visual trends tell the same story:

```text
Filters concentrate the graph into a progressively smaller,
progressively higher-attention subset of the gene population.
```

---

# Where the F1-vs-F2 Pattern Appears

A useful detail in the figure is the difference between F1 and F2.

F1 retains fewer pairs than F2:

```text
F1: 39.8k pairs
F2: 179.8k pairs
```

But F1 survivors have higher mean attention:

```text
F1: log(pubs + 1) = 4.41
F2: log(pubs + 1) = 4.14
```

This is not a contradiction.

It reflects the Open Targets scoring structure.

F1 requires a high overall association score.

That score can be achieved through:

- one strongly anchored evidence source;
- multiple corroborating moderate evidence sources;
- focused disease-specific evidence.

F2 requires multiple sources, but it can still admit target–disease pairs with moderate per-source scores.

Therefore, F2 allows a broader population through, while F1 is more selective for higher-attention target–disease pairs.

In simple terms:

```text
F1 is stricter in attention selectivity,
even though F2 is a multi-source filter.
```

This is a useful point to unpack in the chapter prose.

---

# Caption

**Figure 3. Filter survival cascade and per-filter attention-associated retention (H1).**  
Horizontal bar chart showing the number of surviving target–disease pairs under seven filter conditions applied to the unfiltered canonical analysis table of 4,508,002 pairs. The x-axis is log-scaled. Bar color encodes the mean `log(publications + 1)` of surviving targets, with publication counts derived from NCBI `gene2pubmed` and mapped to Ensembl identifiers via `gene2ensembl`. Each bar is annotated with the surviving pair count and mean log-publication value. Filters: F1 = overall association score ≥ 0.5; F2 = ≥ 2 distinct data sources; F3 = restriction to the largest connected component of the bipartite target–disease graph; F4 = `biotype = protein_coding`. F3 alone is not shown because it removes only one pair in the absence of other filters. All filters individually retain higher-attention targets than the unfiltered baseline, supporting H1. Stacking filters further concentrates survivors toward the well-studied gene population, with the fully stacked F1 ∧ F2 ∧ F3 ∧ F4 cell retaining 17,823 pairs whose underlying gene population has approximately four times higher mean publication count than the unfiltered baseline.

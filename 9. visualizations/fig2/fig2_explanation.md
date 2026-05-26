# What the Figure Shows

The main panel plots the distribution of **gene degree** across the Open Targets gene-disease graph.

Here, gene degree means:

```text
the number of distinct diseases each gene is associated with in Open Targets
```

The plot includes approximately:

```text
~31,000 genes
```

Both axes are log-scaled so the full range is visible, from genes associated with only one disease to genes associated with thousands of diseases.

---

## Reading the Main Panel

### 1. Sparsely Attested Genes

The leftmost column is the tallest.

It contains approximately:

```text
~4,000 genes
```

that are associated with exactly one disease.

The next two columns, corresponding to degree 2 and degree 3, are nearly as tall.

Together, these first few columns represent the **sparsely attested mode**.

These are genes whose presence in Open Targets is supported by very limited disease-association evidence.

In many cases, this may reflect:

- one disease association
- one or two thin evidence links
- literature-mined mentions
- limited source support

---

### 2. Empirical Scarcity at Intermediate Degree

From approximately:

```text
degree ~5 to ~20
```

the distribution drops into a visible valley.

This region is labeled:

```text
empirical scarcity
```

Genes with this intermediate level of disease coverage are unexpectedly rare.

The figure alone cannot determine whether this gap reflects:

- real biological structure
- database construction
- evidence aggregation behavior
- measurement artifact
- curation practices

However, the gap is structurally present in the Open Targets graph.

In other words:

```text
genes with intermediate disease degree are systematically under-represented relative to what a smooth distribution would suggest
```

---

### 3. Well-Studied Mode

From approximately:

```text
degree ~30 to ~500
```

a second hill appears.

This hill peaks around:

```text
degree ~100 to ~200
```

This is the **well-studied mode**.

These are genes connected to hundreds of diseases.

They include canonical biomedical research workhorses such as:

```text
TP53
AKT1
TNF
IL6
```

These genes are often:

- master regulators
- signaling intermediates
- cytokines
- immune genes
- pleiotropic biological hubs
- heavily studied biomedical targets

---

### 4. Extreme High-Degree Tail

Past approximately:

```text
degree ~1000
```

the distribution falls sharply.

This means that very few genes are connected to literally thousands of diseases.

These are extreme outliers in the Open Targets gene–disease graph.

---

# Disease Distribution Inset

The inset in the upper right shows the same degree-distribution analysis from the disease side.

Instead of asking:

```text
How many diseases is each gene associated with?
```

it asks:

```text
How many genes is each disease associated with?
```

The disease-side distribution looks different.

It follows a smoother, monotonically decreasing heavy-tailed pattern.

Most diseases have only a few gene associations, while some diseases have many.

Importantly:

```text
there is no clear second mode
```

and no comparable valley.

---

## Key Contrast

The contrast between the main panel and the inset is the main point.

The disease distribution is smooth.

The gene distribution is bimodal.

This suggests that the bimodality is not simply a generic property of the bipartite graph.

Instead, it is specifically a property of how genes accumulate disease associations in Open Targets.

In simple terms:

```text
The bimodality is a gene-side phenomenon, not a disease-side phenomenon.
```

---

# Why This Figure Motivates the Chapter

Filters in gene–disease knowledge graphs are often discussed as if they operate on a uniform population.

For example:

```text
a filter removes weak evidence
```

or:

```text
a filter retains high-quality associations
```

But this figure shows that the population is not uniform.

Instead, the gene population is structurally bimodal.

There are two qualitatively different gene populations:

1. sparsely attested genes with very few disease associations;
2. well-studied genes connected to many diseases.

These two groups are separated by a region of empirical scarcity.

---

## Why This Matters for Filtering

Filter behavior may differ depending on which mode a gene belongs to.

A filter that mostly removes sparsely attested genes is operating on one kind of structure:

```text
thin evidence
single-source support
limited disease coverage
```

A filter that removes well-studied genes is operating on another kind of structure:

```text
broad disease coverage
pleiotropic associations
diffuse evidence
many disease contexts
```

Therefore, filter effects cannot be understood only as “weak evidence removed” or “strong evidence retained.”

The effect depends on where genes sit in the underlying degree structure of the graph.

---

# Chapter Motivation

The chapter’s central question is:

```text
How do common filters interact with the structure of the gene population,
and which genes do they jointly exclude?
```

This question is meaningful because the gene population already has structure before filtering begins.

The figure establishes that structure.

It shows that Open Targets gene–disease associations are not distributed smoothly across genes.

Instead, genes cluster into distinct regimes of disease connectivity.

This motivates the chapter’s analysis of whether filtering:

- reinforces the well-studied mode;
- removes sparsely attested genes;
- excludes some highly connected pleiotropic genes;
- or compounds these effects when filters are stacked.

---

## Caption
**Figure 2. The gene-side degree distribution is bimodal, while the disease-side distribution is unimodal.** 
Main panel: distribution of gene degree (number of distinct diseases each gene is associated with) across 
all 31,275 genes in Open Targets, on log-log axes (30 logarithmically-spaced bins). The gene population is bimodal, 
with a sparsely-attested mode at degree 1-3 (left, ~7,000 genes with one or two disease associations), an empirical 
scarcity region at degree 5-20, and a well-studied mode peaking at degree 100-200 (~1,300 genes per bin near the peak). 
Vertical dashed lines mark the approximate location of each mode. Inset: distribution of disease degree (number of distinct 
genes each disease is associated with) across 26,288 diseases. The disease distribution is monotonically decreasing with 
a heavy right tail and shows no comparable bimodality. The bimodality of the gene distribution is the structural feature 
that motivates the chapter's central question: filter effects depend on which mode of the gene population a filter targets.

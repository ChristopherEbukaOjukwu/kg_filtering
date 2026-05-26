# What the Figure Shows

The figure plots all:

```text
17,793 protein-coding genes
```

that have both Open Targets disease-association data and an NCBI publication count.

The panel combines three pieces of information:

1. research attention;
2. filter survival;
3. residual status relative to the H3 baseline model.

---

## X-Axis: Research Attention

The x-axis shows research attention, measured as:

```text
log(publications + 1)
```

Publication counts are derived from NCBI `gene2pubmed`.

Genes on the left have only one or two papers.

Genes on the right have several thousand papers.

---

## Y-Axis: Filter Survival

The y-axis shows the binary survival outcome under the stacked filter:

```text
F1 ∧ F2 ∧ F4
```

where:

```text
F1 = overall association score ≥ 0.5
F2 = ≥ 2 data sources
F4 = biotype = protein_coding
```

A gene at:

```text
y = 1
```

has at least one disease association that passes all three filters.

A gene at:

```text
y = 0
```

has no disease association that passes all three filters.

Small vertical jitter is added so that the thousands of genes at each outcome value appear as visible stripes instead of overlapping on a single line.

---

## Black Curve: Predicted Survival Probability

The black curve shows the model’s predicted probability of survival as a function of:

```text
log(publications + 1)
```

while holding structural covariates at typical values.

The structural covariates include:

```text
constraint bin
PPI degree
chromosome
```

This is the H3 baseline model.

The curve has the expected logistic S-shape:

- near zero at the low-publication end;
- rising through moderate publication counts;
- approaching one at the high-attention extreme.

In simple terms:

```text
genes with very few publications are predicted to rarely survive,
while highly published genes are predicted to survive more often.
```

---

## Point Colors: Residuals

Point color encodes the residual from the structural baseline model.

Residual is defined as:

```text
actual survival - predicted survival probability
```

| Color | Residual Pattern | Meaning |
|---|---|---|
| Red | residual < -0.3 | under-survivors |
| Blue | residual > +0.3 | over-survivors |
| Gray | residual between -0.3 and +0.3 | neutral cases |

---

# Reading the Figure

## Lower-Right: Under-Survivors

The lower-right red cluster contains the under-survivor genes.

There are:

```text
4,004 under-survivor genes
```

representing:

```text
22.5% of the protein-coding population
```

These genes have moderate-to-high publication counts:

```text
log_pubs ≈ 3.5 to 9
```

but their survival outcome is:

```text
0
```

The model predicts that many of these genes should survive based on their publication attention, but they do not.

The labeled examples are:

```text
HIF1A
IFNG
MDM2
```

These genes each have thousands of associated publications and high predicted probabilities of surviving the filters.

However, none has a disease association that crosses both F1 and F2.

This is the key H3 under-survival pattern.

---

## Upper-Left: Over-Survivors

The upper-left blue cluster contains the over-survivor genes.

There are:

```text
4,825 over-survivor genes
```

representing:

```text
27.1% of the protein-coding population
```

These genes have low publication counts:

```text
log_pubs ≈ 1 to 5
```

but their survival outcome is:

```text
1
```

The model predicts that many of these genes should not survive based on their low publication attention, but they do.

The labeled examples are:

```text
OR10R2
GRXCR2
PRCD
```

These genes each have very few publications but still pass F1 ∧ F2 ∧ F4.

Mechanistically, this can happen when a gene has a focused, high-confidence curated disease association.

For example, one strong curated source, such as ClinGen or OMIM, can push a gene over the evidence thresholds even when broader research attention is minimal.

---

## Gray Points: Neutral Majority

The gray points represent genes whose observed survival status roughly matches the baseline model prediction.

These are genes where:

```text
actual survival ≈ predicted survival
```

The gray points fade into the background so the reader’s attention is drawn to the red and blue residual regions, where the H3 result is most visible.

---

# What the Figure Argues

The chapter’s central claim is that filters do not simply select for well-studied genes.

Instead, filters select for genes whose evidence has crystallized into:

```text
focused
source-diverse
disease-specific anchors
```

The lower-right red cluster makes this visible.

If filters were simply a clean proxy for research attention, the lower-right red region would be mostly empty.

Highly published genes would almost always survive.

But many highly published genes do not survive.

These include:

- master regulators;
- cytokines;
- MHC molecules;
- oncogenes;
- pleiotropic biological hubs.

Their evidence is often broad rather than focused.

They appear in thousands of papers across many disease contexts, but each disease-specific association may contribute only modest evidence or evidence concentrated in limited source types.

The harmonic-sum scoring and multi-source filters reward concentrated disease-specific evidence.

Broadly relevant biological hubs may lack that concentration.

---

# Mirror-Image Pattern

The upper-left blue cluster shows the opposite pattern.

Some minimally studied genes survive because their evidence is concentrated in a focused, high-confidence disease association.

Examples:

```text
OR10R2
GRXCR2
PRCD
```

These genes may have very few publications, but their limited evidence is sharp, curated, and disease-specific.

This means they can pass F1 ∧ F2 even without broad publication attention.

---

# Core Interpretation

The figure supports H3 both numerically and mechanistically.

Numerically:

```text
22.5% under-survivors
27.1% over-survivors
```

Mechanistically:

```text
under-survivors = highly published, broad/diffuse evidence
over-survivors = low-publication, focused/curated evidence
```

The main takeaway is:

```text
Filters privilege evidence concentration over publication volume.
```

Or, more explicitly:

```text
The filters do not simply retain well-studied genes.
They retain genes whose disease evidence is focused, source-diverse, and curated.
```

---

# Caption

**Figure 5. Filter survival relative to the attention-adjusted baseline (H3).**  
Each point represents one of 17,793 protein-coding genes with available publication counts from NCBI `gene2pubmed` and gnomAD loss-of-function constraint. The x-axis shows `log(publications + 1)` as a measure of research attention. The y-axis shows binary survival in the stacked filter F1 ∧ F2 ∧ F4, where F1 = overall association score ≥ 0.5, F2 = ≥ 2 distinct data sources, and F4 = `biotype = protein_coding`. Small vertical jitter is added for visibility. The black curve shows the predicted probability of survival from a logistic regression baseline that combines attention, constraint, PPI degree, and chromosome, with full-model AUC = 0.77. Points are colored by residual: red points are under-survivors, defined as residual < -0.3; blue points are over-survivors, defined as residual > +0.3; and gray points are neutral. Under-survivors include 4,004 genes, or 22.5% of the population; over-survivors include 4,825 genes, or 27.1%; neutral genes include 8,964 genes. Three under-survivors representing distinct biological domains are labeled: **HIF1A**, a master hypoxia regulator; **IFNG**, a cytokine involved in immune signaling; and **MDM2**, a p53 regulator in oncology. Three over-survivors representing the mirror-image mechanism are labeled: **OR10R2**, an olfactory receptor with minimal research attention; **GRXCR2**, a hearing-loss gene with focused curated evidence; and **PRCD**, a rare-disease gene with high-confidence curated evidence. The under-survivor population concentrates in the lower-right region, showing high attention but no filter survival. This pattern is inconsistent with the simple claim that filters retain well-studied genes. Instead, filters retain genes whose evidence has consolidated into focused, source-diverse disease anchors, while broadly studied pleiotropic hub genes may lack this concentration despite large cumulative publication records.

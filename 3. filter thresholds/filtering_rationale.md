# Rationale for Filtering Decisions

This section documents the rationale behind the filtering choices used to construct and compare filtered versions of the Open Targets gene–disease graph.

The goal is not to define one “correct” filter, but to test whether common filtering decisions systematically change which genes remain eligible for downstream analysis.

---

## F1: Overall Association Score Threshold

**Filter definition:**  
Retain target–disease associations whose Open Targets overall association score is greater than or equal to a chosen threshold.

The Open Targets overall association score summarizes the evidence supporting a target–disease association across data sources. Open Targets notes that deciding what constitutes a “strong” association is open to interpretation, because association scores are heuristic summaries of available evidence rather than direct measures of biological truth. Because there is no single universally accepted threshold, this analysis uses multiple thresholds rather than relying on one cutoff. This choice is also consistent with the design of disease-specific knowledge graph workflows such as KGG, where users can inspect the Open Targets association score distribution and choose a desired score threshold.

**Rationale sources:**
- [Open Targets Platform documentation: Target–disease association scores](https://platform-docs.opentargets.org/associations)
- [Karki et al., 2025. *KGG: a fully automated workflow for creating disease-specific knowledge graphs*. Bioinformatics.](https://doi.org/10.1093/bioinformatics/btaf383)

### Thresholds Used

Three F1 thresholds are used:

| Threshold | Interpretation | Rationale |
|---:|---|---|
| `≥ 0.2` | Permissive | Used in the AstraZeneca Mantis-ML 2.0 paper for selecting Open Targets seed genes. |
| `≥ 0.5` | Default / middle | A moderate cutoff used as a middle point between permissive and stringent filtering. |
| `≥ 0.8` | Stringent | A high-confidence cutoff that retains only strong Open Targets associations. |

**Additional rationale source for `0.2`:**
- [AstraZeneca Mantis-ML 2.0](https://www.science.org/doi/10.1126/sciadv.adj1424)
- [Middleton et al., 2024. *Phenome-wide identification of therapeutic genetic targets, leveraging knowledge graphs, graph neural networks, and UK Biobank data*. Science Advances.](https://www.science.org/doi/10.1126/sciadv.adj1424)

The non-linearity hypothesis (H2) should be evaluated across all three thresholds. In other words, if stacked filters create a narrower or more canonical surviving gene set than expected, that pattern should not depend entirely on one arbitrary score cutoff.

---

## F2: Multi-Source Threshold

**Filter definition:**  
Retain target–disease associations supported by at least `N` independent evidence sources or evidence types. The rationale is that associations supported by multiple evidence streams are usually treated as more reliable than associations supported by only one source.

This follows the broader logic of evidence-based gene-disease curation frameworks, especially the ClinGen gene-disease validity framework, which evaluates gene-disease validity using multiple categories of evidence rather than relying on a single observation.

For this project, the filter operationalizes that idea as a source-count threshold.

**Rationale source:**

- [Strande et al., 2017. *Evaluating the Clinical Validity of Gene-Disease Associations: An Evidence-Based Framework Developed by the Clinical Genome Resource*. American Journal of Human Genetics.](https://doi.org/10.1016/j.ajhg.2017.04.015)

| Setting | Source/Data-Type Requirement |
|---|---|
| Permissive (Default) | `≥ 2` sources |
| Stringent | `≥ 3` sources |

The `≥ 2` rule captures the common intuition of requiring more than one independent line of evidence.
The `≥ 3` rule is used as a stricter version to test whether requiring broader support disproportionately removes lower-attention or less canonical genes.

---

## F3: Largest Connected Component

**Filter definition:**  
After constructing the graph, retain only the largest connected component. No numeric threshold is used. This is a structural graph filter rather than an evidence-score filter. It removes isolated nodes and small disconnected components, keeping the main connected body of the graph.

The rationale is that many graph-based downstream analyses, such as path-based reasoning, network propagation, centrality analysis, and embedding methods, often operate most naturally on the largest connected component.

However, this filter may also introduce bias because genes outside the largest connected component may be systematically less studied, less annotated, or less connected to canonical disease biology.

### Rule Used

```text
Retain nodes and edges in the largest connected component only.
```

**Rationale sources:**

- [Barabási, *Network Science*, Chapter 3](https://networksciencebook.com/chapter/3)
- [NetworkX documentation: `connected_components`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html)
- [Li et al., 2024. *Contextual AI models for single-cell protein biology*. Nature Methods.](https://www.nature.com/articles/s41592-024-02341-3)
---

## F4: Biotype / Type Constraint

**Filter definition:**  
Apply node-type and edge-type constraints to restrict the graph to a more conventional target–disease structure.

### Node Constraint

Retain only protein-coding targets.

```text
biotype == "protein_coding"
```

This focuses the analysis on the target class most commonly used in therapeutic target discovery and gene prioritization.

### Edge Constraint

Retain only gene–disease association edges.

This removes other possible relationship types and keeps the analysis focused on target/gene associations with diseases.

### Stringent Variant

The stringent version additionally restricts evidence to genetic evidence only.

```text
biotype == "protein_coding"
AND data_type == "Genetic association"
```

This tests whether filtering to genetically supported protein-coding targets creates a much narrower and more canonical surviving gene set.

**Relevant source:**

- [Open Targets Platform documentation: Target–disease evidence and data types](https://platform-docs.opentargets.org/evidence)

### F4 biotype / type constraint
1. Node constraint: protein-coding only.
2. Edge constraint: gene association only.

---

# Filter Settings

| Setting | F1: Overall Score | F2: Source/Data-Type Support | F3: Graph Structure | F4: Type Constraint |
|---|---:|---:|---|---|
| Permissive | `≥ 0.2` | `≥ 2` sources | largest connected component | protein-coding |
| Default | `≥ 0.5` | `≥ 2` sources | largest connected component | protein-coding |
| Stringent | `≥ 0.8` | `≥ 3` sources | largest connected component | protein-coding + genetics-only |

---

# Hypothesis Connection

These filters are used to test whether common graph construction and filtering decisions are neutral.

The key hypotheses are:

1. **H1: Filters exhibit attention-associated retention**
   Filters may disproportionately retain genes with higher prior publication attention, even though publication count     is not directly used as a filtering criterion.

   ```
   Given:
   F1: evidence strength threshold
   F2: multi-source support threshold
   F3: largest connected component
   F4: protein-coding / genetics-only constraint

   Question:
   Do these filters indirectly retain the highly published genes?
   ```

2. **H2: Filters exhibit non-linear compounding**  
   Stacked filters may retain a narrower gene set than expected from the individual filters alone.

   ```
   #### Example

   Suppose the unfiltered graph contains 10,000 genes.

   Applied separately:

   | Filter | Genes Retained | Percent Retained |
   |---|---:|---:|
   | No filter | 10,000 | 100% |
   | F1: score ≥ 0.5 | 6,000 | 60% |
   | F2: ≥ 2 sources | 5,500 | 55% |
   | F3: largest connected component | 7,000 | 70% |

   Each filter appears moderately selective.

   If the filters acted independently, the expected retention after stacking them would be approximately:

   Expected retention: 23.1%
   Observed retention: 9%
   
   If OR < ER: The stacked filters are not just reducing the graph size. They are producing a survivor set that is        much smaller and much more publication-enriched than expected.
   ```
   
3. **H3: Structural counterfactual**  
   Some genes may under-survive relative to what would be expected from research attention alone.

### Logic
**H1:** Highly published genes are generally more likely to survive filtering.
**H2:** When filters are stacked, survival filtering favors the most highly published genes.
**H3:**
If H3 is supported:
    Publication attention is not enough.
    Some highly published genes still fail because of the evidence structure,
    source coverage, graph position, or type constraints.

If H3 is not supported:
    Publication attention explains most of survival.
    In other words, once you know how well studied a gene is,
    there is little extra under-survival left to explain.

The main expectation is that the non-linearity hypothesis should hold across the permissive, default, and stringent filter settings.

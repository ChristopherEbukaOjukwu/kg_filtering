# The Canonical Input Table

The canonical analysis table, `analysis.parquet`, is the main row-per-association table used for downstream filtering and hypothesis testing.

Each row represents one:

```text
target–disease pair
```

or, more explicitly:

```text
(targetId, diseaseId)
```

---

## Row-Level Fields

Each row contains the inputs needed for the Chapter 3 filters and the H3 counterfactual analysis.

| Purpose | Field(s) | Source |
|---|---|---|
| Identifiers | `targetId`, `diseaseId` | `association_overall_direct` |
| F1: overall association score | `overall_score` | `association_overall_direct` |
| F2: multi-source support | `n_sources` | `association_by_datasource_direct` |
| F4: main type constraint | `biotype` | Open Targets Target file |
| F4: alternative genetics-only specification | `datatypes` | `association_by_datatype_direct` |
| F3: largest connected component | computed after filtering | graph structure |
| H3 covariates | `n_publications`, `constraint_score`, `ppi_degree`, `chromosome` | external and OT-derived sources |
| Interpretation fields | `approvedSymbol`, `currentNovelty` | Open Targets Target file |

---

# Purpose of the Canonical Analysis Table

The canonical analysis table, `analysis.parquet`, consolidates five separate Open Targets and external data sources into a single row-per-`(target, disease)` table.

Each row contains all inputs needed to:

1. apply the four Chapter 3 filters;
2. run the `2⁴` factorial filter analysis;
3. fit the H3 counterfactual baseline;
4. avoid repeated joins across large files during downstream analysis.

In simple terms:

```text
analysis.parquet = one table containing all filter inputs and modeling covariates
```

---

# Sources Joined into the Canonical Table

The base table is:

```text
association_overall_direct
```

This file contains one row per target–disease pair with the Open Targets overall harmonic-sum association score.

The base table contains:

```text
4,508,002 target–disease pairs
```

Four additional sources are `LEFT JOIN`ed onto this base table.

The `LEFT JOIN` preserves the original target–disease universe from `association_overall_direct`.

---

## 1. `association_by_datasource_direct`

This file contributes the per-pair count of distinct data sources supporting each target–disease association.

Used for:

```text
F2: multi-source support
```

Derived field:

```text
n_sources
```

---

## 2. `association_by_datatype_direct`

This file contributes the per-pair list of distinct data types supporting each target–disease association.

Used for:

```text
F4 alternative specification: genetics-only robustness check
```

Derived field:

```text
datatypes
```

Example use:

```text
retain only associations where datatypes includes genetic association evidence
```

---

## 3. Open Targets Target Dataset

The Open Targets Target file contributes per-gene metadata.

Fields used include:

```text
biotype
chromosome
approvedSymbol
currentNovelty
gnomAD constraint metrics
```

The `biotype` field is used for the main F4 specification:

```text
biotype == "protein_coding"
```

The Target file also contains gnomAD constraint information.

---

## 4. External Research-Attention Data

External research-attention data is built from:

```text
NCBI gene2pubmed
```

Publication counts are mapped to Ensembl gene identifiers using:

```text
NCBI gene2ensembl
```

This contributes the field:

```text
n_publications
```

This field is used as the main publication-attention measure in H1, H2, and H3.

---

## 5. Protein-Protein Interaction Degree

PPI degree is computed from the Open Targets interaction dataset.

Two versions are included:

| Field | Description |
|---|---|
| broad PPI degree | computed using all source databases |
| curated PPI degree | computed using selected curated databases |

The broad version includes all Open Targets interaction source databases and is dominated by STRING.

The curated version is restricted to:

```text
IntAct
SIGNOR
Reactome
```

PPI degree is used as a structural covariate for H3.

---

# Constraint Extraction

The Open Targets `constraint` field is an array of structs.

Each gene usually contains three constraint records:

```text
synonymous
missense
loss-of-function
```

The canonical build extracts the loss-of-function constraint record by filtering:

```text
constraintType = "lof"
```

The extracted fields are then flattened into row-level columns.

Fields exposed include:

```text
constraint_score
constraint_oe
constraint_upperBin
```

---

## Recommended Constraint Covariate

The recommended single constraint covariate for H3 is:

```text
constraint_upperBin
```

The `upperBin` field is a decile rank from `0` to `9`.

Interpretation:

| `upperBin` | Meaning |
|---:|---|
| `0` | most loss-of-function intolerant genes |
| `9` | least loss-of-function intolerant genes |

So lower `upperBin` values indicate stronger loss-of-function constraint.

---

# Deduplication Step

An initial build produced:

```text
4,525,741 rows
```

This was:

```text
17,739 rows more than the source file
```

The expected row count from `association_overall_direct` was:

```text
4,508,002 rows
```

---

## Cause of Row Inflation

The row inflation was traced to the attention table.

The attention table contained:

```text
281 Ensembl IDs
```

that mapped to multiple NCBI Gene IDs through `gene2ensembl`.

Because the attention table kept one row per:

```text
(ensembl_id, ncbi_gene_id)
```

some Ensembl IDs appeared multiple times.

When this duplicated attention table was joined to the association table, it created a fanout.

That means some target–disease associations were duplicated during the join.

---

## Deduplication Fix

The attention table was collapsed to one row per Ensembl ID by summing publication counts across NCBI Gene IDs.

Correct aggregation:

```text
ensembl_id → sum(n_publications across mapped NCBI Gene IDs)
```

This produced a strictly one-to-one attention table:

```text
one Ensembl ID → one publication count
```

After deduplication, the final canonical table row count was exactly:

```text
4,508,002 rows
```

matching the original `association_overall_direct` source file.

---

# Final Coverage

## Coverage Summary

| Field | Coverage | Notes |
|---|---:|---|
| `biotype` | 100.0% | Target metadata covers all Open Targets targets |
| `n_publications` | 99.0% | 43,936 rows missing |
| LOF constraint scores | 93.0% | mostly available for protein-coding genes with adequate exonic coverage |
| broad PPI degree | 97.4% | based on Open Targets interaction data |

---

## Publication Count Missingness

Publication counts are missing for:

```text
43,936 rows
```

These missing values mostly correspond to non-coding RNAs and pseudogenes that lacked an NCBI Gene mapping.

---

## Constraint Missingness

LOF constraint scores are available for approximately:

```text
93.0% of rows
```

This is expected because gnomAD LOEUF is primarily computed for protein-coding genes with adequate exonic coverage.

---

## PPI Missingness

Broad PPI degree is available for approximately:

```text
97.4% of rows
```

Genes missing from the PPI network are preserved as `NULL`.

---

# Missing Value Handling

Missing values are preserved as `NULL`.

Binary missingness indicator columns are also included so downstream models can either drop missing rows or include missingness as a covariate.

Missingness indicators include:

```text
attention_missing
ppi_all_missing
ppi_cur_missing
```

This avoids additional data wrangling during downstream analysis.

---

# What Is Not in the Canonical Table

The canonical table contains only filter inputs, not filter outputs.

In particular, F3 is not precomputed.

```text
F3 = largest connected component
```

is computed on demand for each filter combination during the factorial analysis.

This is necessary because the largest connected component depends on which other filters have already been applied.

For example, the LCC after applying only F1 may differ from the LCC after applying:

```text
F1 ∧ F2 ∧ F4
```

Therefore, F3 must be recomputed dynamically for each graph state.

---

# Downstream Step

The next step is to compute survival flags for all `2⁴ = 16` factorial filter combinations.

These survival flags are not stored in the canonical input table.

They are generated during downstream analysis from the filter inputs in `analysis.parquet`.

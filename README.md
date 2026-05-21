# kg_filtering

This repository contains the data-processing and analysis workflow for studying how common filters reshape Open Targets gene–disease knowledge graphs.

The project focuses on filters commonly used before downstream graph analysis, including:

- association score thresholds
- multi-source evidence requirements
- protein-coding restrictions
- largest connected component filtering

The goal is to measure how these filters change the retained target–disease graph and which genes remain available for downstream analysis.

---

## Project Structure

```text
kg_filtering/
├── OT_data/
├── gene2pubmed/
├── filter_thresholds/
├── Falsification_criteria/
├── PPI_addon/
├── canonical_input_table/
├── factorial/
└── log_reg/
```

---

## 1. `OT_data/`

This folder contains the initial Open Targets data collection and summary scripts.

It includes downloaded and converted Open Targets files for:

- overall target–disease association scores
- association scores by data source
- association scores by data type
- target metadata

### Key files

```text
source/
n_targets.py
run_parq.py
run_target_parq.py
sourcefile.md
data_collection.md
datasouce_summary.txt
datatype_summary.txt
n_targets_summary.txt
overall_summary.txt
target_summary.txt
```

### Purpose

This folder documents and processes the Open Targets input data used as the base of the project.

The main Open Targets datasets are:

```text
association_overall_direct
association_by_datasource_direct
association_by_datatype_direct
target
```

---

## 2. `gene2pubmed/`

This folder contains the publication-attention pipeline.

NCBI `gene2pubmed` is used to count how many PubMed papers are linked to each gene. Since Open Targets uses Ensembl gene IDs, NCBI Gene IDs are mapped to Ensembl IDs using `gene2ensembl`.

### Key files

```text
aggregated_per_gene_count.py
data_collection.md
gene_attention.parquet
map_to_ensenbl.py
per_count_gene2pubmed_summary.txt
```

### Output

```text
gene_attention.parquet
```

This file contains publication counts mapped to Ensembl gene IDs.

---

## 3. `filter_thresholds/`

This folder documents the rationale for the filter thresholds used in the project.

### Key file

```text
filtering_rationale.md
```

### Filters

| Filter | Description |
|---|---|
| F1 | overall association score threshold |
| F2 | minimum number of evidence sources |
| F3 | largest connected component |
| F4 | protein-coding restriction |

Default filter settings:

```text
F1: overall_score ≥ 0.5
F2: n_sources ≥ 2
F3: retain largest connected component
F4: biotype = protein_coding
```

Robustness settings include:

```text
F1 ≥ 0.2
F1 ≥ 0.8
F2 ≥ 3 sources
```

---

## 4. `Falsification_criteria/`

This folder defines the preregistered-style criteria for determining whether each hypothesis is supported or not.

### Key file

```text
falsification.md
```

### Main hypotheses

| Hypothesis | Question |
|---|---|
| H1 | Do individual filters retain higher-publication genes? |
| H2 | Do stacked filters compound non-linearly? |
| H3 | Do some genes under-survive relative to attention-based expectations? |

---

## 5. `PPI_addon/`

This folder contains the protein–protein interaction degree add-on.

Open Targets molecular interaction data are used to compute PPI degree for each target.

### Key files

```text
ppi_sumnmary.txt
steps.md
```

### Purpose

PPI degree is used as a structural covariate in the H3 regression analysis.

Two versions can be considered:

- broad PPI degree using all available interaction sources
- curated PPI degree using selected sources such as IntAct, SIGNOR, and Reactome

---

## 6. `canonical_input_table/`

This folder builds the main analysis-ready table.

### Key files

```text
cannonical_table_summary.txt
process.md
```

### Purpose

The canonical input table combines:

- Open Targets target–disease associations
- source counts
- data-type information
- target metadata
- publication counts
- PPI degree
- constraint annotations

Each row represents one:

```text
target–disease pair
```

The canonical table is the main input for the factorial and regression analyses.

---

## 7. `factorial/`

This folder contains the factorial filtering analysis.

### Key files

```text
README.md
factorial_result_meaning.md
factorial_summary.txt
```

### Purpose

The factorial analysis applies all combinations of the four filters:

```text
F1, F2, F3, F4
```

Since each filter can be on or off, the analysis has:

```text
2⁴ = 16 filter combinations
```

For each filter combination, the analysis records metrics such as:

- number of surviving target–disease pairs
- number of surviving targets
- number of surviving diseases
- mean publication attention
- protein-coding composition
- constraint coverage

---

## 8. `log_reg/`

This folder contains the regression analyses for H1, H2, and H3.

### Structure

```text
log_reg/
├── H1/
├── H2/
├── H3/
└── README.md
```

### Purpose

This folder contains the statistical analyses used to test the main project hypotheses.

| Folder | Purpose |
|---|---|
| `H1/` | tests whether individual filters retain higher-publication genes |
| `H2/` | tests whether filters interact non-linearly |
| `H3/` | identifies genes that under-survive or over-survive relative to attention-based expectations |

---

## Workflow Overview

The project workflow is:

```text
1. Download and process Open Targets data
        ↓
2. Build gene publication-attention table from NCBI gene2pubmed
        ↓
3. Define filter thresholds and falsification criteria
        ↓
4. Add PPI degree and structural covariates
        ↓
5. Build canonical input table
        ↓
6. Run 16-cell factorial filtering analysis
        ↓
7. Run H1, H2, and H3 regression analyses
```

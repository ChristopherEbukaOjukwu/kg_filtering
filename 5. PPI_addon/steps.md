# Downloading the PPI Data from Open Targets

## Step 1: Download

We use the Open Targets molecular interaction dataset:

<https://platform.opentargets.org/downloads>

Download command:

```bash
wget --recursive --no-parent --no-host-directories --cut-dirs 6 \
ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/interaction .
```

---

## Dataset Description

The Open Targets interaction file is an aggregated, deduplicated edge list.

Each row represents one:

```text
(targetA, targetB, source_database)
```

tuple.

This is the structure needed to compute PPI degree.

The computed PPI degree table is saved as:

```text
ppi_degree.parquet
```

---

## Joining PPI Degree to the H3 Regression Table

When building the H3 regression input table, `ppi_degree.parquet` is joined onto the target table using:

```text
targetId / ensembl_id
```

This follows the same identifier logic as the other gene-level covariates.

Genes that are not present in the PPI network will have missing PPI degree values.

These is handled as:

```sql
COALESCE(ppi_degree, 0)
```

However, we treat “not in PPI network” as a separate indicator variable.

This matters because some genes legitimately have no known interactions, especially newly annotated genes or less-studied genes.

Example:

```text
ppi_degree = 0
not_in_ppi = 1
```

This distinguishes genes with no observed PPI edges from genes whose degree is truly measured as zero.

---

# Practical Notes

## 1. Source Databases Differ in Evidence Quality

The Open Targets interaction file aggregates molecular interaction evidence from multiple PPI databases, including:

- IntAct
- SIGNOR
- Reactome
- STRING

These sources have different conventions and evidence standards.

For example, STRING includes predicted and text-mined interactions with confidence scores, while IntAct is mostly curated experimental interaction data.

Therefore, for a stricter “high-confidence” PPI degree, we filter by:

```text
sourceDatabase ∈ {IntAct, SIGNOR}
```

before computing degree.

This produces a more conservative interaction-degree covariate.

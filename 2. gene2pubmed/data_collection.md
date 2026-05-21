# Data Collection

NCBI publishes `gene2pubmed` as a single flat file with one row per `(gene, paper)` pair. This file is aggregated into per-gene publication counts. The Ensembl mapping is already available through the Open Targets Target file via `dbXrefs`, so no extra mapping table is needed beyond mapping NCBI Gene IDs to Ensembl IDs.

---
## NCBI Gene IDs Are Mapped to Ensembl IDs

The `gene2pubmed` file uses **NCBI Gene IDs** to link genes to PubMed articles. However, Open Targets primarily uses **Ensembl gene IDs** for targets. Because the identifiers are different, the publication counts from `gene2pubmed` cannot be joined directly to the Open Targets association files.

The workflow is therefore:

1. Use `gene2pubmed` to count publications per NCBI Gene ID.
2. Use `gene2ensembl` to map NCBI Gene IDs to Ensembl gene IDs.
3. Join the mapped publication counts to the Open Targets Target file using Ensembl ID.
4. Use the resulting table as `gene_attention.parquet`.

## Overall Workflow

```text
gene2pubmed     →  pub_counts (NCBI Gene ID → n_publications)
↓
JOIN on NCBI Gene ID
↓
gene2ensembl    →  ensembl_to_ncbi (NCBI Gene ID ↔ Ensembl ID)
↓
JOIN on Ensembl ID
↓
OT Target file  →  final gene_attention table (Ensembl ID → n_publications)
```

## Step 1: Download `gene2pubmed`

The file was downloaded from: https://ftp.ncbi.nlm.nih.gov/gene/DATA/.

File used:

```text
gene2pubmed.gz
```

| Field | Value |
|---|---|
| Last modified | 2026-05-20 05:08 |
| Compressed size | 253M |
| Uncompressed size | 1.8G |

Download command:

```bash
wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz
gunzip -k gene2pubmed.gz   # -k keeps the .gz too
```

The file is 253M zipped and 1.8G unzipped.

The file format is a three tab-separated columns:

| Column | Meaning |
|---|---|
| `#tax_id` | NCBI taxonomy ID |
| `GeneID` | NCBI Gene ID |
| `PubMed_ID` | PubMed publication ID |

Example rows:

```text
#tax_id GeneID  PubMed_ID
23      310495631       15925900
23      310495633       7751290
```
---

## Step 2: Aggregate to Per-Gene Publication Counts

The raw `gene2pubmed` file was aggregated into publication counts per NCBI Gene ID.

Source script:
```text
aggregated_per_gene_count.py
```

Output concept:
```text
NCBI Gene ID → n_publications
```

---

## Step 3: Download `gene2ensembl`

The file was downloaded from: <https://ftp.ncbi.nlm.nih.gov/gene/DATA/>

File used:

```text
gene2ensembl.gz
```

Metadata at download time:

| Field | Value |
|---|---|
| Last modified | 2026-05-20 05:05 |
| Compressed size | 276M |

Download command:

```bash
wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz
gunzip -k gene2ensembl.gz
```

Only the following columns were needed:

| Column | Meaning |
|---|---|
| `tax_id` | NCBI taxonomy ID |
| `GeneID` | NCBI Gene ID |
| `Ensembl_gene_identifier` | Ensembl gene ID |

This file was used to map:

```text
NCBI Gene ID ↔ Ensembl ID
```
Then the mapped table was joined on Ensembl ID to produce the final gene attention table.

Mapping script:

```text
map_to_ensenbl.py
```
Output file:

```text
gene_attention.parquet
```
---

## Mapping Summary

After mapping NCBI Gene IDs to Ensembl IDs:

| total_rows | unique_ensembl | unique_ncbi |
|---:|---:|---:|
| 38,548 | 38,267 | 38,516 |

### Mapping Coverage by Biotype
| Biotype | Total | Mapped | Percent Mapped |
|---|---:|---:|---:|
| `lncRNA` | 35,100 | 6,932 | 19.7 |
| `protein_coding` | 20,158 | 19,530 | 96.9 |
| `processed_pseudogene` | 9,487 | 3,832 | 40.4 |
| `misc_RNA` | 2,207 | 942 | 42.7 |
| `unprocessed_pseudogene` | 1,949 | 859 | 44.1 |
| `snRNA` | 1,901 | 1,839 | 96.7 |
| `miRNA` | 1,879 | 1,847 | 98.3 |
| `transcribed_unprocessed_pseudogene` | 1,587 | 376 | 23.7 |
| `transcribed_processed_pseudogene` | 1,149 | 338 | 29.4 |
| missing/blank biotype | 1,019 | 19 | 1.9 |
| `ribozyme` | 8 | 5 | 62.5 |
| `TR_C_gene` | 6 | 5 | 83.3 |
| `sRNA` | 5 | 1 | 20.0 |
| `TR_D_gene` | 5 | 5 | 100.0 |
| `vault_RNA` | 4 | 4 | 100.0 |
| `TR_J_pseudogene` | 4 | 4 | 100.0 |
| `IG_J_pseudogene` | 3 | 3 | 100.0 |
| `translated_processed_pseudogene` | 2 | 1 | 50.0 |
| `Mt_rRNA` | 2 | 2 | 100.0 |
| `IG_pseudogene` | 1 | 0 | 0.0 |

 Full table:

```text
37 rows total; 20 shown above.
```

---

### Most Published Genes in `gene_attention.parquet`
| Approved Symbol | Biotype | Number of Publications |
|---|---|---:|
| `TP53` | `protein_coding` | 11,627 |
| `EGFR` | `protein_coding` | 6,684 |
| `TNF` | `protein_coding` | 6,446 |
| `IL6` | `protein_coding` | 5,468 |
| `APOE` | `protein_coding` | 5,224 |
| `VEGFA` | `protein_coding` | 5,213 |
| `TGFB1` | `protein_coding` | 5,007 |
| `HIF1A` | `protein_coding` | 3,912 |
| `MTHFR` | `protein_coding` | 3,863 |
| `AKT1` | `protein_coding` | 3,746 |
| `STAT3` | `protein_coding` | 3,705 |
| `ESR1` | `protein_coding` | 3,640 |
| `IL10` | `protein_coding` | 3,485 |
| `BRCA1` | `protein_coding` | 3,449 |
| `NFKB1` | `protein_coding` | 3,396 |

### Publication Count Summary

| Total Genes | Genes with Zero Publications | Mean Publications | Median Publications | Maximum Publications |
|---:|---:|---:|---:|---:|
| 38,548 | 10,081 | 52.34 | 7.0 | 11,627 |



## Data Available After This Step

At the end of this step, the working data includes:

1. Open Targets association files:
   - `association_overall_direct`
   - `association_by_datatype_direct`
   - `association_by_datasource_direct`
2. Open Targets target metadata:
   - biotype
   - constraint
   - structural features
   - approved gene symbol
   - other target annotations
3. External gene attention data:
   - publication counts from `gene2pubmed`
   - mapped to Ensembl IDs using `gene2ensembl`
  
---

## Note on `gene_attention.parquet`

The `gene_attention.parquet` file contains:

```text
38,548 rows
```
The `gene_attention.parquet` file contains only the Open Targets genes that could be mapped from NCBI Gene IDs to Ensembl IDs. Therefore, all 38,548 Ensembl IDs in `gene_attention.parquet` are valid Open Targets targets, but they represent only a subset of the full 78,691 Open Targets Target file.

The OT Target file has ~78,691 targets. The gene_attention.parquet has 38,548. The missing ~40,000 are the targets that didn't map to NCBI Gene IDs, which are mostly lncRNAs (28,000 unmapped), pseudogenes (~9,000 unmapped), and a handful of others.


### The following issue was found:

| Metric | Value |
|---|---:|
| `attn_rows` | 38,548 |
| `attn_unique` | 38,267 |
| duplicate Ensembl ID rows | 281 |

This means the attention file contained 281 duplicate `ensembl_id` rows.

---

### Why Duplicates Occur

A few hundred genes map to multiple NCBI Gene IDs in `gene2ensembl`.  Specifically, Ensembl and NCBI independently identify and annotate genes, particularly non-coding RNAs and pseudogenes. if one gene model is split into two or more distinct genes in the NCBI database but kept as a single, contiguous gene in Ensembl, a 1:many map occurs.

This can happen because of:
- alternative loci
- X/Y pseudoautosomal copies
- other complex gene mapping cases

The initial `gene_attention.parquet` kept one row per:
```text
(ensembl_id, ncbi_gene_id)
```

instead of collapsing to one row per Ensembl gene.

---

### Deduplication Fix

To fix this, the attention table is deduplicated by summing publication counts across NCBI Gene IDs that map to the same Ensembl gene.

This keeps the data rather than dropping duplicate mappings.

Correct aggregation logic:

```text
ensembl_id → sum(n_publications across mapped NCBI Gene IDs)
```

After this fix, each Ensembl gene appeared only once in the attention table. This prevents duplicated gene rows from multiplying gene–disease associations during joins.

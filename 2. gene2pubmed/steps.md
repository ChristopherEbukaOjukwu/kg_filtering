# Data Collection For Gene2Pubmed

> NCBI publishes gene2pubmed as a single flat file: one row per (gene, paper) pair. This is then aggregated to per-gene counts. 
> The Ensembl mapping is already inside the Target file via dbXrefs, so no extra mapping table is needed.
>

gene2pubmed     →  pub_counts (NCBI Gene ID → n_publications)
                                    ↓
                            JOIN on NCBI Gene ID
                                    ↓
gene2ensembl    →  ensembl_to_ncbi (NCBI Gene ID ↔ Ensembl ID)
                                    ↓
                            JOIN on Ensembl ID
                                    ↓
OT Target file  →  final gene_attention table (Ensembl ID → n_publications)

## Step 1 Download.
The file used was gotten from https://ftp.ncbi.nlm.nih.gov/gene/DATA/:
gene2pubmed.gz (last modified date and time: 2026-05-20 05:08;  size: 253M)

wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz
gunzip -k gene2pubmed.gz   # -k keeps the .gz too

The file is 253M zipped and 1.8G unzipped.

File Format: Three tab-separated columns: #tax_id, GeneID (NCBI Gene ID), PubMed_ID.
#tax_id GeneID  PubMed_ID
23      310495631       15925900
23      310495633       7751290
23      310495633       9182530
23      310495633       10799476


## Step 2 Aggregate to per-gene counts.
source file: aggregated_per_gene_count.py

## step 3 get gene2ensembl
The file used was gotten from https://ftp.ncbi.nlm.nih.gov/gene/DATA/:
gene2ensembl.gz (last modified: 2026-05-20 05:05  size: 276M)

wget https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2ensembl.gz
gunzip -k gene2ensembl.gz

We only need: tax_id, GeneID (NCBI), and Ensembl_gene_identifier.

for mapping (NCBI Gene ID ↔ Ensembl ID) and JOIN on Ensembl ID for final gene_attention table: map_to_ensenbl.py saved to: gene_attention.parquet

┌────────────┬────────────────┬─────────────┐
│ total_rows │ unique_ensembl │ unique_ncbi │
│   int64    │     int64      │    int64    │
├────────────┼────────────────┼─────────────┤
│      38548 │          38267 │       38516 │
└────────────┴────────────────┴─────────────┘

┌────────────────────────────────────┬─────────┬──────────┬────────────┐
│              biotype               │ n_total │ n_mapped │ pct_mapped │
│              varchar               │  int64  │  int128  │   double   │
├────────────────────────────────────┼─────────┼──────────┼────────────┤
│ lncRNA                             │   35100 │     6932 │       19.7 │
│ protein_coding                     │   20158 │    19530 │       96.9 │
│ processed_pseudogene               │    9487 │     3832 │       40.4 │
│ misc_RNA                           │    2207 │      942 │       42.7 │
│ unprocessed_pseudogene             │    1949 │      859 │       44.1 │
│ snRNA                              │    1901 │     1839 │       96.7 │
│ miRNA                              │    1879 │     1847 │       98.3 │
│ transcribed_unprocessed_pseudogene │    1587 │      376 │       23.7 │
│ transcribed_processed_pseudogene   │    1149 │      338 │       29.4 │
│                                    │    1019 │       19 │        1.9 │
│    ·                               │       · │        · │         ·  │
│    ·                               │       · │        · │         ·  │
│    ·                               │       · │        · │         ·  │
│ ribozyme                           │       8 │        5 │       62.5 │
│ TR_C_gene                          │       6 │        5 │       83.3 │
│ sRNA                               │       5 │        1 │       20.0 │
│ TR_D_gene                          │       5 │        5 │      100.0 │
│ vault_RNA                          │       4 │        4 │      100.0 │
│ TR_J_pseudogene                    │       4 │        4 │      100.0 │
│ IG_J_pseudogene                    │       3 │        3 │      100.0 │
│ translated_processed_pseudogene    │       2 │        1 │       50.0 │
│ Mt_rRNA                            │       2 │        2 │      100.0 │
│ IG_pseudogene                      │       1 │        0 │        0.0 │
└────────────────────────────────────┴─────────┴──────────┴────────────┘
  37 rows (20 shown)                                         4 columns

┌────────────────┬────────────────┬────────────────┐
│ approvedSymbol │    biotype     │ n_publications │
│    varchar     │    varchar     │     int64      │
├────────────────┼────────────────┼────────────────┤
│ TP53           │ protein_coding │          11627 │
│ EGFR           │ protein_coding │           6684 │
│ TNF            │ protein_coding │           6446 │
│ IL6            │ protein_coding │           5468 │
│ APOE           │ protein_coding │           5224 │
│ VEGFA          │ protein_coding │           5213 │
│ TGFB1          │ protein_coding │           5007 │
│ HIF1A          │ protein_coding │           3912 │
│ MTHFR          │ protein_coding │           3863 │
│ AKT1           │ protein_coding │           3746 │
│ STAT3          │ protein_coding │           3705 │
│ ESR1           │ protein_coding │           3640 │
│ IL10           │ protein_coding │           3485 │
│ BRCA1          │ protein_coding │           3449 │
│ NFKB1          │ protein_coding │           3396 │
└────────────────┴────────────────┴────────────────┘
  15 rows                                3 columns

┌───────┬───────────┬──────────────────┬─────────────┬──────────┐
│ total │ zero_pubs │    mean_pubs     │ median_pubs │ max_pubs │
│ int64 │  int128   │      double      │   double    │  int64   │
├───────┼───────────┼──────────────────┼─────────────┼──────────┤
│ 38548 │     10081 │ 52.3444017847878 │         7.0 │    11627 │
└───────┴───────────┴──────────────────┴─────────────┴──────────┘



At the end of this step:
OT associations (overall, by-datatype, by-datasource)
OT target metadata (biotype, constraint, structural features)
External attention (gene2pubmed via gene2ensembl mapping)

NOTE:
What gene_attention.parquet contains:
38,548 rows. Each row is one Ensembl ID that succeeded in the gene2ensembl mapping. Those 38,548 IDs are all targets in OT's vocabulary, but they are not all the targets in OT.
The OT Target file has ~78,691 targets. The gene_attention.parquet has 38,548. The missing ~40,000 are the targets that didn't map to NCBI Gene IDs — mostly lncRNAs (28,000 unmapped), pseudogenes (~9,000 unmapped), and a handful of others.

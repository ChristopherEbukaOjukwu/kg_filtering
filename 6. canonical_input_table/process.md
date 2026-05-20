# The canonical input table

Per row (a target-disease pair):

Identifiers: targetId, diseaseId
For F1: overall_score (from association_overall_direct)
For F2: n_sources (distinct count from association_by_datasource_direct)
For F4 main: biotype (from Target, joined on targetId)
For F4 alt-spec: datatypes (array from association_by_datatype_direct — needed for the genetics-only robustness check)
For F3: computed after filtering, not pre-stored — connected components depend on which other filters are applied
For H3 right-hand side: n_publications, constraint_score, ppi_degree, chromosome
For interpretation: approvedSymbol, currentNovelty

## Here's a clean account you can drop into your methods or your lab notebook.

What the canonical analysis table does
The canonical analysis table (analysis.parquet) consolidates five separate Open Targets and external data sources into a single row-per-(target, disease) table. Each row contains all of the inputs needed to apply the four chapter-3 filters and to fit the H3 counterfactual baseline, eliminating the need to re-join across files during downstream analysis.
Sources joined. The base table is association_overall_direct, which contains one row per target-disease pair with Open Targets' overall harmonic-sum association score. Four additional sources are LEFT-joined onto this base, preserving the 4,508,002 target-disease pairs of the original file:

association_by_datasource_direct contributes the per-pair count of distinct data sources supporting each association (input for F2).
association_by_datatype_direct contributes the per-pair list of distinct data types (input for an alternative F4 specification restricted to genetic-association data types).
The Open Targets target dataset contributes per-gene metadata: biotype (input for the main F4 specification), chromosome, and the gnomAD loss-of-function constraint metrics (score, oe, upperBin) extracted from the constraint array of structs by filtering on constraintType = 'lof'.
External research-attention data (publication counts per gene), built from NCBI gene2pubmed and joined to Ensembl identifiers via NCBI gene2ensembl.
Protein-protein interaction degree, computed from Open Targets' interaction dataset in two variants: a broad version including all source databases (dominated by STRING) and a curated version restricted to IntAct, Signor, and Reactome.

Constraint extraction. The Open Targets constraint field is an array of three structs per gene (synonymous, missense, and loss-of-function constraint records from gnomAD). The canonical build unnests this array, filters to the lof record, and exposes its score, oe, and upperBin columns as flat row-level fields. The upperBin field is a 0-9 decile rank where 0 indicates the most loss-of-function-intolerant genes; this is the recommended single covariate for H3.
Deduplication step. An initial build produced 4,525,741 rows — 17,739 more than the source file. The inflation was traced to the attention table, which contained 281 Ensembl IDs mapped to multiple NCBI Gene IDs through gene2ensembl. These were collapsed by summing publication counts within each Ensembl ID, yielding a strictly 1-to-1 attention table and a final row count of exactly 4,508,002.
Final coverage. Biotype is available for 100% of rows (Target metadata covers all OT targets). Publication counts are available for 99.0% (43,936 rows missing, mostly non-coding RNAs and pseudogenes that lacked an NCBI Gene mapping). LOF constraint scores are available for 93.0% (gnomAD computes LOEUF primarily for protein-coding genes with adequate exonic coverage). PPI degree is available for 97.4% (broad version). Missing values are preserved as NULLs and accompanied by binary indicator columns (attention_missing, ppi_all_missing, ppi_cur_missing) so that downstream models can either drop these rows or include the indicator as a covariate without further data wrangling.
What is not in this table. F3 (largest connected component) is computed on demand for each filter combination during the factorial, because the LCC depends on which other filters have already been applied. The canonical table contains only filter inputs, not filter outputs; survival flags for the 16 factorial cells are computed in the next step.

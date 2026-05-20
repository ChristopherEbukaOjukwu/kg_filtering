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

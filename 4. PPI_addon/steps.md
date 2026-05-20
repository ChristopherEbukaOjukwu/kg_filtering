# Downloading the PPI data from OT

## Step 1 Download
We use the OT molecular interaction (https://platform.opentargets.org/downloads) dataset:
wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/interaction .

It is the  aggregated, deduplicated edge list; one row per (targetA, targetB, source_database) tuple, 
which is what we need to compute degree.

The computed degree is at: ppi_degree.parquet

When we build our H3 regression input table, this joins onto targetId / ensembl_id like everything else. Genes not in the PPI network get NULL and handled as COALESCE(ppi_degree, 0) or, more specifically, we treat "not in PPI" as a separate indicator variable (some genes legitimately have no known interactions, especially newly-annotated ones).

## Two practical notes.
The Open Targets interaction file aggregates multiple PPI databases (IntAct, Signor, Reactome, STRING). They have very different conventions, STRING in particular includes predicted and text-mined interactions with confidence scores, while IntAct is mostly curated experimental data. For a "high-confidence" PPI degree, we filter by sourceDatabase to just IntAct and Signor before computing degree. 
Second: PPI degree is itself attention-correlated. Well-studied genes have more characterized interactions because someone went looking. So adding PPI as a covariate doesn't fully decouple from the attention proxy, it partially does. Constraint (gnomAD LOEUF) is cleaner in this regard since it's computed from sequence variation, not from researcher attention. If you only have time to add one structural covariate, constraint > PPI.

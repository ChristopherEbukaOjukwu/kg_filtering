# Downloading the PPI data from OT

## Step 1 Download
We use the OT molecular interaction (https://platform.opentargets.org/downloads) dataset:
wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/interaction .

It is the  aggregated, deduplicated edge list; one row per (targetA, targetB, source_database) tuple, 
which is what you need to compute degree.

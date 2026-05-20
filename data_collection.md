# Initial data collection from OT
Three datasets were downloaded from "https://platform.opentargets.org/downloads/association_by_datasource_direct/access" on 5/20/2026:


1. Associations - direct (by data source): 
This gives source-specific evidence. Use for F2/F4: source-type constraints.
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_by_datasource_direct ."


2. Associations - direct (by data type): 
This gives evidence-type scores. Used for F2: ≥ N data types.
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_by_datatype_direct ."


3. Associations - direct (overall score): 
This gives the main gene–disease edge score. Used for F1: score ≥ threshold.
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_overall_direct ."

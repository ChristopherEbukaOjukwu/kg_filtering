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

4. Target:
This is the analogue of the overall file for nodes: one row per Ensembl gene ID with the canonical metadata (biotype, chromosome, protein class, approved symbol, etc.)
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/target ."


Targets in data:
A gene, in the modern definition, is just a region of DNA that gets transcribed into RNA. Whether that RNA then gets translated into a protein is a separate question, and the answer determines the gene's biotype:

1. protein_coding: transcribed into mRNA, then translated into a protein. ~20,000 of these in humans. These are the genes most people mean colloquially when they say "gene" — insulin, hemoglobin, TP53.
2. lncRNA (long non-coding RNA): transcribed into RNA, but the RNA itself is the functional product. It's never translated. Examples: XIST (which silences one X chromosome in female cells), HOTAIR, MALAT1. There are ~35,000 of these in the human genome, more than protein-coding ones — a relatively recent discovery.
3. miRNA (microRNA): transcribed into very short RNAs (~22 nucleotides) that regulate the expression of other genes by binding to their mRNA. Examples: let-7, miR-21.
4. snRNA, snoRNA, misc_RNA: small RNAs with various structural and processing roles in the cell.
5. pseudogene: a gene that was protein-coding at some point in evolution but has accumulated mutations that broke it. The DNA sequence still resembles a real gene but it doesn't produce a functional product. Mostly. Some pseudogenes turn out to have regulatory functions, which keeps biologists employed.

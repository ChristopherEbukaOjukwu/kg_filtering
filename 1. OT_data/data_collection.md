# Initial data collection from OT
Three association datasets and a Target dataset were downloaded from the Open Targets Platform on **May 20, 2026**.
**Source page:** <https://platform.opentargets.org/downloads>.
**Open Targets release:** `26.03`

## Downloaded Datasets

### 1. Associations - direct (by data source):

This dataset provides **source-specific evidence** (ClinVar, GWAS Catalog, europepmc) for target-disease association.

**Used for:**
- **F2/F4:** source-type constraints.

```bash
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_by_datasource_direct ."
```

---

### 2. Associations - direct (by data type): 

This dataset provides **evidence-type scores** (e.g., text mining, animal models, pathways) for gene–disease associations.

**Used for:**

- **F2:** retaining associations supported by at least `N` data types

```bash
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_by_datatype_direct ."
```

---

### 3. Associations - direct (overall score): 

This dataset provides the main **target–disease edge score**; an aggregated scientific evidence linking a target directly to a disease.

**Used for:**

- **F1:** for a score ≥ threshold.

```bash
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/association_overall_direct ."
```

---

### 4. Target:

This dataset provides metadata for target nodes, showing information about what each target node is:

- biotype
- chromosome
- protein class
- approved symbol
- target/gene annotations
  

Example:
- ENSG00000141510
- approved symbol: TP53
- biotype: protein_coding
- chromosome: 17
- protein class: transcription factor

```bash
"wget --recursive --no-parent --no-host-directories --cut-dirs 6 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/26.03/output/target ."
```

## Targets in the Data

In modern biology, a **gene** is a region of DNA that is transcribed into RNA. Whether that RNA is translated into a protein is a separate question. This distinction determines the gene’s **biotype**.

The Open Targets target metadata file includes different gene biotypes, including protein-coding genes, non-coding RNAs, and pseudogenes.

---

## Common Gene Biotypes

### 1. `protein_coding`

Protein-coding genes are transcribed into mRNA and then translated into proteins. These are the genes most people mean when they casually say “gene.” There are roughly **20,000 protein-coding genes** in humans.

**Examples:**

- `INS` — insulin
- `HBB` — hemoglobin beta
- `TP53`

---

### 2. `lncRNA`

Long non-coding RNAs are transcribed into RNA, but the RNA itself is the functional product. They are not translated into proteins. There are roughly **35,000 lncRNAs** in the human genome, making them more numerous than protein-coding genes.

**Examples:**
- `XIST`
- `HOTAIR`
- `MALAT1`
---

### 3. `miRNA`

MicroRNAs are transcribed into short RNA molecules, usually around **22 nucleotides** long. They regulate gene expression by binding to mRNA transcripts and affecting their stability or translation.

**Examples:**
- `let-7`
- `miR-21`

---

### 4. `snRNA`, `snoRNA`, and `misc_RNA`

These are small RNA classes involved in structural, regulatory, or RNA-processing roles in the cell.

They may be involved in:

- splicing
- ribosomal RNA modification
- RNA processing
- other regulatory functions

---

### 5. `pseudogene`

Pseudogenes are sequences that resemble functional genes but usually do not produce a functional product. Many originated from formerly protein-coding genes but accumulated mutations that disrupted their original function. Some pseudogenes may still have regulatory roles, so they can remain biologically relevant even when they do not encode functional proteins.

---

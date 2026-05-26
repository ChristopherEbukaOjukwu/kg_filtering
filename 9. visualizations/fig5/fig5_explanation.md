# What the figure shows

The figure plots all 17,793 protein-coding genes that have both Open Targets disease association data and an NCBI publication count, on a single panel that combines three pieces of information at once.

The **x-axis** is research attention, measured as log(publications + 1) from NCBI's gene2pubmed. Genes on the left have one or two papers about them; genes on the right have several thousand.

The **y-axis** is the binary survival outcome under stacked filtering (F1: overall score ≥ 0.5; F2: ≥ 2 data sources; F4: protein-coding). A gene at y = 1 has at least one disease association that passes all three filters. A gene at y = 0 has no such association. Small vertical jitter is added so that the thousands of genes at each outcome value spread into a visible stripe rather than overlapping at a single line.

The **black curve** shows the model's predicted probability of survival as a function of log(publications), holding the structural covariates (constraint bin, PPI degree, chromosome) at typical values. This is what the chapter's H3 baseline model predicts. The curve has the classic logistic S-shape: nearly zero at the low-publication end (genes with 1-2 papers almost never have strong, multi-source disease evidence), rising through ~0.5 at moderate publication counts, asymptoting near 1.0 at the high-attention extreme.

The **colors encode the residual** from the structural baseline. Red dots are genes that survive *less than the model predicts* (residual < -0.3). Blue dots are genes that survive *more than the model predicts* (residual > +0.3). Gray dots are the neutral majority where actual survival matches the baseline prediction within ±0.3.



## Reading the figure:

**Lower-right (red cluster).** The 4,004 under-survivor genes — 22.5% of the protein-coding population. Their distribution is striking: they pile up at moderate-to-high publication counts (log_pubs from ~3.5 to ~9), but their survival outcome is uniformly zero. The model predicts these genes *should* survive — based on their publication counts they're well above the curve's inflection point — but in practice they don't. The three labeled examples are at the extreme right: HIF1A, IFNG, and MDM2 each have thousands of associated publications and a high predicted probability of surviving filters, but none has any disease association that crosses both F1 and F2.

**Upper-left (blue cluster).** The 4,825 over-survivor genes — 27.1% of the population. These are the mirror-image case: low publication counts (log_pubs from ~1 to ~5) but actual survival. The model predicts they *shouldn't* survive (very low along the curve), but they do. The three labeled examples — OR10R2, GRXCR2, PRCD — each have fewer than five publications but managed to cross both F1 and F2. Mechanistically, this happens because a single high-quality curated source (typically a ClinGen Definitive or OMIM rare-disease entry) can push a gene over both thresholds even when broader research attention is minimal.

**The neutral majority (gray)** fades into the background, doing the visual work of showing where the prediction matches the data. The reader's eye naturally goes to the colored regions where the H3 story lives.


## What the figure argues

The chapter's central claim about filters is that they don't simply select for "well-studied" genes — they select for genes whose study has crystallized into focused, source-diverse disease anchors. The H3 hero figure makes this visible in the lower-right red cluster.

If filters were a clean attention proxy, every red dot would be missing. A high publication count would imply high survival. But many of the most-studied genes in human biology — master regulators, cytokines, MHC molecules, oncogenes — fail filter survival because their study is *broad* rather than *focused*. They show up in thousands of papers across hundreds of diseases, each appearance contributing a modest score and often only one source. The harmonic-sum scoring rewards concentration, and broadly-relevant biological hubs lack it.

Symmetrically, the upper-left blue cluster shows that even minimally-studied genes can survive filtering if their attention is concentrated in a single high-confidence curated source. OR10R2 is one of hundreds of olfactory receptors that appear in fewer than ten papers each; PRCD is associated with progressive rod-cone degeneration through a single ClinGen Definitive entry. Both pass F1 ∧ F2 not because they're well-studied but because the evidence they do have is sharp.

The figure therefore supports H3 not just numerically — 22.5% of the population is meaningfully under-predicted, 27.1% over-predicted — but mechanistically. The named genes in each cluster are recognizable archetypes of two different filter-survival modes, and the chapter's reader gets the structural point without needing to read the regression coefficients.


## Caption

**Figure 5. Filter survival relative to the attention-adjusted baseline (H3).** Each point represents one of 17,793 protein-coding genes with available publication counts (NCBI gene2pubmed) and gnomAD loss-of-function constraint. The x-axis shows log(publications + 1) as a measure of research attention. The y-axis shows binary survival in the stacked filter F1 ∧ F2 ∧ F4 (F1: overall association score ≥ 0.5; F2: ≥ 2 distinct data sources; F4: biotype = protein_coding), with small vertical jitter added for visibility. The black curve shows the predicted probability of survival from a logistic regression baseline that combines attention, constraint, PPI degree, and chromosome (full model AUC = 0.77). Points are colored by residual: red points are under-survivors (residual < −0.3, n = 4,004; 22.5% of the population) — genes that the baseline predicts *should* survive but do not. Blue points are over-survivors (residual > +0.3, n = 4,825; 27.1%) — genes the baseline predicts *should not* survive but do. Gray points are neutral (n = 8,964). Three under-survivors representing distinct biological domains are labeled: **HIF1A** (master hypoxia regulator), **IFNG** (cytokine, immune signaling), **MDM2** (p53 regulator, oncology). Three over-survivors representing the mirror-image mechanism are labeled: **OR10R2** (olfactory receptor, minimal research attention), **GRXCR2** (hearing-loss gene with single ClinGen entry), **PRCD** (rare-disease gene with high-confidence curated source). The under-survivor population concentrates in the lower-right (high attention, no survival) — a structural feature inconsistent with the simple claim that filters retain well-studied genes. Filters instead retain genes whose evidence has consolidated into focused, source-diverse disease anchors; broadly-studied pleiotropic hub genes lack this concentration even when their cumulative publication record is large.

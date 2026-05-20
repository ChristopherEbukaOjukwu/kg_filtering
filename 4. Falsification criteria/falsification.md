# Falsification critier for determining whether hypotheses hold

## Filter thresholds:

F1: overall association score ≥ 0.5 (main); robustness at 0.2 and 0.8
F2: ≥ 2 distinct data sources (main); robustness at ≥ 3
F3: restrict to the largest connected component
F4: biotype = protein_coding (main); robustness with genetic-associations datatype restriction

Analysis universe: All target-disease pairs in association_overall_direct with mapped targets 
(~28k targets after gene2ensembl mapping). For H3, we restrict further to targets with 
n_publications > 0 to enable attention regression.

## H1 Each filter individually retains higher-attention genes
**Claim**: Apply each filter alone. Compute the mean log(n_publications + 1) of surviving 
genes vs. dropped genes. The bias exists if survivors are systematically higher-attention.

H1 supported if:
For each of F1, F2, F3, F4 applied alone, mean log(pubs+1) of surviving genes exceeds that of dropped
genes by ≥ 0.5 log-units (~1.6× difference in raw pub counts). The effect is statistically 
significant (Mann-Whitney U test, p < 0.001) for at least 3 of 4 filters.

H1 failed if:
For 2 or more filters, the attention gap between survivors and dropped is < 0.2 log-units, 
OR is in the opposite direction.

Interpretation if mixed: If F3 (LCC) or F4 (protein-coding) show no attention bias individually, 
that's a finding; they're operating on different axes. We don't claim H1 failed if only F1 and F2 
show the effect; we revise the claim to "evidence-based filters (F1, F2) carry attention bias; structural 
filters (F3, F4) do not."

## H2 Stacked filters compound non-linearly

Claim: Run the 2⁴ factorial. Model gene survival probability as a function of filter indicators plus their interactions. 
Non-zero interaction coefficients mean filters aren't independent.

**Statistical setup: Logistic regression on per-gene survival:**
survive_i = β₀ + β₁·F1 + β₂·F2 + β₃·F3 + β₄·F4
          + β₁₂·F1·F2 + β₁₃·F1·F3 + ... (all 6 pairwise terms)
          + (optional higher-order terms if pairwise underdescribes)
where each filter is a binary indicator (1 = filter applied).

H2 supported if:

At least 2 of 6 pairwise interaction terms have |β| ≥ 0.3 (log-odds scale) and 
p < 0.01 after Bonferroni correction.
AND: Top-100 gene overlap between F1-alone-survivors and F1∧F2∧F3∧F4-survivors is < 0.7 
(i.e., stacking removes >30% of the F1 set despite each additional filter "only" removing 
a fraction individually).

H2 failed if:

All pairwise interactions are |β| < 0.1, OR
Top-100 overlap exceeds 0.85 (filters act nearly independently; stacking is redundant).

The pivot if H2 fails: The chapter becomes "filters are largely 
redundant; a methodological note on apparent multi-filter robustness in published pipelines." 

## H3 Some genes under-survive relative to attention baseline.

Claim: Build a logistic regression predicting survival from attention alone (and structural covariates). 
Identify genes whose actual survival is lower than predicted. These are the "should-be-kept-but-aren't" 
cases.

Statistical setup:
Baseline model:
P(survive_i | F1∧F2∧F3∧F4) = logit⁻¹(α + γ·log(pubs_i + 1) + δ·structural_covariates_i)

Where structural covariates include:
1. biotype (categorical, restricted to protein-coding for main analysis)
2. chromosome (categorical, to absorb chromosomal biases)

Compute residuals: residual_i = actual_survival_i - predicted_P_i.

H3 supported if:

The baseline model has AUC < 0.85 on hold-out data. (If attention + structure perfectly predict survival, there's no residual signal to characterize.)
At least 5% of genes have |residual| > 0.3 — i.e., a substantial under/over-survival population exists.
The bottom-100 residual genes (most under-surviving) show a non-random structural enrichment: at least one biotype/chromosome/constraint category is over-represented at p < 0.01 vs. background.

H3 failed if:

Baseline AUC ≥ 0.95 — attention + structure fully explain survival, no residual signal.
OR: under-survivor residuals show no structural pattern beyond noise.

Hard interpretation rule: Even if H3 is supported, we do not claim the under-surviving genes are 
"biologically important but unfairly excluded." We claim only what the data shows: "These genes survive 
filtering at rates lower than their measured attention and structural features predict." Causal 
interpretation (unfairly excluded vs. correctly weak) requires evidence we do not have.

Cross-cutting commitments
No threshold tuning after seeing results. F1 ≥ 0.5 is the main threshold. If H2 fails at 0.5 but 
succeeds at 0.3, do not retroactively switch. Report all three and let the inconsistency be the finding.
Multiple comparisons. With 6 pairwise interaction terms, Bonferroni at α = 0.01 means individual 
p < 0.00167. State this in the methods. Effect size reporting. Report all interaction terms regardless 
of significance. The story is about magnitudes, not p-values. p-values are screening; β coefficients 
carry the actual claim.

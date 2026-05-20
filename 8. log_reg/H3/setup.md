H3: counterfactual baselineThe question H3 asks: after controlling for measured attention and structural features, does any signal remain in which genes do or don't survive filtering?If yes, the residual pattern of under-survival isn't fully explained by "well-studied genes survive more" — there's something else going on, and the structural enrichment of the under-survivors tells you what.If no, the entire filter-survival story collapses to attention bias plus measured biology, with no residual mystery to characterize.SetupUnit of analysis: target (one row per gene), restricted to:

Targets that survive at least one filter combination (otherwise we're modeling nothing — pure non-survivors carry no information)
Targets with publication count data (attention_missing == 0)
Targets with measured constraint (constraint_bin IS NOT NULL) — required for the structural baseline
The constraint requirement effectively restricts H3 to protein-coding genes, which is fine: that's where the disease-association literature operates and where the chapter's findings are most consequential.Outcome variable: binary indicator for survival in the fully-stacked cell (F1 ∧ F2 ∧ F4). Target survives the stacked filter if it has at least one association passing all three filters. We drop F3 because, as established, it does effectively no work.Predictors:

log_pubs = log(n_publications + 1) — attention
constraint_bin — gnomAD LOEUF decile (0-9, with 0 = most LOF-intolerant)
log_ppi_degree = log(ppi_degree_all + 1) — interaction-space density
chromosome — categorical, absorbs chromosomal idiosyncrasies
Model: logistic regression. Standard, interpretable, gives you per-gene predicted survival probabilities and well-defined residuals.

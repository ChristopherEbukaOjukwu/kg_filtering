## The H2 logistic regression. 

**The setup:**

1. Unit of analysis: target-disease pair. Population: all 4,508,002 pairs.
2. Outcome variable: survival in the fully-filtered cell (F1 ∧ F2 ∧ F3 ∧ F4). Binary.
3. Predictors: binary indicators for each individual filter, plus pairwise interactions.

Conceptually: given that we know F1/F2/F3/F4 individually flag certain pairs, can we predict 
fully-stacked survival linearly from those individual flags? If yes (low interaction effects), 
the filters compose additively. If no (large interaction effects), the filters interact, H2 supported.
A subtlety: H2 doesn't actually require running a regression on the full 4.5M dataset. 
The 16-cell factorial is the data. The regression operates on contingency-table logic, 
fitting log-linear effects to predict cell counts. But for clarity and ease of fitting, 
we'll do the per-pair version.

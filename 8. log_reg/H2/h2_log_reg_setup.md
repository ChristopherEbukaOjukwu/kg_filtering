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

Also, So the regression that actually tests H2 isn't "predict stacked survival from individual flags" (that's trivial). It's a different question: does the size of each filtered subgraph deviate from what the marginal filter rates predict under independence?

The log-linear setup
Let n_{abcd} be the count of pairs in cell (F1=a, F2=b, F3=c, F4=d); these are the 16 numbers from your factorial. Under independence of all four filters, we'd expect:

E[n_{abcd}] ∝ P(F1=a) × P(F2=b) × P(F3=c) × P(F4=d)

Any deviation from this multiplicative structure is an interaction effect. Fitting a Poisson regression with main effects and interactions to the 16 cell counts decomposes the deviation into specific 2-way (F1×F2, F1×F4, etc.) and higher-order interactions.
Significant interaction coefficients = H2 supported.
But — and this matters — your factorial cells aren't independent populations. Each cell is a subset nested inside the unfiltered set. To get this right, we need to recast the data slightly. Instead of cell counts, we work with the 2⁴ contingency table of (passes_F1, passes_F2, passes_F3, passes_F4) for each of the 4.5M pairs.

The source file to run this is: h2_log_reg.py

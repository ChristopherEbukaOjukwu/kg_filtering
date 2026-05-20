# Here is some reasoning behind the filtering decisions

## f1 Overall association score threshold:

The rationale here for using multiple thresholds is found here https://academic.oup.com/bioinformatics/article/41/7/btaf383/8177146?login=false
as there is no consensus.
Despite this, the non-linearity hypothesis (H2) should hold across all three.

Here, we use three threshold scores based on the literature.
1. 0.2 used in the AstraZeneca Mantis-ML 2.0 paper: https://www.science.org/doi/10.1126/sciadv.adj1424.
2. 0.5 an arbitrary middle.
3. 0.8

## F2 multi-source threshold
The common practice is "≥2 independent lines of evidence," which mirrors the ClinGen gene-disease validity 
framework (a well-cited curation standard from Strande et al., AJHG 2017)

## F3 largest connected component
No threshold. Largest component will be taken.

## F4 biotype / type constraint
1. Node constraint: protein-coding only.
2. Edge constraint: gene association only.


| | F1 | F2 | F4 |
|---|---|---|---|
| Permissive | ≥ 0.2 | ≥ 2 sources | protein-coding |
| Default | ≥ 0.5 | ≥ 2 sources | protein-coding |
| Stringent | ≥ 0.8 | ≥ 3 sources | protein-coding + genetics-only |


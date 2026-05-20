#Filters in Target–Disease Knowledge Graphs

## Core framing

Use **target**, not gene, because Open Targets is organized around target–disease associations.

> Filters applied to target–disease KGs preferentially retain high-attention targets, and stacked filters compound this selectivity.

Your unit can be either:

```text
Primary unit: target–disease association
Secondary unit: target
```

A target “survives” if at least one of its target–disease edges survives.

---

# Filters

## F1: Evidence score ≥ threshold

This keeps only target–disease pairs with strong Open Targets association scores.

**Likely bias mechanism:** high-attention targets usually have more accumulated evidence, so they are more likely to pass the score threshold.

**H1 test:**  
Do targets retained by F1 have higher publication counts than targets removed by F1?

```text
survival ~ log(publication_count)
```

Expected H1 result:

```text
β_publication > 0
```

Meaning: more published targets are more likely to survive the score filter.

---

## F2: ≥ N source types

This keeps associations supported by multiple evidence sources or data types.

Example:

```text
Keep target–disease pairs with evidence from ≥ 2 data sources
```

or:

```text
Keep target–disease pairs with evidence from ≥ 2 data types
```

**Likely bias mechanism:** well-studied targets are more likely to appear in many databases, papers, clinical resources, and curated datasets.

This may be the most attention-biased filter.

**H1 test:**  
Do targets retained by the “multi-source” filter have higher publication counts?

Expected result:

```text
high-attention targets survive more often
low-attention targets are removed more often
```

---

## F3: Largest connected component only

You build a bipartite graph:

```text
target -- disease
```

Then keep only the largest connected component.

**Likely bias mechanism:** canonical targets connect to many diseases; canonical diseases connect to many targets. Rare, specific, or understudied target–disease pairs may sit in small disconnected components.

**H1 test:**  
Compare publication counts of targets inside vs. outside the largest connected component.

Expected result:

```text
targets inside LCC have higher attention
targets outside LCC have lower attention
```

But this filter is more structural than F1/F2. It may retain targets because they are graph-central, not only because they are published.

---

## F4: Metapath/type constraint

In Open Targets, this is probably better phrased as:

> evidence-type or source-type constraint

because Open Targets is not exactly a Hetionet-style metapath KG unless you explicitly model paths through evidence/source nodes.

Example F4 versions:

```text
keep only genetics-supported associations
keep only clinical-precedence-supported associations
keep only pathway-supported associations
keep only associations supported by genetics + clinical evidence
```

**Likely bias mechanism:** some evidence types are more available for canonical, well-funded, well-studied targets.

**H1 test:**  
Do targets surviving a specific evidence-type constraint have higher publication counts?

Expected result:

```text
clinical/genetics/pathway-constrained survivors are more canonical and higher-attention
```

---

# H1: Bias exists

H1 asks:

> Does each filter individually retain higher-attention targets?

Run each filter alone:

```text
No filter
F1 only
F2 only
F3 only
F4 only
```

For each one, compare:

```text
retained targets vs removed targets
```

using:

```text
publication count
citation count if available
target degree
number of diseases per target
target category / biotype
```

Simple model:

```text
Survived_filter_i ~ log(publication_count)
```

H1 is supported if:

```text
publication coefficient > 0
```

for most or all filters.

Plain English:

> Each filter is supposed to improve KG quality, but it also acts as an attention filter.

---

# H2: Non-linear compounding

H2 asks:

> When filters are stacked, is the surviving set more selective than expected from the individual filters alone?

This is where the 2⁴ factorial design matters.

Run all 16 combinations:

```text
none
F1
F2
F3
F4
F1 + F2
F1 + F3
F1 + F4
F2 + F3
...
F1 + F2 + F3 + F4
```

Then fit:

```text
Survival ~ F1 + F2 + F3 + F4
         + F1:F2 + F1:F3 + F1:F4
         + F2:F3 + F2:F4 + F3:F4
         + higher-order interactions
```

If filters are merely additive, then this is enough:

```text
Survival ~ F1 + F2 + F3 + F4
```

But if stacked filters compound bias, interaction terms matter:

```text
F1:F2 ≠ 0
F1:F3 ≠ 0
F2:F4 ≠ 0
F1:F2:F3 ≠ 0
```

H2 is supported if combined filters retain a much narrower target set than expected.

Example:

```text
F1 alone keeps 60%
F2 alone keeps 50%

If independent, F1 + F2 might keep about 30%

But observed F1 + F2 keeps only 10%
```

That means the filters are not just independently removing weak edges. They are jointly selecting a more canonical subset.

Plain English:

> The scary part is not that each filter removes data. The scary part is that stacked filters may repeatedly favor the same already-canonical targets.

---

# H3: Structural counterfactual

H3 asks:

> Are there targets that should survive based on research attention, but still get removed because of graph structure or evidence-type structure?

This is different from H1.

H1 says:

```text
high-attention targets survive more often
```

H3 says:

```text
some high-attention targets still under-survive
```

For example:

```text
Target A has many publications
But it fails F3 because it sits outside the largest connected component

Target B has many publications
But it fails F2 because evidence is concentrated in one data source

Target C has many publications
But it fails F4 because it lacks the required evidence type
```

So you fit an attention-only expectation model:

```text
Survival ~ log(publication_count)
```

Then find targets where:

```text
predicted survival probability = high
actual survival = 0
```

Those are your **under-surviving targets**.

Better wording:

> targets that under-survive relative to their attention-predicted survival probability.

Not:

> targets that should have been kept.

Because “should” sounds like you know biological truth.

---

# How the hypotheses connect to filters

| Hypothesis | Question | Uses which filters? | Main output |
|---|---|---|---|
| H1 | Does each filter favor high-attention targets? | F1, F2, F3, F4 separately | Retained vs removed publication counts |
| H2 | Do stacked filters compound selectivity non-linearly? | All 16 filter combinations | Interaction coefficients |
| H3 | Which targets under-survive despite high attention? | Usually stacked filters, plus individual filters | Residual/under-survival list |

---

# Clean study logic

```text
F1 asks: does score thresholding favor known targets?

F2 asks: does multi-source evidence favor known targets?

F3 asks: does graph connectivity favor known targets?

F4 asks: do evidence-type constraints favor known targets?

H1 asks: does each filter do this individually?

H2 asks: do combinations of filters intensify this beyond expectation?

H3 asks: which targets are unexpectedly removed, even after accounting for attention?
```

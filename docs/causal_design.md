# Causal design memo

This document outlines next-stage causal research designs for SSRO applications.

## Current status

The current repository only performs descriptive analysis on a synthetic dataset.
It does not estimate causal effects.

## Why causal design matters

A descriptive wage gap or exposure difference does not tell us whether AI causes inequality changes.
To make a stronger claim, the project needs a credible identification strategy.

## Candidate designs for labor-market inequality

### 1. Difference-in-differences
Use staggered adoption of generative AI tools across firms, occupations, or regions.

Possible comparison:
- treatment: firms or occupations with earlier AI adoption
- control: similar units with later or no adoption

Key checks:
- parallel trends
- cohort-specific dynamics
- treatment timing heterogeneity

### 2. Event study
Study dynamic changes around a public release, enterprise rollout, or policy change related to AI tools.

Possible outcomes:
- posted wages
- skill requirements
- education requirements
- AI exposure language in postings

Key checks:
- pre-trends
- window sensitivity
- anticipation effects

### 3. Shift-share or exposure design
Construct exposure measures based on pre-existing occupational task bundles.
Then test whether high-exposure labor markets changed differently after AI shocks.

Key checks:
- baseline comparability
- exposure validity
- sensitivity to alternative taxonomies

### 4. Matched comparisons
Match firms, occupations, or postings on observables before comparing outcomes.

Useful when:
- treatment is not randomized
- strong balance is needed before outcome comparison

## Threats to identification

- occupational composition shifts
- industry-specific shocks
- wage posting selection
- measurement error in AI exposure
- endogenous adoption of AI tools

## What a stronger version of SSRO should do

A stronger research package should produce:
- a design memo
- identifying assumptions
- pre-trend diagnostics
- robustness to alternative exposure definitions
- validity and falsification checks

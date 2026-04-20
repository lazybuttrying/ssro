# Measurement memo

This document explains the current measurement design in the starter SSRO pipeline.

## Purpose

The current demo focuses on a toy question about generative AI and labor-market inequality.
The variables are intentionally simple and illustrative rather than research-grade.

## Core variables

### `education_score`
An ordinal proxy for formal education requirements.

Mapping:
- `HighSchool` → 1
- `Bachelor` → 2
- `Master` → 3
- `PhD` → 4
- `Unknown` → 0

### `high_skill_signal`
A count of high-skill keywords found in the posting text.

Current keywords:
- `python`
- `econometrics`
- `evaluation`
- `mlops`
- `causal inference`
- `api`

### `routine_signal`
A count of routine-task keywords found in the posting text.

Current keywords:
- `scheduling`
- `packing`
- `scanning`
- `crm`

### `ai_exposure_score`
A simple proxy for exposure to AI-related work.

Current rule:
- start from `ai_related * 2`
- add 1 if at least one high-skill keyword is present

This is meant only as a starter proxy.

### `high_skill_job`
A binary indicator of likely high-skill jobs.

Current rule:
- 1 if `education_score >= 2`
- or 1 if `high_skill_signal >= 1`
- otherwise 0

## Why this is only a starter

These variables are deliberately simple so the repository can demonstrate a full research workflow.
They should not be treated as valid substantive measures for publication.

## Main threats to validity

- keyword-based measurement can misclassify jobs
- education requirements do not fully capture skill intensity
- AI-related labels may not reflect true task-level AI exposure
- posted wages may differ from realized compensation

## Better next-stage measurement options

- occupation-task mappings using O*NET or similar taxonomies
- richer text classification instead of keyword matching
- separate measures of substitution risk and complementarity
- human annotation protocols for validation samples
- inter-annotator agreement checks

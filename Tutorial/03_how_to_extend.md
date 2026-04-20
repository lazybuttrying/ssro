# 03. How to extend SSRO

This tutorial explains how to adapt the starter repository to your own research topic.

## Goal

The current demo is about generative AI and labor-market inequality.
But SSRO is designed so that the core architecture stays the same even when the topic changes.

Think of the repository like this:
- the **architecture** stays stable
- the **application topic** changes

## What usually changes first

### 1. Research question
Edit `main.py` and replace the current task with your own.

Possible examples:
- finance and information asymmetry
- digital inequality
- platform governance
- AI policy

## 2. Input data
Replace:
- `data/raw/sample_job_postings.csv`

with your own dataset.

Possible examples:
- labor-market text data
- financial text data
- public documents
- survey or panel data

## 3. Measurement rules
The most important file for topic adaptation is:
- `research_os/agents/research_work.py`

In particular, the `MeasurementAgent` defines how concepts become variables.

That is where you should change:
- keyword sets
- operational definitions
- index construction rules
- proxy logic

## 4. Measurement documentation
If you change measurement, also update:
- `docs/measurement.md`
- the codebook output if needed

## 5. Causal design memo
If your project moves beyond descriptive analysis, update:
- `docs/causal_design.md`

This should explain:
- possible identification strategies
- threats to inference
- what stronger evidence would require

## 6. Output artifacts
If your project needs different outputs, modify the analysis stage.

Examples:
- add more figures
- export tables for slides
- write a memo for a paper
- add richer audit checks

## Suggested extension path

A good order is:
1. change the research question
2. replace the raw data
3. revise measurement logic
4. update docs
5. add better figures
6. strengthen audit
7. add a better causal design section

## Rule of thumb

If you only swap the topic name, the project stays shallow.
If you update the **measurement layer** and the **audit layer**, the project becomes much more convincing.

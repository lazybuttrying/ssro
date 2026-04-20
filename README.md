# Social Science Research OS

A three-layer multi-agent operating system for social science research.

This repository implements a minimal but runnable Research OS that separates:

- **Level 1: Governance** — decide what to study and preserve research memory
- **Level 2: Research Work** — build theory, data, measurement, analysis, and synthesis
- **Level 3: Audit** — check reproducibility, robustness, and validity

The goal is not to fully automate social science research, but to structure it into accountable responsibilities with explicit intermediate outputs.

## Core idea

Instead of treating research as a single monolithic task, this system models it as a layered workflow:

- governance
- empirical work
- audit

This makes research workflows more structured, reproducible, and accountable.

## Current demo domain

This starter repository includes a toy application for:

**Generative AI and labor-market inequality**

The example uses a small synthetic job-postings dataset and demonstrates:
- data cleaning
- variable construction
- AI exposure measurement
- simple descriptive inequality analysis
- audit reports

## Repository layout

```text
social-science-research-os/
├─ main.py
├─ configs/
├─ data/
├─ docs/
├─ outputs/
├─ tests/
└─ research_os/
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

## Generated outputs

Running `python main.py` creates:

- `outputs/research_brief.json`
- `outputs/literature_map.json`
- `outputs/data_memo.json`
- `outputs/cleaned_data.csv`
- `outputs/measured_data.csv`
- `outputs/codebook.json`
- `outputs/analysis_results.json`
- `outputs/abstract_draft.txt`
- `outputs/reproducibility_report.json`
- `outputs/robustness_report.json`
- `outputs/bias_validity_report.json`
- `outputs/provenance_log.json`

## Agents

### Level 1 — Governance
- `ResearchDirectorAgent`
- `ProvenanceManager`

### Level 2 — Research Work
- `LiteratureTheoryAgent`
- `DataConstructionAgent`
- `MeasurementAgent`
- `IdentificationAnalysisAgent`
- `WritingSynthesisAgent`

### Level 3 — Audit
- `ReproducibilityAgent`
- `RobustnessSensitivityAgent`
- `BiasValidityAuditAgent`

## Suggested next steps

- replace synthetic data with real job-postings data
- add LLM-backed literature extraction
- add richer measurement protocols
- add causal designs such as event study or DiD
- add report generation or dashboarding

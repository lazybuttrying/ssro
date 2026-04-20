# Social Science Research OS

[![Tests](https://github.com/lazybuttrying/utility/actions/workflows/tests.yml/badge.svg)](https://github.com/lazybuttrying/utility/actions/workflows/tests.yml)

A three-layer multi-agent operating system for social science research.

This repository is a **research infrastructure prototype**. It treats social science research not as a single monolithic task, but as a layered workflow with distinct responsibilities:

- **Level 1: Governance** — decide what to study and preserve research memory
- **Level 2: Research Work** — build theory, data, measurement, analysis, and synthesis
- **Level 3: Audit** — check reproducibility, robustness, and validity

The goal is not to fully automate research. The goal is to make research workflows more **structured, reproducible, interpretable, and accountable**.

> Recommended future repo name: `SSRO`

---

## Start here

- `Tutorial/01_quickstart.md`
- `Tutorial/02_outputs_walkthrough.md`
- `docs/implementation_checklist.md`

---

## Why this project exists

In real social science research, one person often has to do everything at once:

- refine the research question
- map prior literature
- build datasets
- operationalize abstract concepts
- choose identification strategies
- interpret results
- document limitations and reproducibility

That creates a familiar problem: theory, measurement, analysis, and audit often become loosely connected.

This repository proposes a different approach:

> **distribute research responsibility instead of pretending research is one task**

The system is designed as a minimal **Research OS** for social science.

---

## Core idea

Instead of relying on a single all-purpose assistant, this system separates research into three layers:

### Level 1 — Governance
Responsible for research direction and memory.

- define research goals
- clarify the current stage of inquiry
- keep track of decisions, versions, and changes

### Level 2 — Research Work
Responsible for the core empirical workflow.

- literature and theory mapping
- data construction
- measurement design
- descriptive and causal analysis
- writing and synthesis

### Level 3 — Audit
Responsible for research trustworthiness.

- reproducibility checks
- robustness and sensitivity checks
- bias and validity review

This makes the system look less like a chatbot and more like a **layered operating system for research workflows**.

---

## Current demo domain

This starter repository includes a toy application for:

**Generative AI and labor-market inequality**

The current example uses a small synthetic job-postings dataset and demonstrates:
- data cleaning
- variable construction
- AI exposure measurement
- measurement registry generation
- design registry generation
- simple descriptive inequality analysis
- figure export
- working note generation
- reproducibility and validity reporting

This topic is only the **first application package**. The architecture is meant to be topic-agnostic and reusable for domains such as:
- labor markets
- finance
- digital inequality
- platform governance
- AI policy and evaluation

---

## Repository layout

```text
SSRO/
├─ README.md
├─ requirements.txt
├─ pyproject.toml
├─ Makefile
├─ main.py
├─ Tutorial/
├─ applications/
├─ configs/
├─ data/
├─ docs/
├─ outputs/
├─ tests/
└─ research_os/
```

### Important folders

- `research_os/` — core package for orchestration, storage, schemas, and agents
- `Tutorial/` — guided walkthroughs for first-time readers
- `applications/` — topic-specific application packages
- `docs/` — architecture, agent responsibilities, measurement design, causal design, and implementation checklist
- `data/raw/` — starter input data
- `outputs/` — generated artifacts from the pipeline
- `tests/` — smoke tests and unit tests

---

## Agent architecture

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

A more detailed explanation is in:
- `docs/architecture.md`
- `docs/agents.md`
- `docs/measurement.md`
- `docs/causal_design.md`
- `docs/outputs.md`
- `docs/demo_run.md`
- `docs/implementation_checklist.md`

---

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
python main.py
```

Or with the Makefile:

```bash
make install
make run
make test
```

---

## Generated outputs

Running `python main.py` creates:

- `outputs/research_brief.json`
- `outputs/literature_map.json`
- `outputs/data_memo.json`
- `outputs/cleaned_data.csv`
- `outputs/measured_data.csv`
- `outputs/codebook.json`
- `outputs/measurement_registry.json`
- `outputs/design_registry.json`
- `outputs/research_entities.json`
- `outputs/analysis_results.json`
- `outputs/figure_wage_by_ai_related.png`
- `outputs/abstract_draft.txt`
- `outputs/working_note.md`
- `outputs/reproducibility_report.json`
- `outputs/robustness_report.json`
- `outputs/bias_validity_report.json`
- `outputs/provenance_log.json`
- `outputs/ssro.duckdb`

These files are meant to model a research workflow with explicit intermediate artifacts rather than just a final answer.

### Example output

A sample output walkthrough is available in:
- `docs/demo_run.md`

It includes example snippets for:
- `analysis_results.json`
- `provenance_log.json`

This helps the repository read more like a research systems prototype and less like an empty scaffold.

---

## What this repository currently shows

This repository is useful if you want to demonstrate that you can:

- design a multi-agent architecture for research rather than only for productivity demos
- translate abstract social-scientific concepts into structured workflows
- separate governance, empirical work, and audit
- build reproducible starter pipelines with intermediate outputs
- think about measurement and validity, not only automation
- export basic research artifacts such as figures, registries, and audit reports
- back research artifacts with lightweight local data infrastructure using DuckDB

In other words, this is not just an AI demo. It is a **research systems prototype**.

---

## Limitations

The current repository is intentionally minimal.

- the data are synthetic
- the analysis is descriptive, not causal
- the literature mapping is hand-coded rather than model-backed
- measurement is based on simple keyword proxies
- audit is illustrative rather than exhaustive
- Redis and retrieval helpers are scaffolding for future expansion rather than full production subsystems

That is acceptable for a starter repo, but the next stage should replace toy components with real research-grade modules.

---

## Suggested next steps

- rename the repository to `SSRO`
- replace synthetic data with real job-postings or domain-specific data
- add LLM-backed literature extraction and theory memo generation
- add richer measurement protocols and codebooks
- add causal designs such as event study, DiD, or matched comparisons
- add report generation and figure exports
- add provenance dashboards or experiment tracking

---

## Portfolio framing

A concise way to describe this repository is:

> **A three-layer multi-agent Research OS for social science that separates governance, empirical work, and audit.**

A slightly longer version:

> **This project treats social science research as a workflow of theory-building, data construction, measurement, analysis, and audit, rather than as a single monolithic assistant task.**

# 01. Quickstart

This tutorial shows the fastest way to run SSRO locally.

## Step 1. Clone the repository

```bash
git clone https://github.com/lazybuttrying/utility.git
cd utility
```

If you rename the repository later, replace the URL accordingly.

## Step 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

## Step 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or use the Makefile:

```bash
make install
```

## Step 4. Run the pipeline

```bash
python main.py
```

Or:

```bash
make run
```

## Step 5. Run tests

```bash
pytest
```

Or:

```bash
make test
```

## Step 6. Inspect outputs

After the run, check the `outputs/` folder.

Expected files include:
- `research_brief.json`
- `literature_map.json`
- `cleaned_data.csv`
- `measured_data.csv`
- `codebook.json`
- `analysis_results.json`
- `figure_wage_by_ai_related.png`
- `provenance_log.json`

## What you just did

You ran a minimal three-layer Research OS:
- governance generated a research brief
- research work created data, measures, and analysis
- audit produced reproducibility and validity reports

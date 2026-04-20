# Demo run outputs

This page shows example artifacts the pipeline is designed to generate.

## Example: `analysis_results.json`

```json
{
  "descriptive_summary": {
    "mean_wage_by_ai_related": {
      "0": 57000.0,
      "1": 98166.66666666667
    },
    "mean_wage_by_high_skill_job": {
      "0": 36000.0,
      "1": 101285.71428571429
    },
    "mean_ai_exposure_by_education": {
      "Bachelor": 1.25,
      "HighSchool": 1.0,
      "Master": 3.0
    },
    "share_high_skill_by_ai_related": {
      "0": 0.5,
      "1": 0.8333333333333334
    }
  },
  "high_skill_wage_gap": 65285.71428571429,
  "interpretation": [
    "In this toy dataset, AI-related postings are associated with higher posted wages.",
    "High-skill jobs display a substantial wage premium relative to lower-skill jobs.",
    "This starter analysis is descriptive and not causal."
  ]
}
```

## Example: `provenance_log.json`

```json
[
  {
    "step": "initialize_project",
    "details": {
      "title": "Generative AI and labor-market inequality",
      "domain": "labor_market_inequality"
    }
  },
  {
    "step": "research_brief_created",
    "details": {
      "stage": "exploratory"
    }
  },
  {
    "step": "analysis_completed",
    "details": {
      "high_skill_wage_gap": 65285.71428571429
    }
  }
]
```

## Why these artifacts matter

The point of this starter is not only to produce a final answer. It is to produce a sequence of explicit intermediate artifacts:

- research brief
- literature map
- cleaned data
- codebook
- descriptive results
- audit reports
- provenance log

That makes the workflow easier to inspect, evaluate, and extend.

from pathlib import Path

import pandas as pd

from research_os.agents.research_work import MeasurementAgent
from research_os.types import ResearchTask


def test_measurement_creates_expected_columns(tmp_path: Path) -> None:
    sample = pd.DataFrame(
        {
            "id": [1],
            "title": ["Economist"],
            "industry": ["Finance"],
            "year": [2025],
            "education": ["Master"],
            "wage_posted": [150000],
            "ai_related": [1],
            "skills_text": ["causal inference econometrics Python experimentation"],
        }
    )
    in_path = tmp_path / "cleaned_data.csv"
    sample.to_csv(in_path, index=False)

    agent = MeasurementAgent(tmp_path)
    task = ResearchTask(title="t", research_question="q", domain="d")
    out = agent.run(task, {"DataConstructionAgent": {"data_path": str(in_path)}})

    measured = pd.read_csv(out.payload["measured_data_path"])
    assert "ai_exposure_score" in measured.columns
    assert "high_skill_job" in measured.columns

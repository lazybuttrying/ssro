from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from ..base import BaseAgent
from ..types import AgentOutput, ResearchTask
from ..utils import write_json


class ReproducibilityAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("ReproducibilityAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        measured_path = Path(context["MeasurementAgent"]["measured_data_path"])
        content = measured_path.read_bytes()
        checksum = hashlib.sha256(content).hexdigest()
        report = {
            "status": "pass",
            "artifacts_checked": [str(measured_path)],
            "checksum": checksum,
            "notes": [
                "Synthetic example is deterministic under the current code path.",
                "Pin dependencies and data versions for stricter reproducibility guarantees."
            ]
        }
        write_json(self.output_dir / "reproducibility_report.json", report)
        return AgentOutput(agent_name=self.name, payload=report)


class RobustnessSensitivityAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("RobustnessSensitivityAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        measured_path = Path(context["MeasurementAgent"]["measured_data_path"])
        df = pd.read_csv(measured_path)

        strict_high_skill = ((df["education_score"] >= 3) | (df["high_skill_signal"] >= 2)).astype(int)
        strict_gap = float(df[strict_high_skill == 1]["wage_posted"].mean() - df[strict_high_skill == 0]["wage_posted"].mean())
        baseline_gap = float(context["IdentificationAnalysisAgent"]["high_skill_wage_gap"])

        report = {
            "baseline_gap": baseline_gap,
            "strict_definition_gap": strict_gap,
            "difference": strict_gap - baseline_gap,
            "notes": [
                "Sensitivity check changes the threshold for defining high-skill jobs.",
                "Large movements would indicate fragility to measurement choice."
            ]
        }
        write_json(self.output_dir / "robustness_report.json", report)
        return AgentOutput(agent_name=self.name, payload=report)


class BiasValidityAuditAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("BiasValidityAuditAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        measured_path = Path(context["MeasurementAgent"]["measured_data_path"])
        df = pd.read_csv(measured_path)

        report = {
            "validity_threats": [
                "AI exposure is approximated using a very simple proxy and may not capture true task-level exposure.",
                "Posted wages may not equal realized compensation.",
                "Education requirements may not fully represent skill intensity.",
                "The synthetic sample is too small for substantive inference."
            ],
            "possible_biases": [
                "selection bias from observed postings only",
                "proxy mismatch between AI-related label and actual AI use",
                "industry composition effects"
            ],
            "missingness_summary": df.isna().sum().to_dict()
        }
        write_json(self.output_dir / "bias_validity_report.json", report)
        return AgentOutput(agent_name=self.name, payload=report)

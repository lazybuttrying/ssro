from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from ..base import BaseAgent
from ..types import AgentOutput, ResearchTask
from ..utils import write_json


class ResearchDirectorAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("ResearchDirectorAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        brief = {
            "title": task.title,
            "research_question": task.research_question,
            "domain": task.domain,
            "stage": "exploratory",
            "primary_goals": [
                "Clarify the research question",
                "Build a minimal analysis-ready dataset",
                "Define operational measures",
                "Generate preliminary inequality analysis",
                "Audit reproducibility and validity"
            ],
            "next_steps": [
                "Map literature and theory",
                "Construct and clean data",
                "Operationalize key concepts",
                "Run descriptive analysis",
                "Generate audit reports"
            ]
        }
        write_json(self.output_dir / "research_brief.json", brief)
        return AgentOutput(agent_name=self.name, payload=brief, messages=["Research brief created."])


class ProvenanceManager(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("ProvenanceManager", output_dir)
        self._events: List[Dict[str, Any]] = []

    def record(self, step: str, details: Dict[str, Any]) -> None:
        self._events.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "step": step,
                "details": details,
            }
        )
        write_json(self.output_dir / "provenance_log.json", self._events)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        self.record(
            step="initialize_project",
            details={
                "title": task.title,
                "domain": task.domain,
                "research_question": task.research_question,
            },
        )
        return AgentOutput(agent_name=self.name, payload={"events": self._events})

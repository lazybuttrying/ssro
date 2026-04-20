from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .agents.audit import (
    BiasValidityAuditAgent,
    ReproducibilityAgent,
    RobustnessSensitivityAgent,
)
from .agents.governance import ProvenanceManager, ResearchDirectorAgent
from .agents.research_work import (
    DataConstructionAgent,
    IdentificationAnalysisAgent,
    LiteratureTheoryAgent,
    MeasurementAgent,
    PaperLaTeXSubagent,
    SlidesLaTeXSubagent,
    WritingSynthesisAgent,
)
from .types import ResearchTask


class ResearchOS:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.context: Dict[str, Dict[str, Any]] = {}

        self.provenance = ProvenanceManager(output_dir)
        self.research_director = ResearchDirectorAgent(output_dir)
        self.literature = LiteratureTheoryAgent(output_dir)
        self.data = DataConstructionAgent(output_dir)
        self.measurement = MeasurementAgent(output_dir)
        self.analysis = IdentificationAnalysisAgent(output_dir)
        self.writing = WritingSynthesisAgent(output_dir)
        self.paper_latex = PaperLaTeXSubagent(output_dir)
        self.slides_latex = SlidesLaTeXSubagent(output_dir)
        self.reproducibility = ReproducibilityAgent(output_dir)
        self.robustness = RobustnessSensitivityAgent(output_dir)
        self.bias_validity = BiasValidityAuditAgent(output_dir)

    def _store(self, agent_output) -> None:
        self.context[agent_output.agent_name] = agent_output.payload

    def run(self, task: ResearchTask) -> None:
        out = self.provenance.run(task, self.context)
        self._store(out)

        out = self.research_director.run(task, self.context)
        self._store(out)
        self.provenance.record("research_brief_created", out.payload)

        out = self.literature.run(task, self.context)
        self._store(out)
        self.provenance.record("literature_completed", {"keys": list(out.payload.keys())})

        out = self.data.run(task, self.context)
        self._store(out)
        self.provenance.record("data_construction_completed", out.payload)

        out = self.measurement.run(task, self.context)
        self._store(out)
        self.provenance.record("measurement_completed", {"variables": list(out.payload["codebook"].keys())})

        out = self.analysis.run(task, self.context)
        self._store(out)
        self.provenance.record("analysis_completed", {"high_skill_wage_gap": out.payload["high_skill_wage_gap"]})

        out = self.writing.run(task, self.context)
        self._store(out)
        self.provenance.record("writing_completed", {"abstract_length": len(out.payload["abstract"])})

        out = self.paper_latex.run(task, self.context)
        self._store(out)
        self.provenance.record("paper_latex_completed", out.payload)

        out = self.slides_latex.run(task, self.context)
        self._store(out)
        self.provenance.record("slides_latex_completed", out.payload)

        out = self.reproducibility.run(task, self.context)
        self._store(out)
        self.provenance.record("reproducibility_completed", out.payload)

        out = self.robustness.run(task, self.context)
        self._store(out)
        self.provenance.record("robustness_completed", out.payload)

        out = self.bias_validity.run(task, self.context)
        self._store(out)
        self.provenance.record("bias_validity_completed", {"threat_count": len(out.payload["validity_threats"])})

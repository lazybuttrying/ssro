from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import pandas as pd

from ..base import BaseAgent
from ..schemas.design_registry import DesignRegistry
from ..schemas.measurement_registry import MeasurementEntry
from ..schemas.research_entities import ResearchEntities
from ..storage.artifact_store import ArtifactStore
from ..storage.duckdb_store import DuckDBStore
from ..types import AgentOutput, ResearchTask
from ..utils import write_json, write_text


class LiteratureTheoryAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("LiteratureTheoryAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        literature_map = {
            "core_concepts": [
                "skill-biased technological change",
                "task automation",
                "AI complementarity vs substitution",
                "labor-market polarization",
            ],
            "mechanisms": [
                {
                    "name": "complementarity",
                    "description": "AI raises productivity more for workers who can effectively leverage it.",
                },
                {
                    "name": "substitution",
                    "description": "AI replaces routine or codifiable tasks, reducing demand for some occupations.",
                },
                {
                    "name": "recomposition",
                    "description": "AI changes the skill bundle required for a job rather than fully replacing it.",
                },
            ],
            "hypothesis_candidates": [
                "AI-related postings may demand higher analytical and digital skills.",
                "Wage differences may widen if AI is more complementary to high-skill jobs.",
                "Some middle-skill administrative tasks may become more automated over time.",
            ],
        }
        write_json(self.output_dir / "literature_map.json", literature_map)
        return AgentOutput(agent_name=self.name, payload=literature_map)


class DataConstructionAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("DataConstructionAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        data_path = Path("data/raw/sample_job_postings.csv")
        df = pd.read_csv(data_path)
        df["education"] = df["education"].fillna("Unknown")
        df["wage_posted"] = pd.to_numeric(df["wage_posted"], errors="coerce")
        df = df.drop_duplicates(subset=["id"])
        df["year"] = df["year"].astype(int)

        cleaned_path = self.output_dir / "cleaned_data.csv"
        df.to_csv(cleaned_path, index=False)

        duck = DuckDBStore(self.output_dir / "ssro.duckdb")
        duck.write_df("cleaned_postings", df)

        data_memo = {
            "rows": int(len(df)),
            "columns": list(df.columns),
            "unit_of_observation": "job_posting",
            "notes": [
                "Synthetic starter dataset used for demonstration.",
                "Replace with real job-posting data in production.",
            ],
        }
        write_json(self.output_dir / "data_memo.json", data_memo)
        return AgentOutput(
            agent_name=self.name,
            payload={
                "data_path": str(cleaned_path),
                "data_memo": data_memo,
                "duckdb_path": str(self.output_dir / "ssro.duckdb"),
            },
        )


class MeasurementAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("MeasurementAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        data_path = Path(context["DataConstructionAgent"]["data_path"])
        duckdb_path = Path(context["DataConstructionAgent"]["duckdb_path"])
        df = pd.read_csv(data_path)

        education_score_map = {"HighSchool": 1, "Bachelor": 2, "Master": 3, "PhD": 4, "Unknown": 0}
        df["education_score"] = df["education"].map(education_score_map).fillna(0)

        high_skill_keywords = ["python", "econometrics", "evaluation", "mlops", "causal inference", "api"]
        low_routine_keywords = ["scheduling", "packing", "scanning", "crm"]

        def keyword_score(text: str, keywords: list[str]) -> int:
            lowered = str(text).lower()
            return int(sum(1 for kw in keywords if kw in lowered))

        df["high_skill_signal"] = df["skills_text"].apply(lambda x: keyword_score(x, high_skill_keywords))
        df["routine_signal"] = df["skills_text"].apply(lambda x: keyword_score(x, low_routine_keywords))
        df["ai_exposure_score"] = df["ai_related"] * 2 + (df["high_skill_signal"] > 0).astype(int)
        df["high_skill_job"] = ((df["education_score"] >= 2) | (df["high_skill_signal"] >= 1)).astype(int)

        measured_path = self.output_dir / "measured_data.csv"
        df.to_csv(measured_path, index=False)

        duck = DuckDBStore(duckdb_path)
        duck.write_df("measured_postings", df)

        codebook = {
            "education_score": "Ordinal proxy for formal education requirements.",
            "high_skill_signal": "Count of high-skill keywords in skills text.",
            "routine_signal": "Count of routine-task keywords in skills text.",
            "ai_exposure_score": "Simple proxy: AI-related label plus text-based skill signal.",
            "high_skill_job": "Binary indicator for jobs that likely require higher skill levels.",
        }
        write_json(self.output_dir / "codebook.json", codebook)

        registry = [
            MeasurementEntry(
                variable="education_score",
                concept="formal education requirement",
                definition="ordinal proxy for stated education level",
                construction_rule="HighSchool=1, Bachelor=2, Master=3, PhD=4, Unknown=0",
                data_source="sample_job_postings.csv",
                known_limitations=["education does not fully capture skill intensity"],
                alternative_operationalizations=["use occupational taxonomies", "use human annotation"],
            ).to_dict(),
            MeasurementEntry(
                variable="ai_exposure_score",
                concept="AI exposure",
                definition="simple proxy for AI-related work content",
                construction_rule="ai_related*2 + 1 if any high-skill keyword is present",
                data_source="sample_job_postings.csv",
                known_limitations=["keyword and label proxy may misclassify actual task-level exposure"],
                alternative_operationalizations=["task-based exposure index", "classifier-based measure"],
            ).to_dict(),
            MeasurementEntry(
                variable="high_skill_job",
                concept="job skill level",
                definition="binary high-skill indicator",
                construction_rule="1 if education_score >= 2 or high_skill_signal >= 1",
                data_source="sample_job_postings.csv",
                known_limitations=["education and keywords are incomplete proxies"],
                alternative_operationalizations=["wage-based threshold", "occupation-based mapping"],
            ).to_dict(),
        ]
        write_json(self.output_dir / "measurement_registry.json", registry)
        duck.write_df("measurement_registry", pd.DataFrame(registry))

        return AgentOutput(
            agent_name=self.name,
            payload={
                "measured_data_path": str(measured_path),
                "codebook": codebook,
                "measurement_registry_path": str(self.output_dir / "measurement_registry.json"),
            },
        )


class IdentificationAnalysisAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("IdentificationAnalysisAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        data_path = Path(context["MeasurementAgent"]["measured_data_path"])
        duckdb_path = Path(context["DataConstructionAgent"]["duckdb_path"])
        df = pd.read_csv(data_path)

        mean_wage_by_ai_related = df.groupby("ai_related")["wage_posted"].mean()
        mean_wage_by_high_skill_job = df.groupby("high_skill_job")["wage_posted"].mean()
        mean_ai_exposure_by_education = df.groupby("education")["ai_exposure_score"].mean()
        share_high_skill_by_ai_related = df.groupby("ai_related")["high_skill_job"].mean()

        summary = {
            "mean_wage_by_ai_related": mean_wage_by_ai_related.to_dict(),
            "mean_wage_by_high_skill_job": mean_wage_by_high_skill_job.to_dict(),
            "mean_ai_exposure_by_education": mean_ai_exposure_by_education.to_dict(),
            "share_high_skill_by_ai_related": share_high_skill_by_ai_related.to_dict(),
        }

        simple_gap = float(df[df["high_skill_job"] == 1]["wage_posted"].mean() - df[df["high_skill_job"] == 0]["wage_posted"].mean())

        fig_path = self.output_dir / "figure_wage_by_ai_related.png"
        fig, ax = plt.subplots(figsize=(6, 4))
        mean_wage_by_ai_related.plot(kind="bar", ax=ax)
        ax.set_title("Mean posted wage by AI-related posting")
        ax.set_xlabel("AI related")
        ax.set_ylabel("Mean posted wage")
        fig.tight_layout()
        fig.savefig(fig_path, dpi=150)
        plt.close(fig)

        analysis_results = {
            "descriptive_summary": summary,
            "high_skill_wage_gap": simple_gap,
            "figure_path": str(fig_path),
            "interpretation": [
                "In this toy dataset, AI-related postings are associated with higher posted wages.",
                "High-skill jobs display a substantial wage premium relative to lower-skill jobs.",
                "This starter analysis is descriptive and not causal.",
            ],
            "suggested_causal_designs": [
                "Difference-in-differences using staggered AI tool adoption across firms or occupations.",
                "Event study around public release or enterprise adoption of generative AI tools.",
                "Regional or occupational exposure designs combined with pre-trend checks.",
            ],
        }
        write_json(self.output_dir / "analysis_results.json", analysis_results)

        design_registry = DesignRegistry(
            analysis_type="descriptive",
            unit="job_posting",
            treatment="ai_related / ai_exposure_score",
            outcome="posted wage and high-skill share",
            time_index="year",
            key_assumptions=["synthetic data are only illustrative", "descriptive patterns are not causal estimates"],
            threats_to_identification=[
                "selection into observed postings",
                "industry composition effects",
                "measurement error in AI exposure",
            ],
            planned_checks=[
                "alternative exposure definitions",
                "subset analysis by education",
                "event-study design with real data",
            ],
        ).to_dict()
        write_json(self.output_dir / "design_registry.json", design_registry)

        entities = ResearchEntities(
            research_question=task.research_question,
            concepts=["AI exposure", "skill level", "labor-market inequality"],
            variables=["ai_exposure_score", "high_skill_job", "wage_posted"],
            datasets=["sample_job_postings.csv", "cleaned_postings", "measured_postings"],
            designs=["descriptive comparison", "future DiD/event study candidate"],
            results=["ai-related wage difference", "high-skill wage gap"],
            limitations=[
                "synthetic data",
                "simple keyword proxy",
                "descriptive analysis only",
            ],
        ).to_dict()
        write_json(self.output_dir / "research_entities.json", entities)

        duck = DuckDBStore(duckdb_path)
        duck.write_df("analysis_summary", pd.DataFrame([{
            "high_skill_wage_gap": simple_gap,
            "mean_wage_ai_0": summary["mean_wage_by_ai_related"].get(0, summary["mean_wage_by_ai_related"].get("0")),
            "mean_wage_ai_1": summary["mean_wage_by_ai_related"].get(1, summary["mean_wage_by_ai_related"].get("1")),
        }]))
        duck.write_df("design_registry", pd.DataFrame([design_registry]))
        duck.write_df("research_entities", pd.DataFrame([entities]))

        return AgentOutput(
            agent_name=self.name,
            payload={
                **analysis_results,
                "design_registry_path": str(self.output_dir / "design_registry.json"),
                "research_entities_path": str(self.output_dir / "research_entities.json"),
            },
        )


class WritingSynthesisAgent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("WritingSynthesisAgent", output_dir)

    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        abstract = (
            "This project demonstrates a minimal social science Research OS using a three-layer multi-agent architecture. "
            "In a toy application on generative AI and labor-market inequality, the system separates governance, research work, and audit into distinct responsibilities. "
            "The pipeline constructs data, operationalizes AI exposure and skill proxies, produces descriptive inequality analysis, stores research artifacts in DuckDB, and generates reproducibility and validity reports."
        )
        write_text(self.output_dir / "abstract_draft.txt", abstract)

        working_note = "\n".join([
            "# Working note",
            "",
            f"## Research question\n{task.research_question}",
            "",
            "## Data",
            "Synthetic job-postings dataset used as a starter application package.",
            "",
            "## Measurement",
            "AI exposure and skill level are proxied using simple labels, education rules, and keyword signals.",
            "",
            "## Findings",
            "The current outputs show higher posted wages in AI-related postings and a substantial wage premium for high-skill jobs.",
            "",
            "## Limitations",
            "The analysis is descriptive, synthetic, and uses simplified measurement rules.",
            "",
            "## Next step",
            "Replace the synthetic data with real job-postings data and move to a stronger causal design.",
        ])
        write_text(self.output_dir / "working_note.md", working_note)

        artifact_store = ArtifactStore(self.output_dir)
        artifact_store.text("notes/summary.txt", "SSRO completed a minimal governance-work-audit run.")

        return AgentOutput(agent_name=self.name, payload={"abstract": abstract, "working_note_path": str(self.output_dir / 'working_note.md')})

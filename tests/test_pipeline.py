from pathlib import Path

from research_os.orchestrator import ResearchOS
from research_os.types import ResearchTask


def test_pipeline_runs_and_creates_outputs(tmp_path: Path) -> None:
    task = ResearchTask(
        title="Generative AI and labor-market inequality",
        research_question="How does AI reshape inequality?",
        domain="labor_market_inequality",
    )
    ros = ResearchOS(output_dir=tmp_path)
    ros.run(task)

    assert (tmp_path / "research_brief.json").exists()
    assert (tmp_path / "analysis_results.json").exists()
    assert (tmp_path / "provenance_log.json").exists()

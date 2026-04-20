from pathlib import Path

from research_os.orchestrator import ResearchOS
from research_os.types import ResearchTask


def test_pipeline_creates_extended_outputs(tmp_path: Path) -> None:
    task = ResearchTask(
        title="Generative AI and labor-market inequality",
        research_question="How does AI reshape inequality?",
        domain="labor_market_inequality",
    )
    ros = ResearchOS(output_dir=tmp_path)
    ros.run(task)

    assert (tmp_path / "measurement_registry.json").exists()
    assert (tmp_path / "design_registry.json").exists()
    assert (tmp_path / "working_note.md").exists()

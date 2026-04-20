from pathlib import Path

from research_os.orchestrator import ResearchOS
from research_os.types import ResearchTask


def test_pipeline_creates_tex_outputs(tmp_path: Path) -> None:
    task = ResearchTask(
        title="Generative AI and labor-market inequality",
        research_question="How does AI reshape inequality?",
        domain="labor_market_inequality",
    )
    ros = ResearchOS(output_dir=tmp_path)
    ros.run(task)

    assert (tmp_path / "paper" / "main.tex").exists()
    assert (tmp_path / "paper" / "sections" / "intro.tex").exists()
    assert (tmp_path / "paper" / "config" / "preamble.tex").exists()
    assert (tmp_path / "slides" / "main.tex").exists()
    assert (tmp_path / "slides" / "sections" / "motivation.tex").exists()
    assert (tmp_path / "slides" / "config" / "theme.tex").exists()

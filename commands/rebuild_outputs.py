import json
from pathlib import Path

from hooks.check_outputs_ready import check_outputs_ready
from research_os.agents.research_work import PaperLaTeXSubagent, SlidesLaTeXSubagent
from research_os.types import ResearchTask


def load_task(output_dir: Path) -> ResearchTask:
    brief_path = output_dir / "research_brief.json"
    if brief_path.exists():
        with brief_path.open("r", encoding="utf-8") as f:
            brief = json.load(f)
        return ResearchTask(
            title=brief.get("title", "SSRO rebuild"),
            research_question=brief.get("research_question", "Unknown research question"),
            domain=brief.get("domain", "unknown"),
            notes="Rebuilt paper/slides from existing outputs.",
        )

    return ResearchTask(
        title="SSRO rebuild",
        research_question="Unknown research question",
        domain="unknown",
        notes="Rebuilt paper/slides from existing outputs.",
    )


def main() -> None:
    output_dir = Path("outputs")

    ok, msg = check_outputs_ready(output_dir)
    if not ok:
        raise RuntimeError(msg)

    task = load_task(output_dir)

    analysis_path = output_dir / "analysis_results.json"
    with analysis_path.open("r", encoding="utf-8") as f:
        analysis_results = json.load(f)

    working_note_path = output_dir / "working_note.md"
    if not working_note_path.exists():
        raise RuntimeError("Missing working_note.md for output rebuild.")

    context = {
        "WritingSynthesisAgent": {
            "working_note_path": str(working_note_path),
        },
        "IdentificationAnalysisAgent": analysis_results,
    }

    paper = PaperLaTeXSubagent(output_dir)
    slides = SlidesLaTeXSubagent(output_dir)

    paper.run(task, context)
    slides.run(task, context)

    print("Rebuilt paper and slides outputs successfully.")


if __name__ == "__main__":
    main()

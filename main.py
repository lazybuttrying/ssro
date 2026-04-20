from pathlib import Path

from research_os.orchestrator import ResearchOS
from research_os.types import ResearchTask


def main() -> None:
    task = ResearchTask(
        title="Generative AI and labor-market inequality",
        research_question=(
            "How might generative AI reshape skill demand and inequality in labor markets?"
        ),
        domain="labor_market_inequality",
        notes="Starter example for a 3-level Social Science Research OS.",
    )

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    ros = ResearchOS(output_dir=output_dir)
    ros.run(task)


if __name__ == "__main__":
    main()

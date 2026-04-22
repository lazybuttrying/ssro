from pathlib import Path

import yaml

from research_os.orchestrator import ResearchOS
from research_os.types import ResearchTask


def load_settings() -> dict:
    settings_path = Path("configs/ssro_settings.yaml")
    with settings_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    settings = load_settings()

    task = ResearchTask(
        title="Generative AI and labor-market inequality",
        research_question=(
            "How might generative AI reshape skill demand and inequality in labor markets?"
        ),
        domain=settings.get("default_application", "labor_market_inequality"),
        notes="Starter example for a 3-level Social Science Research OS.",
    )

    output_dir = Path(settings.get("output_dir", "outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    ros = ResearchOS(output_dir=output_dir, settings=settings)
    ros.run(task)


if __name__ == "__main__":
    main()

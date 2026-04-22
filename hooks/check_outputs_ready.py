from pathlib import Path


def check_outputs_ready(output_dir: Path) -> tuple[bool, str]:
    output_dir = Path(output_dir)
    analysis_path = output_dir / "analysis_results.json"
    figure_path = output_dir / "figure_wage_by_ai_related.png"

    missing = []
    if not analysis_path.exists():
        missing.append(str(analysis_path))
    if not figure_path.exists():
        missing.append(str(figure_path))

    if missing:
        return False, f"Missing required output artifacts: {missing}"
    return True, "Analysis outputs are ready for paper/slides generation."

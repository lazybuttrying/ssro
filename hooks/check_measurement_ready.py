from pathlib import Path


def check_measurement_ready(output_dir: Path) -> tuple[bool, str]:
    output_dir = Path(output_dir)
    required = [
        output_dir / "measurement_registry.json",
        output_dir / "design_registry.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        return False, f"Missing required measurement/design artifacts: {missing}"
    return True, "Measurement and design artifacts are ready."

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..utils import write_json, write_text


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def json(self, relative_path: str, obj: Any) -> Path:
        path = self.root / relative_path
        write_json(path, obj)
        return path

    def text(self, relative_path: str, text: str) -> Path:
        path = self.root / relative_path
        write_text(path, text)
        return path

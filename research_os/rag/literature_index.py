from pathlib import Path


class LiteratureIndex:
    def __init__(self, root: Path):
        self.root = Path(root)

    def load_documents(self) -> list[dict]:
        docs = []
        literature_map = self.root / "literature_map.json"
        if literature_map.exists():
            docs.append({
                "id": "literature_map",
                "text": literature_map.read_text(encoding="utf-8"),
                "source": str(literature_map),
            })
        return docs

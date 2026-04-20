from pathlib import Path


class MemoIndex:
    def __init__(self, root: Path):
        self.root = Path(root)

    def load_documents(self) -> list[dict]:
        docs = []
        if not self.root.exists():
            return docs
        for path in list(self.root.iterdir()):
            if path.suffix == ".md":
                docs.append({
                    "id": path.stem,
                    "text": path.read_text(encoding="utf-8"),
                    "source": str(path),
                })
        return docs

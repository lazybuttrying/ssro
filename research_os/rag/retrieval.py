from pathlib import Path


def tokenize(text: str) -> set[str]:
    return set(str(text).lower().replace("_", " ").replace("-", " ").split())


def score_query(query: str, text: str) -> int:
    q = tokenize(query)
    t = tokenize(text)
    return len(q.intersection(t))


def retrieve_top_k(query: str, documents: list[dict], k: int = 3) -> list[dict]:
    scored = []
    for doc in documents:
        score = score_query(query, doc.get("text", ""))
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:k] if score > 0]

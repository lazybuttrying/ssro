from dataclasses import asdict, dataclass


@dataclass
class ResearchEntities:
    research_question: str
    concepts: list[str]
    variables: list[str]
    datasets: list[str]
    designs: list[str]
    results: list[str]
    limitations: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

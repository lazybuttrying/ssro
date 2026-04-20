from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class MeasurementEntry:
    variable: str
    concept: str
    definition: str
    construction_rule: str
    data_source: str
    known_limitations: list[str]
    alternative_operationalizations: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

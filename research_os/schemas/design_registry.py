from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class DesignRegistry:
    analysis_type: str
    unit: str
    treatment: str
    outcome: str
    time_index: str
    key_assumptions: list[str]
    threats_to_identification: list[str]
    planned_checks: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

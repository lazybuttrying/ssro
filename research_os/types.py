from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ResearchTask:
    title: str
    research_question: str
    domain: str
    notes: str = ""


@dataclass
class AgentOutput:
    agent_name: str
    payload: Dict[str, Any] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)

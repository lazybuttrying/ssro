from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from .types import AgentOutput, ResearchTask


class BaseAgent(ABC):
    def __init__(self, name: str, output_dir: Path):
        self.name = name
        self.output_dir = output_dir

    @abstractmethod
    def run(self, task: ResearchTask, context: Dict[str, Any]) -> AgentOutput:
        raise NotImplementedError

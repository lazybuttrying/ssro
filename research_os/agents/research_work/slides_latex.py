from pathlib import Path

from ...base import BaseAgent
from ...types import AgentOutput, ResearchTask
from ...utils import write_text


class SlidesLaTeXSubagent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("SlidesLaTeXSubagent", output_dir)

    def run(self, task: ResearchTask, context: dict) -> AgentOutput:
        slides_root = self.output_dir / "slides"
        frames_dir = slides_root / "sections"
        config_dir = slides_root / "config"
        img_dir = slides_root / "img"

        frames_dir.mkdir(parents=True, exist_ok=True)
        config_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)

        write_text(config_dir / "theme.tex", "\\usetheme{Madrid}\n")

        main_tex = """\\documentclass{beamer}
\\input{config/theme}
\\title{SSRO Slide Draft}
\\author{SSRO}
\\date{\\today}

\\begin{document}

\\frame{\\titlepage}

\\input{sections/motivation}
\\input{sections/data}
\\input{sections/measurement}
\\input{sections/results}
\\input{sections/next_steps}

\\end{document}
"""
        write_text(slides_root / "main.tex", main_tex)

        write_text(frames_dir / "motivation.tex", "\\begin{frame}{Motivation}\n\\begin{itemize}\n\\item SSRO structures social science research into governance, work, and audit.\n\\end{itemize}\n\\end{frame}\n")
        write_text(frames_dir / "data.tex", "\\begin{frame}{Data}\n\\begin{itemize}\n\\item Synthetic job-postings dataset for the starter demo.\n\\end{itemize}\n\\end{frame}\n")
        write_text(frames_dir / "measurement.tex", "\\begin{frame}{Measurement}\n\\begin{itemize}\n\\item AI exposure and high-skill indicators are built from simple starter rules.\n\\end{itemize}\n\\end{frame}\n")
        write_text(frames_dir / "results.tex", "\\begin{frame}{Results}\n\\begin{itemize}\n\\item AI-related postings show higher mean posted wages in the toy dataset.\n\\end{itemize}\n\\end{frame}\n")
        write_text(frames_dir / "next_steps.tex", "\\begin{frame}{Next Steps}\n\\begin{itemize}\n\\item Replace synthetic data with real data.\n\\item Add stronger causal designs.\n\\end{itemize}\n\\end{frame}\n")

        return AgentOutput(agent_name=self.name, payload={"slides_main_tex": str(slides_root / "main.tex")})

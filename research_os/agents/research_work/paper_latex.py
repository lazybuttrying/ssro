from pathlib import Path

from ...base import BaseAgent
from ...types import AgentOutput, ResearchTask
from ...utils import write_text


class PaperLaTeXSubagent(BaseAgent):
    def __init__(self, output_dir):
        super().__init__("PaperLaTeXSubagent", output_dir)

    def run(self, task: ResearchTask, context: dict) -> AgentOutput:
        paper_root = self.output_dir / "paper"
        sections_dir = paper_root / "sections"
        config_dir = paper_root / "config"
        img_dir = paper_root / "img"

        sections_dir.mkdir(parents=True, exist_ok=True)
        config_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)

        write_text(config_dir / "preamble.tex", "\\usepackage{graphicx}\n\\usepackage{booktabs}\n\\usepackage{amsmath}\n")

        main_tex = """\\documentclass[11pt]{article}
\\input{config/preamble}
\\title{SSRO Working Paper Draft}
\\author{SSRO}
\\date{\\today}

\\begin{document}
\\maketitle

\\input{sections/intro}
\\input{sections/data}
\\input{sections/measurement}
\\input{sections/results}
\\input{sections/limitations}

\\end{document}
"""
        write_text(paper_root / "main.tex", main_tex)

        working_note = context.get("WritingSynthesisAgent", {}).get("working_note_path", "")
        intro_text = "\\section{Introduction}\nThis paper draft is generated from SSRO outputs.\\n"
        if working_note:
            intro_text += "% Source working note: " + str(working_note) + "\n"
        write_text(sections_dir / "intro.tex", intro_text)
        write_text(sections_dir / "data.tex", "\\section{Data}\\nThis section summarizes the input dataset and unit of observation.\\n")
        write_text(sections_dir / "measurement.tex", "\\section{Measurement}\\nThis section documents variable construction and measurement choices.\\n")
        write_text(sections_dir / "results.tex", "\\section{Results}\\nThis section summarizes the descriptive results and figure references.\\n")
        write_text(sections_dir / "limitations.tex", "\\section{Limitations}\\nThis section documents the current limitations of the starter pipeline.\\n")

        return AgentOutput(agent_name=self.name, payload={"paper_main_tex": str(paper_root / "main.tex")})

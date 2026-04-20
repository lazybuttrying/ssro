# LaTeX workflow

SSRO now includes two LaTeX output modes:

- paper mode
- slides mode

## Why both exist

The repository separates content generation from output formatting.

The same research outputs can be rendered as:
- a paper-style draft
- a beamer-style slide deck draft

## Output structure

### Paper
- `outputs/paper/main.tex`
- `outputs/paper/config/`
- `outputs/paper/sections/`
- `outputs/paper/img/`

The paper `main.tex` uses `\input{}` to load each section file.

### Slides
- `outputs/slides/main.tex`
- `outputs/slides/config/`
- `outputs/slides/sections/`
- `outputs/slides/img/`

The slide `main.tex` also uses `\input{}` to load each frame file.

## Current behavior

When the main pipeline runs, SSRO:
1. creates research outputs
2. writes a working note
3. builds paper and slides folders
4. writes `main.tex` files
5. writes section files
6. copies the generated figure into each `img/` folder when available

## Current limitation

The current LaTeX subagents generate starter drafts, not polished publication-ready outputs.

## Better next step

A stronger next version should:
- populate sections from registries and notes more richly
- add table formatting and bibliography handling
- add artifact consistency checks for figure and citation references

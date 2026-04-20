def write_frame(title: str, bullets: list[str]) -> str:
    body = "\n".join([f"\\item {b}" for b in bullets])
    return f"\\begin{{frame}}{{{title}}}\n\\begin{{itemize}}\n{body}\n\\end{{itemize}}\n\\end{{frame}}\n"

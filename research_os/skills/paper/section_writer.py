def write_section(title: str, body: str) -> str:
    return f"\\section{{{title}}}\n{body}\n"

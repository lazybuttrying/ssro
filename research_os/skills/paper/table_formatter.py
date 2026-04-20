def simple_table_to_latex(headers: list[str], rows: list[list[str]]) -> str:
    cols = "l" * len(headers)
    lines = [f"\\begin{{tabular}}{{{cols}}}", "\\toprule", " & ".join(headers) + " \\\", "\\midrule"]
    for row in rows:
        lines.append(" & ".join(str(x) for x in row) + " \\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    return "\n".join(lines)

import os

def generate_markdown_report(reports: list, timeline_df, out_path: str):
    lines = ["# ForenPy - Relatório de Triagem\n"]
    lines.append("## Sumário\n")
    lines.append(f"- Arquivos analisados: {len(reports)}\n")

    lines.append("## Timeline\n")
    try:
        lines.append(timeline_df.to_markdown(index=False))
    except Exception:
        lines.append("(não foi possível gerar a tabela de timeline)\n")

    lines.append("\n\n## Detalhes\n")
    for r in reports:
        lines.append(f"### {r['path']}\n")
        lines.append(f"- SHA256: `{r['sha256']}`\n")
        lines.append(f"- MD5: `{r['md5']}`\n")
        if r.get("ela_image"):
            lines.append(f"- ELA: ![]({r['ela_image']})\n")
        if r.get("ocr_text"):
            txt = r['ocr_text'].strip().replace("\n", "  \n")
            lines.append(f"- OCR text:\n\n```\n{txt}\n```\n")
    md = "\n".join(lines)
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

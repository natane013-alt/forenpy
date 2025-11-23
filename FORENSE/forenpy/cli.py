import argparse
from forenpy import metadata, ela, ocr_module, timeline, report
import os
import glob

def main():
    parser = argparse.ArgumentParser(description="ForenPy - triagem forense básica")
    parser.add_argument("input", help="arquivo ou pasta para analisar")
    parser.add_argument("--ela", action="store_true", help="gerar E.L.A. para imagens jpeg")
    parser.add_argument("--ocr", action="store_true", help="rodar OCR em imagens")
    parser.add_argument("--out", default="forenpy_report.md", help="arquivo de saída (Markdown)")
    args = parser.parse_args()

    paths = []
    if os.path.isdir(args.input):
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.pdf", "*.docx", "*.*"]:
            paths.extend(glob.glob(os.path.join(args.input, ext)))
    else:
        paths = [args.input]

    reports = []
    for p in paths:
        try:
            rep = metadata.file_report(p)
        except Exception as e:
            print("Erro metadata:", e)
            continue
        if args.ela and p.lower().endswith(('.jpg', '.jpeg')):
            ela_out = p + ".ela.png"
            try:
                ela.ela_image(p, ela_out)
                rep["ela_image"] = ela_out
            except Exception as e:
                print("Erro ELA:", e)
        if args.ocr and p.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                rep["ocr_text"] = ocr_module.ocr_image(p)
            except Exception as e:
                print("Erro OCR:", e)
        reports.append(rep)

    df = timeline.build_timeline(reports)
    report.generate_markdown_report(reports, df, args.out)
    print("Relatório gerado:", args.out)

if __name__ == "__main__":
    main()

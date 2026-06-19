from __future__ import annotations
import argparse, asyncio, json
from pathlib import Path
from skatlaz_surftask_mcp.core.webtools import analyze_url
from skatlaz_surftask_mcp.core.screenshots import screenshot_url
from skatlaz_surftask_mcp.core.reports import make_docx_report

def main():
    ap = argparse.ArgumentParser(description="Skatlaz SurfTask MCP CLI")
    ap.add_argument("url", help="URL do site para analisar")
    ap.add_argument("--screenshot", action="store_true", help="Cria miniatura PNG do site")
    ap.add_argument("--docx", action="store_true", help="Cria relatório DOCX")
    args = ap.parse_args()
    page = analyze_url(args.url, "outputs")
    if args.screenshot:
        page["thumbnail"] = asyncio.run(screenshot_url(args.url, "screenshots"))
    if args.docx:
        page["docx_report"] = make_docx_report(page, Path("reports") / "site_report.docx")
    print(json.dumps(page, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

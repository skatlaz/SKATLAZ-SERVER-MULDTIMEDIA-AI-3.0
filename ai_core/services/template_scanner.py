from pathlib import Path


def scan_pugex_templates(language="html"):
    root = Path(__file__).resolve().parents[2]
    lang = (language or "html").lower().replace("c++", "cpp").replace("c#", "csharp")
    folder = root / "pugex" / lang / "templates"
    items = []
    if folder.exists():
        for p in sorted(folder.glob("*")):
            if p.is_file():
                items.append({"title": p.stem, "filename": p.name, "path": str(p.relative_to(root)).replace("\\\\", "/")})
    return {"language": lang, "path": f"/pugex/{lang}/templates/", "items": items}

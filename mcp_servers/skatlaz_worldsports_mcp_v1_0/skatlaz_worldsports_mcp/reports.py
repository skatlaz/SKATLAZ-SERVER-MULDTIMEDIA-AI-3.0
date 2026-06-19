from pathlib import Path
from datetime import datetime
import json

def markdown_report(title, sections, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", f"Generated: {datetime.now().isoformat()}", ""]
    for heading, content in sections:
        lines += [f"## {heading}", ""]
        if isinstance(content, (dict, list)):
            lines += ["```json", json.dumps(content, ensure_ascii=False, indent=2), "```", ""]
        else:
            lines += [str(content), ""]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return str(output_path)

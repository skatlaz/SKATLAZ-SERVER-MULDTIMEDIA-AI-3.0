from pathlib import Path
from jinja2 import Template

DEFAULT_TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head><meta charset="utf-8"><title>{{ title }}</title>
<style>
body{font-family:Arial,sans-serif;background:#f8f5ec;color:#4f5525;margin:40px;}
.card{background:white;border:1px solid #c9a646;border-radius:18px;padding:32px;box-shadow:0 8px 30px #0002;}
h1{color:#6B7A2D}.muted{color:#7a5a24}.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));}
</style></head><body><div class="card"><h1>{{ title }}</h1><p class="muted">{{ subtitle }}</p><div class="grid">{% for item in items %}<div><h3>{{ item.title }}</h3><p>{{ item.text }}</p></div>{% endfor %}</div></div></body></html>
"""

def render_template(output_path: str, title: str, subtitle: str = '', items: list[dict] | None = None, template_text: str | None = None) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    html = Template(template_text or DEFAULT_TEMPLATE).render(title=title, subtitle=subtitle, items=items or [])
    Path(output_path).write_text(html, encoding='utf-8')
    return output_path

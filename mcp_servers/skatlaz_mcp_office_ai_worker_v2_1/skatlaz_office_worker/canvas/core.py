from pathlib import Path
from jinja2 import Template

DEFAULT_TEMPLATE = '''<!doctype html><html lang="pt-br"><head><meta charset="utf-8"><title>{{ title }}</title><style>{{ css }}</style></head><body><main class="page"><h1>{{ title }}</h1><section>{{ body }}</section></main></body></html>'''
DEFAULT_CSS = 'body{font-family:Arial;background:#f8f5ec;color:#222}.page{max-width:1000px;margin:30px auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 28px #0002}h1{color:#6B7A2D;border-bottom:3px solid #C9A646;padding-bottom:10px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:8px}'

def render_html(template_text: str, data: dict, out_html: str) -> str:
    p=Path(out_html); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(Template(template_text).render(**data), encoding='utf-8')
    return str(p)


def create_report_html(title: str, body: str, out_html: str, css: str = DEFAULT_CSS) -> str:
    return render_html(DEFAULT_TEMPLATE, {'title':title,'body':body.replace('\n','<br>'),'css':css}, out_html)

import re, json, shutil
from pathlib import Path
from datetime import datetime
from .config import GENERATED_DIR, SUPPORTED_LANGUAGES
from .llm import LLMClient

LANG_EXT = {
    'python':'py','php':'php','perl':'pl','cgi':'cgi','html':'html','css':'css','javascript':'js',
    'typescript':'ts','nodejs':'js','java':'java','kotlin':'kt','dart':'dart','flutter':'dart',
    'kivy':'py','c':'c','cpp':'cpp','csharp':'cs','assembler':'asm','ruby':'rb','go':'go',
    'rust':'rs','zig':'zig','sql':'sql','bash':'sh','powershell':'ps1','katlaz':'katlaz'
}

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9_-]+','-', text.strip().lower())
    return text.strip('-')[:50] or 'gexprog-project'

class CodeGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def detect_language(self, prompt: str, default='python') -> str:
        p = prompt.lower()
        for lang in SUPPORTED_LANGUAGES:
            if lang in p:
                return lang
        aliases = {'c++':'cpp','c#':'csharp','js':'javascript','ts':'typescript','shell':'bash'}
        for k,v in aliases.items():
            if k in p:
                return v
        return default

    def generate_code(self, prompt: str, language: str | None = None) -> dict:
        language = language or self.detect_language(prompt)
        system = f"Você é o Skatlaz GexProg MCP. Gere código limpo, seguro, documentado, em {language}. Inclua comentários e instruções curtas."
        code = self.llm.generate(prompt, system)
        return {'language': language, 'code': code, 'created_at': datetime.utcnow().isoformat()}

    def create_project(self, prompt: str, language: str | None = None, name: str | None = None) -> dict:
        language = language or self.detect_language(prompt)
        name = name or slugify(prompt)
        project_dir = GENERATED_DIR / name
        if project_dir.exists():
            shutil.rmtree(project_dir)
        project_dir.mkdir(parents=True)
        result = self.generate_code(prompt, language)
        ext = LANG_EXT.get(language,'txt')
        main_file = project_dir / f'main.{ext}'
        main_file.write_text(result['code'], encoding='utf-8')
        (project_dir / 'README.md').write_text(self.create_readme(name, prompt, language), encoding='utf-8')
        (project_dir / 'gexprog_manifest.json').write_text(json.dumps({
            'name': name, 'language': language, 'prompt': prompt, 'created_at': result['created_at']
        }, indent=2, ensure_ascii=False), encoding='utf-8')
        if language == 'python':
            (project_dir / 'requirements.txt').write_text('# adicione dependencias aqui\n', encoding='utf-8')
        return {'project': name, 'path': str(project_dir), 'main_file': str(main_file), **result}

    def create_readme(self, name, prompt, language):
        return f"""# {name}\n\nProjeto gerado pelo **Skatlaz GexProg MCP v1.0**.\n\n## Linguagem\n\n{language}\n\n## Prompt original\n\n```text\n{prompt}\n```\n\n## Como usar\n\nAbra o arquivo principal e revise o código gerado antes de executar.\n\n## Observação\n\nPara geração avançada, configure Ollama com `deepseek-coder` ou provedor compatível via variáveis de ambiente.\n"""

    def explain(self, code: str, language='python'):
        return self.llm.generate(f'Explique o código abaixo em português:\n```{language}\n{code}\n```', 'Você é um professor de programação.')

    def refactor(self, code: str, language='python'):
        return self.llm.generate(f'Refatore e melhore este código mantendo comportamento:\n```{language}\n{code}\n```', 'Você é um engenheiro de software sênior.')

    def debug(self, code: str, error: str='', language='python'):
        return self.llm.generate(f'Corrija o código. Erro: {error}\n```{language}\n{code}\n```', 'Você é especialista em debugging.')

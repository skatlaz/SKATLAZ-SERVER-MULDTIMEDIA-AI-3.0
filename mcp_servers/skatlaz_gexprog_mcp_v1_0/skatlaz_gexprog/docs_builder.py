from pathlib import Path

class DocsBuilder:
    def build_readme(self, project_name, description, tools=None):
        tools = tools or []
        return f"""# {project_name}\n\n{description}\n\n## Recursos\n\n""" + '\n'.join([f'- {t}' for t in tools]) + "\n\n## Instalação\n\n```bash\npip install -r requirements.txt\n```\n\n## Uso\n\n```bash\npython main.py\n```\n"

    def write_docs(self, folder, project_name, description):
        folder=Path(folder); folder.mkdir(parents=True, exist_ok=True)
        (folder/'README.md').write_text(self.build_readme(project_name, description), encoding='utf-8')
        (folder/'ROADMAP.md').write_text('# Roadmap\n\n- v1.0 Base funcional\n- v2.0 Testes, CI/CD e RAG avançado\n', encoding='utf-8')
        (folder/'CHANGELOG.md').write_text('# Changelog\n\n## v1.0\n- Projeto inicial\n', encoding='utf-8')
        return {'docs':[str(folder/'README.md'),str(folder/'ROADMAP.md'),str(folder/'CHANGELOG.md')]}

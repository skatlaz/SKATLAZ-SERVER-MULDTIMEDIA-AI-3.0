from django.core.management.base import BaseCommand
from django.utils.text import slugify
from ai_core.models import AgentCategory, LlmProvider, AiAgent, AITaskType, AIMCPServer, AIAgent, AIJSONLibrary, PromptTemplate
from ai_core.services.gemini_mcp_builder import build_mcp_json

class Command(BaseCommand):
    help = "Cria parâmetros iniciais MCP e preserva estrutura legacy do Skatlaz Server AI"

    def handle(self, *args, **kwargs):
        cat, _ = AgentCategory.objects.get_or_create(name="General AI", defaults={"slug":"general-ai", "description":"Categoria padrão dos agentes Skatlaz"})
        provider, _ = LlmProvider.objects.get_or_create(name="Google Gemini", defaults={"provider_type":"gemini", "model_name":"gemini-1.5-flash", "api_key_env":"GEMINI_API_KEY"})
        legacy_prompts = {
            "Assistant": "Assistente geral do Skatlaz Server AI 2.0.",
            "Code": "Agente para programação, templates e geração de arquivos.",
            "Debug": "Agente para correção de logs e erros por ambiente.",
            "RAG": "Agente para indexação e busca em documentos.",
            "Web Diver": "Agente para crawling, tarefas web e coleta de dados.",
        }
        for name, prompt in legacy_prompts.items():
            AiAgent.objects.get_or_create(name=name, defaults={"slug": slugify(name), "category":cat, "provider":provider, "role":name.lower(), "system_prompt":prompt})
            PromptTemplate.objects.get_or_create(title=f"{name} Prompt", defaults={"slug": slugify(f'{name} Prompt'), "category": name, "prompt": prompt})

        defaults = {
            "code":"Gerar código por linguagem, template e sistema operacional.",
            "debug":"Corrigir erros por linguagem, ambiente e logs.",
            "image":"Criar prompts zturbo/HuggingFace com hashtags e cinewiz.json.",
            "documents":"Tratar PDF, PowerPoint, HTML, CSS, planilhas e textos.",
        }
        for code, desc in defaults.items():
            AITaskType.objects.get_or_create(code=code, defaults={"title":code.title(),"description":desc,"default_prompt":desc})
            mcp, _ = AIMCPServer.objects.get_or_create(name=f"Skatlaz {code.title()} MCP", task_type=code, defaults={"system_prompt":desc,"config_json":build_mcp_json(code, desc)})
            AIAgent.objects.get_or_create(name=f"MCP Agent {code.title()}", slug=f"mcp-agent-{code}", task_type=code, defaults={"mcp_server":mcp,"base_prompt":desc,"mcp_json":mcp.config_json})
        AIJSONLibrary.objects.get_or_create(key="cinewiz-json", defaults={"title":"cinewiz.json","task_type":"image","source":"cinewiz","json_data":{"hashtags":{},"style_keys":{},"zturbo_best_commands":[]}})
        AIJSONLibrary.objects.get_or_create(key="docs-template-json", defaults={"title":"docs_template.json","task_type":"documents","source":"docs_template","json_data":{"templates":[],"formats":["pdf","pptx","xlsx","html","css"]}})
        self.stdout.write(self.style.SUCCESS("Skatlaz legacy admin + MCP seed criado/atualizado."))

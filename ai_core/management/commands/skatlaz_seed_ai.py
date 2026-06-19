from django.core.management.base import BaseCommand
from ai_core.models import LLMProvider, PromptTemplate, AgentCategory, AIAgent, RAGCollection

class Command(BaseCommand):
    help = "Create default providers, categories, agents and a RAG collection."
    def handle(self, *args, **kwargs):
        ollama,_=LLMProvider.objects.get_or_create(name="Ollama Local", defaults={"provider_type":"ollama","base_url":"http://localhost:11434","default_model":"llama3.1","embedding_model":"nomic-embed-text"})
        gemini,_=LLMProvider.objects.get_or_create(name="Google Gemini", defaults={"provider_type":"gemini","api_key_env":"GOOGLE_API_KEY","default_model":"gemini-2.0-flash"})
        tmpl,_=PromptTemplate.objects.get_or_create(name="RAG Generativo", defaults={"category":"rag","system_prompt":"Você é o Skatlaz Server AI. Responda usando o contexto RAG quando existir. Se faltar informação, diga claramente.","user_template":"Pergunta: {question}\n\nContexto RAG/WebDiver:\n{context}"})
        for name, slug, desc, tools in [("Pesquisador","pesquisador","Busca, RAG e WebDiver",["rag","webdiver"]),("Programador","programador","Ajuda com código e arquitetura",["rag","python"]),("Resumidor","resumidor","Resume documentos",["rag"]),("Crawler","crawler","Coleta sites com WebDiver",["webdiver"]),("Imagem","imagem","Preparação futura para imagens",["image_search","bing_images"] )]:
            cat,_=AgentCategory.objects.get_or_create(name=name, slug=slug, defaults={"description":desc})
            AIAgent.objects.get_or_create(name=f"Agente {name}", defaults={"category":cat,"provider":ollama,"prompt_template":tmpl,"model_name":"llama3.1","description":desc,"tools":tools})
        RAGCollection.objects.get_or_create(name="Base Principal", defaults={"description":"Coleção inicial para uploads, CSV, PDF, DOCX e WebDiver.","embedding_provider":ollama,"embedding_model":"nomic-embed-text"})
        self.stdout.write(self.style.SUCCESS("Skatlaz Server AI 2.0 seed created."))

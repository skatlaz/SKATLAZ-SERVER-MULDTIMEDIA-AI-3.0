from ai_core.models import AIAgent, ChatSession, ChatMessage, RAGCollection
from ai_core.rag.retriever import retrieve_context
from ai_core.providers.ollama_provider import OllamaProvider
from ai_core.providers.gemini_provider import GeminiProvider

def _provider_instance(provider):
    if not provider or provider.provider_type == "ollama": return OllamaProvider(base_url=getattr(provider, "base_url", "http://localhost:11434"), model=getattr(provider, "default_model", "llama3.1") or "llama3.1")
    if provider.provider_type == "gemini": return GeminiProvider(api_key_env=provider.api_key_env or "GOOGLE_API_KEY", model=provider.default_model or "gemini-2.0-flash")
    return OllamaProvider()

def ask_agent(question: str, agent: AIAgent|None=None, collection: RAGCollection|None=None, session: ChatSession|None=None) -> dict:
    if agent is None: agent=AIAgent.objects.filter(enabled=True).first()
    provider=agent.provider if agent else None
    tmpl=agent.prompt_template if agent and agent.prompt_template else None
    context=retrieve_context(collection, question) if collection else ""
    system=tmpl.system_prompt if tmpl else "You are Skatlaz Server AI. Use context when available."
    user_prompt=tmpl.user_template.format(question=question, context=context) if tmpl else f"{question}\n\nContext:\n{context}"
    answer=_provider_instance(provider).chat([{"role":"system","content":system},{"role":"user","content":user_prompt}], model=(agent.model_name if agent and agent.model_name else None))
    if session:
        ChatMessage.objects.create(session=session, role="user", content=question, provider=provider, model_name=(agent.model_name if agent else ""))
        ChatMessage.objects.create(session=session, role="assistant", content=answer, provider=provider, model_name=(agent.model_name if agent else ""), metadata={"context": context[:4000]})
    return {"answer": answer, "agent": agent.name if agent else "default", "context_used": bool(context)}

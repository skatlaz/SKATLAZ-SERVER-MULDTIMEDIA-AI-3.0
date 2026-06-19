import requests
from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL

class LLMClient:
    def __init__(self, provider: str = "ollama", model: str | None = None):
        self.provider = provider
        self.model = model or OLLAMA_MODEL

    def ask(self, prompt: str, system: str = "Você é um assistente educacional do Skatlaz Studies MCP.") -> str:
        if self.provider == "ollama":
            try:
                resp = requests.post(
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": prompt},
                        ],
                        "stream": False,
                    },
                    timeout=30,
                )
                if resp.ok:
                    data = resp.json()
                    return data.get("message", {}).get("content", "").strip() or self.local_answer(prompt)
            except Exception:
                pass
        return self.local_answer(prompt)

    def local_answer(self, prompt: str) -> str:
        return (
            "Resposta local Skatlaz Studies MCP: "
            + prompt.strip()[:500]
            + "\n\nDica: ative o Ollama para respostas avançadas."
        )

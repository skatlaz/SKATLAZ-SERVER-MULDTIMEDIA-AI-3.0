from .llm import LLMClient
from .memory import MemoryStore
from ..config import DATA_DIR

class ChatAgent:
    def __init__(self):
        self.memory = MemoryStore(DATA_DIR / "studies_memory.sqlite3")
        self.llm = LLMClient()

    def ask(self, prompt: str, user_id: str = "default", agent: str = "teacher") -> dict:
        system = self._system_for_agent(agent)
        self.memory.add(user_id, "user", prompt)
        answer = self.llm.ask(prompt, system=system)
        self.memory.add(user_id, "assistant", answer)
        return {"agent": agent, "user_id": user_id, "answer": answer}

    def history(self, user_id: str = "default", limit: int = 20):
        return self.memory.history(user_id, limit)

    def _system_for_agent(self, agent: str) -> str:
        agents = {
            "teacher": "Você é um professor claro e didático do Skatlaz Studies MCP.",
            "support": "Você é um atendente profissional e objetivo do Skatlaz Server AI.",
            "designer": "Você é um designer criativo que gera ideias visuais, banners, slides e templates.",
            "writer": "Você é um escritor e revisor de textos educacionais e profissionais.",
        }
        return agents.get(agent, agents["teacher"])

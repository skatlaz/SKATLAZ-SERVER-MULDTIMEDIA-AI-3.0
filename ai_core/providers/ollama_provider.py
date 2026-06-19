import json, urllib.request
from typing import Any, Dict, List

class OllamaProvider:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        self.base_url = base_url.rstrip("/"); self.model = model
    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib.request.Request(f"{self.base_url}{path}", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read().decode())
    def chat(self, messages: List[Dict[str,str]], model: str|None=None, **options: Any) -> str:
        payload={"model": model or self.model, "messages": messages, "stream": False}
        if options: payload["options"]=options
        try: return self._post("/api/chat", payload).get("message",{}).get("content","")
        except Exception as exc: return f"[Ollama error: {exc}]"
    def generate(self, prompt: str, model: str|None=None, system: str="", **options: Any) -> str:
        payload={"model": model or self.model, "prompt": prompt, "stream": False}
        if system: payload["system"]=system
        if options: payload["options"]=options
        try: return self._post("/api/generate", payload).get("response","")
        except Exception as exc: return f"[Ollama error: {exc}]"
    def embed(self, text: str, model: str="nomic-embed-text") -> list[float]:
        try: return self._post("/api/embeddings", {"model": model, "prompt": text}).get("embedding", [])
        except Exception: return []

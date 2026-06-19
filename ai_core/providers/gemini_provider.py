import os
from typing import Any, List, Dict

class GeminiProvider:
    def __init__(self, api_key_env: str="GOOGLE_API_KEY", model: str="gemini-2.0-flash"):
        self.api_key_env=api_key_env; self.model=model
    def generate(self, prompt: str, system: str="", model: str|None=None, **kwargs: Any) -> str:
        api_key=os.getenv(self.api_key_env)
        if not api_key: return "[Gemini disabled: set GOOGLE_API_KEY or the configured env variable.]"
        try:
            from google import genai
            client=genai.Client(api_key=api_key)
            contents=f"{system}\n\n{prompt}" if system else prompt
            response=client.models.generate_content(model=model or self.model, contents=contents)
            return getattr(response, "text", "") or str(response)
        except Exception as exc: return f"[Gemini error: {exc}]"
    def chat(self, messages: List[Dict[str,str]], model: str|None=None, **kwargs: Any) -> str:
        return self.generate("\n".join(f"{m.get('role','user')}: {m.get('content','')}" for m in messages), model=model, **kwargs)

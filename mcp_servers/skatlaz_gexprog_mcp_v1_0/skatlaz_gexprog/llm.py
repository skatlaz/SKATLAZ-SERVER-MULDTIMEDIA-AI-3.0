import os, requests

class LLMClient:
    """Cliente simples para Ollama/OpenAI-compatible/DeepSeek-compatible.
    Se nenhum endpoint estiver configurado, usa modo template local.
    """
    def __init__(self):
        self.provider = os.getenv('GEXPROG_PROVIDER', 'local').lower()
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:6.7b')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL', '').rstrip('/')
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.openai_model = os.getenv('OPENAI_MODEL', 'deepseek-chat')

    def generate(self, prompt: str, system: str = '') -> str:
        if self.provider == 'ollama':
            return self._ollama(prompt, system)
        if self.provider in ('openai','deepseek','compatible') and self.openai_base_url:
            return self._openai_compatible(prompt, system)
        return self._local_template(prompt)

    def _ollama(self, prompt, system):
        payload = {'model': self.ollama_model, 'prompt': (system + '\n' + prompt).strip(), 'stream': False}
        r = requests.post(self.ollama_url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get('response','')

    def _openai_compatible(self, prompt, system):
        headers = {'Authorization': f'Bearer {self.openai_api_key}', 'Content-Type':'application/json'}
        payload = {
            'model': self.openai_model,
            'messages': [{'role':'system','content':system or 'You are a coding assistant.'},{'role':'user','content':prompt}],
            'temperature': 0.2,
        }
        r = requests.post(f'{self.openai_base_url}/chat/completions', headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']

    def _local_template(self, prompt):
        return f"""# GexProg local template response\n# Prompt recebido:\n# {prompt}\n\n# Configure GEXPROG_PROVIDER=ollama e OLLAMA_MODEL=deepseek-coder:6.7b\n# para geração avançada com DeepSeek Code local via Ollama.\n"""

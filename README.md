# Skatlaz Server Multimedia AI 3.0

# Beta VERSION

Servidor Django para IA generativa com painel administrativo, agentes por categoria, RAG, uploads de arquivos, WebDiver, Ollama, Google Gemini e preparação de LoRA/QLoRA para exportação ao Ollama.

## Instalação rápida

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py skatlaz_seed_ai
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/admin/` para configurar provedores, agentes, coleções RAG, datasets, tarefas WebDiver e jobs de fine-tuning.

## Endpoints

- `POST /ai/chat/` com `{ "prompt": "...", "agent_id": 1, "collection_id": 1 }`
- `GET /ai/models/list/`
- `GET /ai/rag/search/?q=texto&collection_id=1`
- `POST /ai/rag/index-source/` com `{ "source_id": 1 }`
- `POST /ai/crawler/start/` com `{ "url": "https://...", "diver_type": "_text", "collection_id": 1 }`
- `POST /ai/finetune/prepare/` com `{ "job_id": 1 }`
- `POST /ai/ollama/export/` com `{ "job_id": 1 }`

## Observação

O treinamento pesado LoRA/QLoRA deve rodar fora do processo web. O Django gera o script e o Modelfile; workers ou máquina GPU executam o treino.
